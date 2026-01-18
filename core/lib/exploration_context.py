from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


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
