"""
Robust Action Handler - Unified system for handling challenging web automation tasks.

Features:
1. Action Sequence Memory - Save/replay successful patterns per domain
2. Enhanced Post-Action Detection - Detect new elements after actions
3. Fallback Chain - Ordered retry strategies for reliability
4. Visual Debugging - Element highlighting and step tracking
"""

import json
import os
import asyncio
from datetime import datetime
from urllib.parse import urlparse
from termcolor import colored


class RobustActionHandler:
    """
    A unified handler for robust web automation that learns from successful patterns
    and handles challenging UI interactions.
    """
    
    def __init__(self, knowledge_base_path: str = "knowledge/sites"):
        self.knowledge_base_path = knowledge_base_path
        self.action_history = []
        self.current_domain = None
        self.context_hints = []
        self.new_elements_detected = []
        
    def set_domain(self, url: str):
        """Set the current domain for pattern storage."""
        self.current_domain = urlparse(url).netloc
        
    # ==================== 1. ACTION SEQUENCE MEMORY ====================
    
    def get_sequences_path(self) -> str:
        """Get the path to action sequences file for current domain."""
        if not self.current_domain:
            return None
        domain_path = os.path.join(self.knowledge_base_path, self.current_domain)
        os.makedirs(domain_path, exist_ok=True)
        return os.path.join(domain_path, "action_sequences.json")
    
    def load_action_sequences(self) -> dict:
        """Load saved action sequences for the current domain."""
        path = self.get_sequences_path()
        if not path or not os.path.exists(path):
            return {}
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_action_sequence(self, sequence_name: str, actions: list):
        """Save a successful action sequence for future replay."""
        path = self.get_sequences_path()
        if not path:
            return
        
        sequences = self.load_action_sequences()
        sequences[sequence_name] = {
            "actions": actions,
            "last_success": datetime.now().isoformat(),
            "success_count": sequences.get(sequence_name, {}).get("success_count", 0) + 1
        }
        
        with open(path, 'w') as f:
            json.dump(sequences, f, indent=2)
        print(colored(f"   💾 Saved action sequence: {sequence_name}", "green"))
    
    def get_matching_sequence(self, goal_keywords: list) -> dict:
        """Find a matching saved sequence based on goal keywords."""
        sequences = self.load_action_sequences()
        for name, data in sequences.items():
            if any(keyword.lower() in name.lower() for keyword in goal_keywords):
                print(colored(f"   📚 Found matching sequence: {name} (used {data.get('success_count', 0)} times)", "cyan"))
                return data
        return None
    
    def record_action(self, action: str, target_id: str, target_text: str, success: bool):
        """Record an action to the history for potential sequence saving."""
        self.action_history.append({
            "action": action,
            "target_id": target_id,
            "target_text": target_text[:50] if target_text else "",
            "success": success,
            "timestamp": datetime.now().isoformat()
        })
    
    def save_successful_flow(self, flow_name: str):
        """Save the current action history as a successful flow."""
        successful_actions = [a for a in self.action_history if a["success"]]
        if successful_actions:
            self.save_action_sequence(flow_name, successful_actions)
    
    # ==================== 2. ENHANCED POST-ACTION DETECTION ====================
    
    async def detect_state_changes(self, page, elements_before: list, elements_after: list) -> dict:
        """Detect what changed after an action."""
        before_ids = {e.get('elementId') for e in elements_before}
        after_ids = {e.get('elementId') for e in elements_after}
        
        new_ids = after_ids - before_ids
        removed_ids = before_ids - after_ids
        
        # Find new elements
        new_elements = [e for e in elements_after if e.get('elementId') in new_ids]
        
        # Categorize new elements
        new_inputs = [e for e in new_elements if e.get('tagName') in ['input', 'textarea']]
        new_buttons = [e for e in new_elements if e.get('tagName') == 'button']
        new_links = [e for e in new_elements if e.get('tagName') == 'a']
        
        changes = {
            "new_count": len(new_elements),
            "removed_count": len(removed_ids),
            "new_inputs": new_inputs,
            "new_buttons": new_buttons,
            "new_links": new_links,
            "has_new_inputs": len(new_inputs) > 0,
            "has_new_buttons": len(new_buttons) > 0
        }
        
        self.new_elements_detected = new_elements
        
        if changes["new_count"] > 0:
            print(colored(f"   🆕 State Change: {changes['new_count']} new elements detected!", "cyan"))
            if changes["has_new_inputs"]:
                print(colored(f"      📝 {len(new_inputs)} new input fields available", "green"))
            if changes["has_new_buttons"]:
                print(colored(f"      🔘 {len(new_buttons)} new buttons available", "green"))
        
        return changes
    
    def get_context_hint(self) -> str:
        """Get a context hint for the Planner based on detected changes."""
        hints = []
        
        if self.new_elements_detected:
            input_count = len([e for e in self.new_elements_detected if e.get('tagName') in ['input', 'textarea']])
            if input_count > 0:
                hints.append(f"🆕 {input_count} new input field(s) are now available - consider filling them.")
        
        if self.context_hints:
            hints.extend(self.context_hints)
        
        return " ".join(hints)
    
    def add_context_hint(self, hint: str):
        """Add a context hint for the Planner."""
        self.context_hints.append(hint)
    
    def clear_context_hints(self):
        """Clear context hints after they've been used."""
        self.context_hints = []
        self.new_elements_detected = []
    
    # ==================== 3. FALLBACK CHAIN ====================
    
    FALLBACK_STRATEGIES = {
        "search": [
            {"name": "planner_natural", "desc": "Let Planner handle naturally"},
            {"name": "click_icon_wait", "desc": "Click icon, wait for popover"},
            {"name": "keyboard_shortcut", "desc": "Try Ctrl+F or / shortcut"},
            {"name": "direct_url", "desc": "Navigate to search URL directly"}
        ],
        "form_fill": [
            {"name": "direct_fill", "desc": "Fill input directly"},
            {"name": "click_then_fill", "desc": "Click to focus, then fill"},
            {"name": "type_keys", "desc": "Use keyboard.type()"},
            {"name": "js_injection", "desc": "Set value via JavaScript"}
        ],
        "button_click": [
            {"name": "direct_click", "desc": "Click directly"},
            {"name": "scroll_click", "desc": "Scroll into view, then click"},
            {"name": "force_click", "desc": "Click with force=True"},
            {"name": "js_click", "desc": "Click via JavaScript"}
        ]
    }
    
    def get_fallback_strategies(self, action_type: str) -> list:
        """Get ordered fallback strategies for an action type."""
        return self.FALLBACK_STRATEGIES.get(action_type, [])
    
    async def execute_with_fallbacks(self, page, action_type: str, primary_action, fallback_actions: dict) -> dict:
        """Execute an action with automatic fallback on failure."""
        strategies = self.get_fallback_strategies(action_type)
        
        for i, strategy in enumerate(strategies):
            strategy_name = strategy["name"]
            
            if strategy_name not in fallback_actions:
                continue
                
            print(colored(f"   🔄 Strategy {i+1}/{len(strategies)}: {strategy['desc']}", "grey"))
            
            try:
                result = await fallback_actions[strategy_name]()
                if result.get("success"):
                    print(colored(f"   ✅ Strategy '{strategy_name}' succeeded!", "green"))
                    return {"success": True, "strategy": strategy_name}
            except Exception as e:
                print(colored(f"   ⚠️ Strategy '{strategy_name}' failed: {str(e)[:50]}", "yellow"))
                continue
        
        return {"success": False, "strategy": None}
    
    # ==================== 4. VISUAL DEBUGGING ====================
    
    async def highlight_element(self, page, element_id: str, color: str = "#FF4444"):
        """Highlight an element on the page for visual debugging."""
        try:
            await page.evaluate(f"""
                (elementId, color) => {{
                    const el = document.querySelector(`[data-agent-id="${{elementId}}"]`);
                    if (el) {{
                        el.style.outline = `3px solid ${{color}}`;
                        el.style.outlineOffset = '2px';
                        setTimeout(() => {{
                            el.style.outline = '';
                            el.style.outlineOffset = '';
                        }}, 2000);
                    }}
                }}
            """, element_id, color)
        except:
            pass
    
    async def show_action_indicator(self, page, x: float, y: float, action: str = "click"):
        """Show a visual indicator at the action location."""
        colors = {
            "click": "#FF4444",
            "fill": "#44FF44",
            "hover": "#4444FF"
        }
        color = colors.get(action, "#FF4444")
        
        try:
            await page.evaluate(f"""
                (x, y, color) => {{
                    const indicator = document.createElement('div');
                    indicator.style.cssText = `
                        position: fixed;
                        left: ${{x - 15}}px;
                        top: ${{y - 15}}px;
                        width: 30px;
                        height: 30px;
                        border: 3px solid ${{color}};
                        border-radius: 50%;
                        background: ${{color}}33;
                        pointer-events: none;
                        z-index: 999999;
                        animation: pulse 0.5s ease-out;
                    `;
                    document.body.appendChild(indicator);
                    setTimeout(() => indicator.remove(), 1000);
                }}
            """, x, y, color)
        except:
            pass
    
    # ==================== UNIFIED API ====================
    
    def get_summary(self) -> dict:
        """Get a summary of the handler's state."""
        return {
            "domain": self.current_domain,
            "actions_recorded": len(self.action_history),
            "successful_actions": len([a for a in self.action_history if a["success"]]),
            "context_hints": len(self.context_hints),
            "new_elements_detected": len(self.new_elements_detected)
        }
    
    def reset(self):
        """Reset the handler for a new session."""
        self.action_history = []
        self.context_hints = []
        self.new_elements_detected = []


# Singleton instance for easy access
_handler_instance = None

def get_handler(knowledge_base_path: str = "knowledge/sites") -> RobustActionHandler:
    """Get or create the singleton handler instance."""
    global _handler_instance
    if _handler_instance is None:
        _handler_instance = RobustActionHandler(knowledge_base_path)
    return _handler_instance
