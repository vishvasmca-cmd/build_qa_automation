    async def _execute_tool_intent(self, page, decision, elements):
        """
        Execute a tool intent from the Planner (NEW PATTERN - replaces _execute_action).
        
        Args:
            page: Playwright Page object
            decision: JSON from Planner with {"tool": "...", "arguments": {...}}
            elements: Current DOM elements
            
        Returns:
            Dict with success status and outcome
        """
        tool_name = decision.get('tool')
        arguments = decision.get('arguments', {})
        
        if not tool_name:
            # Fallback to old pattern if Planner hasn't adapted yet
            if decision.get('action'):
                print(colored("⚠️ Planner used old 'action' format, falling back to legacy executor", "yellow"))
                return await self._execute_action(page, decision, elements)
            return {"success": False, "outcome": "No tool or action specified in decision"}
        
        # Execute the tool through ToolExecutor
        result = await self.tool_executor.execute_intent(page, decision)
        
        # Convert ToolExecutor result to legacy format for compatibility
        return {
            "success": result.get("status") == "success",
            "outcome": result.get("error") if result.get("status") == "failure" else f"Tool '{tool_name}' executed successfully"
        }
