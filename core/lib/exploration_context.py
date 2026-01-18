from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import hashlib


@dataclass
class ActionRecord:
    """Records a single exploration action."""
    step_id: Any
    keyword: str
    description: str
    selector: Optional[str]
    success: bool
    timestamp: datetime
    error: Optional[str] = None
    confidence: Optional[float] = None
    page_url: Optional[str] = None


class ExplorationContext:
    """
    Maintains exploration state across steps to provide LLM with historical context.
    Helps prevent loops, track progress, and learn from failures.
    """
    
    def __init__(self, goal: str, base_url: str):
        self.goal = goal
        self.base_url = base_url
        self.actions_taken: List[ActionRecord] = []
        self.pages_visited: List[str] = []
        self.failed_selectors: List[Dict[str, Any]] = []
        self.successful_patterns: List[Dict[str, Any]] = []
        self.stuck_count = 0
        self.last_url = None
        self.url_visit_count: Dict[str, int] = {}
        
        # State fingerprinting for page equivalence
        self.state_fingerprints: Dict[str, Tuple[str, List[str]]] = {}  # {fingerprint: (url, actions_to_reach)}
        self.current_fingerprint: Optional[str] = None
        self.state_transitions: Dict[str, Dict[str, str]] = {}  # {from_state: {action: to_state}}
        
    def add_action(self, step_id: Any, keyword: str, description: str, 
                   selector: Optional[str], success: bool, page_url: str,
                   error: Optional[str] = None, confidence: Optional[float] = None):
        """Record an action attempt."""
        action = ActionRecord(
            step_id=step_id,
            keyword=keyword,
            description=description,
            selector=selector,
            success=success,
            timestamp=datetime.now(),
            error=error,
            confidence=confidence,
            page_url=page_url
        )
        self.actions_taken.append(action)
        
        # Track page visits
        if page_url not in self.pages_visited:
            self.pages_visited.append(page_url)
        
        self.url_visit_count[page_url] = self.url_visit_count.get(page_url, 0) + 1
        
        # Track stuck state (same page, multiple failures)
        if not success:
            if page_url == self.last_url:
                self.stuck_count += 1
            else:
                self.stuck_count = 0
            
            self.failed_selectors.append({
                "selector": selector,
                "description": description,
                "error": error,
                "page_url": page_url
            })
        else:
            self.stuck_count = 0
            if selector and confidence and confidence > 0.8:
                self.successful_patterns.append({
                    "selector": selector,
                    "description": description,
                    "confidence": confidence,
                    "page_url": page_url
                })
        
        self.last_url = page_url
    
    def is_stuck(self) -> bool:
        """Detect if we're in a loop or stuck state."""
        return self.stuck_count >= 3
    
    def has_visited_page(self, url: str) -> bool:
        """Check if we've been to this page before."""
        return url in self.pages_visited
    
    def get_visit_count(self, url: str) -> int:
        """Get number of times we've visited a page."""
        return self.url_visit_count.get(url, 0)
    
    def get_recent_actions(self, count: int = 5) -> List[ActionRecord]:
        """Get the most recent N actions."""
        return self.actions_taken[-count:] if self.actions_taken else []
    
    def get_failed_selectors_for_description(self, description: str) -> List[str]:
        """Get all selectors that failed for a specific description."""
        return [
            f["selector"] for f in self.failed_selectors 
            if f["description"] == description and f["selector"]
        ]
    
    def to_prompt_summary(self) -> str:
        """
        Convert exploration context to a concise summary for LLM prompts.
        """
        recent_actions = self.get_recent_actions(5)
        
        # Build action summary
        action_summary = []
        for action in recent_actions:
            status = "✅" if action.success else "❌"
            conf = f" (conf: {action.confidence:.2f})" if action.confidence else ""
            action_summary.append(
                f"{status} {action.keyword.upper()}: {action.description or 'N/A'}{conf}"
            )
        
        # Check for loops
        loop_warning = ""
        if self.is_stuck():
            loop_warning = "\n⚠️ **STUCK WARNING**: Multiple failures on same page. Need alternative strategy!"
        
        # Page visit frequency
        frequent_pages = [
            url for url, count in self.url_visit_count.items() if count > 2
        ]
        loop_info = ""
        if frequent_pages:
            loop_info = f"\n🔄 **Revisited Pages**: {', '.join(frequent_pages[:3])}"
        
        # Recent failures
        recent_failures = [f for f in self.failed_selectors[-3:]]
        failure_info = ""
        if recent_failures:
            failure_info = "\n❌ **Recent Failures**:\n" + "\n".join([
                f"  - '{f['description']}' using {f['selector']}" 
                for f in recent_failures if f['selector']
            ])
        
        summary = f"""
**EXPLORATION HISTORY:**
Goal: "{self.goal}"
Total Actions: {len(self.actions_taken)}
Pages Visited: {len(self.pages_visited)}

**Recent Actions (Last 5):**
{chr(10).join(action_summary) if action_summary else "No actions yet"}
{loop_warning}
{loop_info}
{failure_info}
"""
        return summary.strip()
    
    def to_dict(self) -> Dict:
        """Export context as dictionary for logging/debugging."""
        return {
            "goal": self.goal,
            "total_actions": len(self.actions_taken),
            "pages_visited": self.pages_visited,
            "stuck": self.is_stuck(),
            "recent_actions": [
                {
                    "keyword": a.keyword,
                    "description": a.description,
                    "success": a.success,
                    "confidence": a.confidence
                }
                for a in self.get_recent_actions(5)
            ]
        }
    
    def get_page_fingerprint(self, url: str, dom_snapshot: Optional[str] = None, form_state: Optional[Dict[str, str]] = None) -> str:
        """
        Generate state fingerprint from URL, DOM content, and form field values.
        
        Args:
            url: Current page URL
            dom_snapshot: Optional DOM content snapshot (first 5000 chars)
            form_state: Optional dict of form field values {field_name: field_value}
            
        Returns:
            MD5 hash representing page state including form data
        """
        # Use URL as primary identifier
        state_parts = [url]
        
        # Add DOM hash if available (for detecting dynamic content changes)
        if dom_snapshot:
            # Hash first 5000 chars to capture page structure without full content
            dom_hash = hashlib.md5(dom_snapshot[:5000].encode()).hexdigest()[:8]
            state_parts.append(dom_hash)
        
        # Add form state hash to detect field-level changes
        if form_state:
            # Sort keys for consistent hashing
            sorted_form = sorted(form_state.items())
            form_repr = "|".join([f"{k}={v}" for k, v in sorted_form if v])  # Only non-empty values
            if form_repr:  # Only add if there are filled fields
                form_hash = hashlib.md5(form_repr.encode()).hexdigest()[:8]
                state_parts.append(f"form:{form_hash}")
        
        # Combine and hash
        combined = "|".join(state_parts)
        return hashlib.md5(combined.encode()).hexdigest()
    
    def record_state(self, url: str, dom_snapshot: Optional[str] = None, form_state: Optional[Dict[str, str]] = None) -> bool:
        """
        Record current page state and detect if we've been here before.
        
        Args:
            url: Current page URL
            dom_snapshot: Optional DOM snapshot
            form_state: Optional form field values dict
            
        Returns:
            True if this is a NEW state, False if we've visited this exact state before
        """
        fingerprint = self.get_page_fingerprint(url, dom_snapshot, form_state)
        
        is_new_state = fingerprint not in self.state_fingerprints
        
        if is_new_state:
            # Track how we reached this state
            recent_step_ids = [a.step_id for a in self.get_recent_actions(3)]
            self.state_fingerprints[fingerprint] = (url, recent_step_ids)
        
        self.current_fingerprint = fingerprint
        return is_new_state
    
    def record_transition(self, from_state: str, action_desc: str, to_state: str):
        """
        Record state transition for path analysis.
        
        Args:
            from_state: State fingerprint before action
            action_desc: Action description (e.g., "click login-button")
            to_state: State fingerprint after action
        """
        if from_state not in self.state_transitions:
            self.state_transitions[from_state] = {}
        
        self.state_transitions[from_state][action_desc] = to_state
    
    def is_circular_navigation(self, target_fingerprint: str) -> bool:
        """
        Detect if we're about to navigate in a circle.
        
        Args:
            target_fingerprint: Fingerprint we're about to navigate to
            
        Returns:
            True if this would create a circular path
        """
        # Check if we've already visited this exact state
        if target_fingerprint in self.state_fingerprints:
            # Allow revisiting if it's been more than 5 actions ago
            _, steps_to_reach = self.state_fingerprints[target_fingerprint]
            recent_steps = [a.step_id for a in self.get_recent_actions(5)]
            
            # If any of the steps to reach this state are in recent actions, it's circular
            return any(step in recent_steps for step in steps_to_reach if step)
        
        return False
    
    def extract_shortest_path(self, start_state: str, goal_state: str) -> Optional[List[Tuple[str, str]]]:
        """
        Extract shortest path from start to goal state using BFS on state transitions.
        
        Args:
            start_state: Starting state fingerprint
            goal_state: Goal state fingerprint
            
        Returns:
            List of (state, action) tuples representing shortest path, or None if no path exists
        """
        from collections import deque
        
        if start_state == goal_state:
            return []
        
        if start_state not in self.state_transitions:
            return None
        
        # BFS to find shortest path
        queue = deque([(start_state, [])])
        visited = {start_state}
        
        while queue:
            current_state, path = queue.popleft()
            
            # Check all possible transitions from current state
            if current_state in self.state_transitions:
                for action, next_state in self.state_transitions[current_state].items():
                    if next_state in visited:
                        continue
                    
                    new_path = path + [(current_state, action)]
                    
                    if next_state == goal_state:
                        return new_path + [(next_state, "GOAL")]
                    
                    queue.append((next_state, new_path))
                    visited.add(next_state)
        
        return None  # No path found
    
    def get_optimized_steps(self) -> List[str]:
        """
        Get optimized step sequence by extracting shortest paths between key states.
        This removes redundant navigation loops and duplicate steps.
        
        Returns:
            List of step IDs representing the optimal path
        """
        if not self.state_fingerprints:
            return [a.step_id for a in self.actions_taken]
        
        # Find start and end states
        state_list = list(self.state_fingerprints.keys())
        if len(state_list) < 2:
            return [a.step_id for a in self.actions_taken]
        
        start_state = state_list[0]
        goal_state = state_list[-1]
        
        # Extract shortest path
        shortest_path = self.extract_shortest_path(start_state, goal_state)
        
        if not shortest_path:
            # Fallback to original steps if no optimization found
            return [a.step_id for a in self.actions_taken]
        
        # Convert state path to step IDs
        optimized_steps = []
        for state, action in shortest_path:
            if state in self.state_fingerprints:
                _, step_ids = self.state_fingerprints[state]
                optimized_steps.extend(step_ids)
        
        return optimized_steps
