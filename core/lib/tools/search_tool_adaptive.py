"""
Smart Search Tool - Handles search operations with auto-detection of submit method.
Now includes self-correction and adaptive learning capabilities.
"""

import asyncio
from termcolor import colored
from .base_tool import Tool
from .adaptive_tool import AdaptiveTool
from .pattern_generator import PatternGenerator
from typing import Dict, Any
from playwright.async_api import Page


class SearchTool(Tool):
    """
    Intelligent search tool that:
    1. Finds search input (multiple strategies)
    2. Fills the query
    3. Auto-detects how to submit (Enter vs Button)
    4. Learns site-specific patterns and generates custom methods
    """
    
    def __init__(self):
        super().__init__()
        # Use composition for adaptive capabilities
        self.adaptive = AdaptiveTool("perform_search")
        self.pattern_generator = PatternGenerator()
    
    async def execute(self, page: Page, query: str, submit: bool = True, **kwargs) -> Dict[str, Any]:
        """
        Execute a search operation.
        
        Args:
            page: Playwright page object
            query: Search query string
            submit: Whether to submit the search (default True)
            
        Returns:
            Dict with status and search details
        """
        self._log(f"Searching for: '{query}'")
        
        domain = self.adaptive.get_domain(page.url)
        
        # 🧠 ADAPTIVE: Check if we have a learned pattern for this domain
        if self.adaptive.has_custom_pattern(domain):
            pattern = self.adaptive.get_custom_pattern(domain)
            self._log(f"📚 Found learned pattern for {domain}", "SUCCESS")
            # TODO: Could execute custom pattern here in future
        
        try:
            # Step 1: Find the search input
            search_input = await self._find_search_input(page)
            if not search_input:
                # 📊 Track failure for learning
                await self.adaptive.track_failure(page, "Could not find search input", {
                    "query": query,
                    "method": "_find_search_input",
                    "step": "locate_input"
                })
                return {"status": "failure", "error": "Could not find search input"}
            
            # --- FIX: Handle Disabled Search Inputs (Popup/Expandable style) ---
            if await search_input.is_disabled() or not await search_input.is_visible():
                self._log("Search input is disabled/hidden. Looking for trigger...", "WARN")
                
                # Strategy: Click a "Search" icon/button to enable it
                trigger_clicked = await self._activate_search_field(page, search_input)
                
                if trigger_clicked:
                    # Wait for DOM to settle
                    await asyncio.sleep(1)
                    
                    # RE-FETCH the input (DOM might have changed!)
                    self._log("Re-fetching search input after trigger...", "INFO")
                    search_input = await self._find_search_input(page)
                    
                    if not search_input:
                        # 📊 Track failure
                        await self.adaptive.track_failure(page, "Search input disappeared after clicking trigger", {
                            "query": query,
                            "trigger_clicked": True,
                            "step": "refetch_after_trigger"
                        })
                        return {"status": "failure", "error": "Search input disappeared after clicking trigger"}
                    
                    # Wait for it to be enabled
                    try:
                        await search_input.wait_for(state="visible", timeout=2000)
                        # Check if enabled
                        for _ in range(5):  # Try 5 times
                            if not await search_input.is_disabled():
                                break
                            await asyncio.sleep(0.2)
                    except:
                        self._log("Input still not ready after trigger click", "WARN")

            # Step 2: Fill the search query
            try:
                # Force click if still stubborn
                await search_input.click(force=True, timeout=2000)
            except:
                pass
                
            await search_input.fill("")  # Clear
            await search_input.type(query, delay=50)  # Natural typing
            
            self._log(f"Entered query: '{query}'", "SUCCESS")
            
            # Step 3: Submit if requested
            if submit:
                submitted = await self._submit_search(page)
                if not submitted:
                    # 📊 Track failure
                    await self.adaptive.track_failure(page, "Could not submit search", {
                        "query": query,
                        "input_found": True,
                        "step": "submit"
                    })
                    return {"status": "failure", "error": "Could not submit search"}
                
                # Wait for results
                await asyncio.sleep(2)
                self._log("Search submitted successfully", "SUCCESS")
            
            # 🎉 Success! Reset failure tracking for this domain
            self.adaptive.reset_failures(domain)
            
            return {
                "status": "success",
                "query": query,
                "submitted": submit
            }
            
        except Exception as e:
            # 📊 Track unexpected failures
            await self.adaptive.track_failure(page, str(e), {
                "query": query,
                "exception_type": type(e).__name__,
                "step": "execution"
            })
            self.last_error = str(e)
            return {"status": "failure", "error": str(e)}
