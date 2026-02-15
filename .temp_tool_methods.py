
    async def _check_page_state_with_tools(self, page: Page, goal: str) -> Dict[str, Any]:
        """
        After page transition, use WebMCP tools to check state.
        Returns: {page_type, cart_count, cart_items, products, etc.}
        """
        import json
        state = {"url": page.url}
        url = page.url
        
        try:
            if 'cart.html' in url:
                # Check cart state
                self.log(f"    [TOOL-CHECK] Checking cart state...", "cyan")
                cart_result = await self._execute_webmcp_tool(page, "verify_cart_items", {})
                count_result = await self._execute_webmcp_tool(page, "get_cart_count", {})
                state.update({
                    "page_type": "cart",
                    "cart_items": cart_result.get("items", []) if cart_result.get("success") else [],
                    "cart_count": count_result.get("count", 0) if count_result.get("success") else 0
                })
                self.log(f"    [STATE] Cart: {state['cart_count']} items", "cyan")
            
            elif 'inventory.html' in url:
                # Check product listing
                self.log(f"    [TOOL-CHECK] Checking product listing...", "cyan")
                products_result = await self._execute_webmcp_tool(page, "get_sorted_products", {})
                if products_result.get("success"):
                    state.update({
                        "page_type": "inventory",
                        "products": products_result.get("products", []),
                        "cheapest": products_result.get("cheapest"),
                        "most_expensive": products_result.get("most_expensive")
                    })
                    self.log(f"    [STATE] Products: {len(state.get('products', []))}", "cyan")
            
            elif 'checkout' in url:
                # Check form completion and totals
                self.log(f"    [TOOL-CHECK] Checking checkout state...", "cyan")
                form_result = await self._execute_webmcp_tool(page, "verify_checkout_form", {})
                total_result = await self._execute_webmcp_tool(page, "verify_cart_total", {})
                state.update({
                    "page_type": "checkout",
                    "form_complete": form_result.get("is_complete", False) if form_result.get("success") else False,
                    "missing_fields": form_result.get("missing_fields", []) if form_result.get("success") else [],
                    "total_amount": total_result.get("total_amount", 0) if total_result.get("success") else 0
                })
                self.log(f"    [STATE] Form: {'Complete' if state.get('form_complete') else 'Incomplete'}", "cyan")
            else:
                state["page_type"] = "other"
        
        except Exception as e:
            self.log(f"    [WARN] State check error: {e}", "yellow")
            state["error"] = str(e)
        
        return state

    async def _reason_about_next_step(self, page: Page, goal: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use LLM to reason about what to do next given goal and current state.
        Returns: {should_continue: bool, suggested_action: str, reasoning: str}
        """
        import json
        from core.lib.llm_utils import try_parse_json
        
        prompt = f"""
GOAL: {goal}
CURRENT PAGE: {page.url}
CURRENT STATE: {json.dumps(state, indent=2)}

QUESTION: Should I proceed to the next workflow step, or take corrective action?

RULES:
- If cart_count < required (goal says "2 items"), suggest "add_missing_items"
- If cart_count > required, suggest "remove_excess_items"  
- If form incomplete, suggest "fill_missing_fields"
- If goal is met (at complete/confirmation page), suggest "goal_complete"
- Otherwise, suggest "continue_workflow"

OUTPUT (JSON):
{{"should_continue": true/false, "suggested_action": "add_missing_items|remove_excess_items|fill_missing_fields|goal_complete|continue_workflow", "reasoning": "explanation"}}
"""
        
        try:
            self.log(f"    [REASONING] Asking AI about next step...", "magenta")
            response = await self.llm.ainvoke([{"role": "user", "content": prompt}])
            result = try_parse_json(response.content)
            
            if not result:
                return {"should_continue": True, "suggested_action": "continue_workflow", "reasoning": "Failed to parse AI response"}
            
            self.log(f"    [AI-DECISION] {result.get('suggested_action')}: {result.get('reasoning')}", "magenta")
            return result
        
        except Exception as e:
            self.log(f"    [WARN] Reasoning error: {e}", "yellow")
            return {"should_continue": True, "suggested_action": "continue_workflow", "reasoning": f"Error: {e}"}
