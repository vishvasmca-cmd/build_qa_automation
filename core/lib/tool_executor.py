"""
Tool Executor - Replaces the old Code Generator/Executor pattern.
This executor calls pre-written tools instead of generating code.
"""

import asyncio
import json
import os
from termcolor import colored
from .tools import get_registry, ToolRegistry
from .visual_locator import VisualLocator
from playwright.async_api import Page
from typing import Dict, Any, List, Optional


class ToolExecutor:
    """
    Executes tool intents from the Planner.
    Replaces the old "Code Generator + Executor" pattern.
    """
    
    def __init__(self, trace_path: Optional[str] = None):
        self.registry: ToolRegistry = get_registry()
        self.execution_history: List[Dict] = []
        self.visual_locator = VisualLocator(confidence_threshold=0.8)
        self.trace_path = trace_path  # For self-healing trace updates
    
    async def _highlight_element(self, page: Page, arguments: Dict[str, Any]):
        """Highlights the target element with a visible border before interaction."""
        try:
            target = None
            if "selector" in arguments:
                target = page.locator(arguments["selector"]).first
            elif "text" in arguments:
                target = page.get_by_text(arguments["text"]).first
            elif "role" in arguments:
                # Basic role support - naive mapping
                target = page.get_by_role(arguments["role"]).first
                
            if target:
                # Magenta border + glow
                await target.evaluate("el => { el.style.outline = '3px solid #FF00FF'; el.style.boxShadow = '0 0 15px rgba(255, 0, 255, 0.7)'; el.style.transition = 'all 0.3s'; }")
                await page.wait_for_timeout(500) # 500ms visual pause
        except Exception:
            # Ignore highlighting errors (e.g., element not found, stale ref) to not break execution
            pass

    async def execute_intent(self, page: Page, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a single tool intent from the Planner.
        
        Args:
            page: Playwright Page object
            intent: Tool intent JSON from Planner
                    Format: {"tool": "perform_search", "arguments": {"query": "..."}}
        
        Returns:
            Execution result
        """
        tool_name = intent.get("tool")
        arguments = intent.get("arguments", {})
        
        if not tool_name:
            return {
                "status": "failure",
                "error": "No tool specified in intent"
            }
        
        print(colored(f"🔧 Executing Tool: {tool_name}", "cyan"))
        print(colored(f"   Arguments: {arguments}", "grey"))
        
        # 🌟 VISUAL DEBUGGING: Highlight target element before interaction
        await self._highlight_element(page, arguments)
        
        try:
            # Execute the tool through the registry
            result = await self.registry.execute_tool(
                tool_name=tool_name,
                page=page,
                **arguments
            )
            
            # Log the execution
            self.execution_history.append({
                "tool": tool_name,
                "arguments": arguments,
                "result": result
            })
            
            if result.get("status") == "success":
                print(colored(f"   ✅ Tool executed successfully", "green"))
            else:
                print(colored(f"   ⚠️ Tool execution failed: {result.get('error')}", "yellow"))
            
            return result
            
        except Exception as e:
            error_msg = f"Tool execution exception: {str(e)}"
            print(colored(f"   ❌ {error_msg}", "red"))
            
            return {
                "status": "failure",
                "error": error_msg
            }
    
    async def execute_workflow(self, page: Page, workflow: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute a sequence of tool intents (for Fast Lane skill replay).
        
        Args:
            page: Playwright Page object
            workflow: List of tool intents
        
        Returns:
            Overall workflow result
        """
        print(colored(f"📋 Executing workflow with {len(workflow)} steps", "cyan"))
        
        results = []
        for idx, intent in enumerate(workflow, 1):
            print(colored(f"\n--- Step {idx}/{len(workflow)} ---", "blue"))
            
            result = await self.execute_intent(page, intent)
            results.append(result)
            
            # Stop on failure if critical
            if result.get("status") == "failure" and not intent.get("optional", False):
                print(colored(f"❌ Workflow failed at step {idx}", "red"))
                return {
                    "status": "failure",
                    "completed_steps": idx - 1,
                    "failed_at": idx,
                    "error": result.get("error"),
                    "results": results
                }
        
        print(colored(f"\n✅ Workflow completed successfully", "green"))
        return {
            "status": "success",
            "completed_steps": len(workflow),
            "results": results
        }
    
    
    async def execute_with_fallback(
        self,
        page: Page,
        step_data: Dict[str, Any],
        screenshot_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute a step with multi-locator fallback strategy.
        Tries locators in priority order and promotes successful fallbacks.
        
        Args:
            page: Playwright page object
            step_data: Step from trace.json containing locators array
            screenshot_path: Current page screenshot for visual matching
            
        Returns:
            Execution result with used_locator info
        """
        
        action = step_data.get("action")
        
        # Handle 'done' action gracefully for replay
        if action == "done":
            print(colored("✅ Reached 'done' step. Fast Lane execution complete.", "green"))
            return {"status": "success", "message": "Mission completed successfully"}

        locators = step_data.get("locators", [])
        
        if not locators:
            # Fallback to old single-locator format
            locator_used = step_data.get("locator_used")
            value = step_data.get("value")
            
            if action == "smart_click" and locator_used:
                return await self.execute_intent(page, {
                    "tool": "smart_click",
                    "arguments": {"selector": locator_used}
                })
            elif action == "perform_search" and value:
                return await self.execute_intent(page, {
                    "tool": "perform_search",
                    "arguments": {"query": value}
                })
            else:
                return await self.execute_intent(page, {
                    "tool": action,
                    "arguments": step_data.get("arguments", {})
                })
        
        # Sort locators by (success_count * 10 + (5 - priority))
        sorted_locators = sorted(
            locators,
            key=lambda l: l.get("success_count", 0) * 10 + (5 - l.get("priority", 5)),
            reverse=True
        )
        
        print(colored(f"🔄 Trying {len(sorted_locators)} locator strategies...", "cyan"))
        
        for idx, locator_info in enumerate(sorted_locators, 1):
            loc_type = locator_info.get("type")
            loc_value = locator_info.get("value")
            
            print(colored(f"  [{idx}/{len(sorted_locators)}] Trying {loc_type}: {loc_value[:50] if isinstance(loc_value, str) else loc_value}", "grey"))
            
            try:
                # Build intent based on locator type
                if loc_type == "css" and action == "smart_click":
                    intent = {"tool": "smart_click", "arguments": {"selector": loc_value}}
                    
                elif loc_type == "text" and action == "smart_click":
                    intent = {"tool": "smart_click", "arguments": {"text": loc_value}}
                    
                elif loc_type == "role" and action == "smart_click":
                    intent = {"tool": "smart_click", "arguments": {"role": loc_value}}
                    
                elif loc_type == "xpath" and action == "smart_click":
                    # XPath selectors are supported by Playwright via page.locator()
                    intent = {"tool": "smart_click", "arguments": {"selector": loc_value}}
                    
                elif loc_type == "visual" and screenshot_path:
                    # Use visual locator
                    template_path = locator_info.get("template")
                    if not template_path:
                        continue
                    
                    # Make path absolute if needed
                    if not os.path.isabs(template_path):
                        trace_dir = os.path.dirname(self.trace_path) if self.trace_path else "."
                        template_path = os.path.join(trace_dir, template_path)
                    
                    match = self.visual_locator.find_element(screenshot_path, template_path)
                    
                    if not match:
                        print(colored(f"      ❌ Visual match failed", "yellow"))
                        continue
                    
                    # Click at matched coordinates
                    intent = {
                        "tool": "smart_click",
                        "arguments": {"coordinates": (match['x'], match['y'])}
                    }
                    
                elif action == "perform_search" and loc_type == "text":
                    # Support for replay of search actions
                    intent = {"tool": "perform_search", "arguments": {"query": loc_value}}
                    
                    
                else:
                    # Skip unsupported combinations
                    continue
                
                # Try executing
                result = await self.execute_intent(page, intent)
                
                if result.get("status") == "success":
                    print(colored(f"      ✅ SUCCESS with {loc_type} locator!", "green"))
                    
                    # Self-healing: Update trace if non-primary worked
                    if idx > 1:
                        self._self_heal_trace(step_data, locator_info)
                    
                    return {**result, "used_locator": locator_info, "fallback_used": idx > 1}
                    
            except Exception as e:
                print(colored(f"      ⚠️ Exception: {e}", "yellow"))
                continue
        
        # All locators failed
        print(colored(f"  ❌ All {len(sorted_locators)} locators failed", "red"))
        return {
            "status": "failure",
            "error": "All locator strategies exhausted",
            "tried_count": len(sorted_locators)
        }
    
    def _self_heal_trace(self, step_data: Dict, successful_locator: Dict):
        """
        Update trace.json to promote a successful fallback locator.
        Increments its success_count so it's tried first next time.
        """
        if not self.trace_path or not os.path.exists(self.trace_path):
            return
        
        try:
            # Increment success count
            successful_locator["success_count"] = successful_locator.get("success_count", 0) + 1
            
            # Update trace file
            with open(self.trace_path, 'r', encoding='utf-8') as f:
                trace_data = json.load(f)
            
            # Find and update the step
            for step in trace_data.get("trace", []):
                if step.get("step") == step_data.get("step"):
                    step["locators"] = step_data["locators"]  # Already updated in memory
                    break
            
            # Save updated trace
            with open(self.trace_path, 'w', encoding='utf-8') as f:
                json.dump(trace_data, f, indent=2)
            
            print(colored(f"  🔄 Self-healed: Promoted {successful_locator['type']} locator", "cyan"))
            
        except Exception as e:
            print(colored(f"  ⚠️ Self-heal failed: {e}", "yellow"))
    
    def get_execution_history(self) -> List[Dict]:
        """Get the history of executed tools"""
        return self.execution_history
    
    def clear_history(self):
        """Clear execution history"""
        self.execution_history = []
