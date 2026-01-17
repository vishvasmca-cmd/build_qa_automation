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
    async def _find_search_input(self, page: Page):
        """Find search input using multiple strategies (priority order)"""
        
        # Strategy 0: Dyson-specific search panel (appears after clicking search button)
        try:
            # Look for the enabled search panel input that appears in the modal
            panel_locator = page.locator('input.search-panel__input, input[name="q"][type="search"]')
            if await panel_locator.count() > 0:
                panel = panel_locator.first
                if await panel.is_visible() and not await panel.is_disabled():
                    self._log("Found Dyson search panel input")
                    return panel
        except Exception as e:
            self._log(f"Dyson panel check failed: {e}", "WARN")
            pass
        
        # Strategy 1: Look for explicit search role
        try:
            if await page.locator('[role="searchbox"]').count() > 0:
                return page.locator('[role="searchbox"]').first
        except:
            pass
        
        # Strategy 2: Look for common search attributes
        for selector in [
            '[placeholder*="Search" i]',
            '[placeholder*="Find" i]',
            '[aria-label*="Search" i]',
            '[name="q"]',  # Google-style
            '[name="search"]',
            'input[type="search"]'
        ]:
            try:
                if await page.locator(selector).count() > 0:
                    return page.locator(selector).first
            except:
                continue
        
        # Strategy 3: Look for text-based identification
        try:
            return page.get_by_placeholder("Search", exact=False)
        except:
            pass
        
        return None
    
    async def _activate_search_field(self, page: Page, input_element) -> bool:
        """
        Attempts to click a button/icon that activates the search bar.
        Used when the search input is present but disabled/hidden.
        """
        try:
            # 1. Try generic search toggles
            for selector in [
                'button[aria-label*="Search"]',
                '.search-toggle',
                '[data-testid*="search-icon"]',
                'svg[aria-label="Search"]',
                # Dyson specific
                'button.header__search-button' 
            ]:
                if await page.locator(selector).count() > 0:
                    btn = page.locator(selector).first
                    if await btn.is_visible():
                        await btn.click()
                        self._log(f"Clicked search trigger: {selector}")
                        await asyncio.sleep(0.5)
                        return True
            
            # 2. Try clicking the parent/container (often the wrapper handles the click)
            # parent = input_element.locator("..")
            # if await parent.is_visible():
            #     await parent.click()
            #     return True
                
        except Exception as e:
            self._log(f"Failed to activate search field: {e}", "WARN")
            
        return False
    
    async def _submit_search(self, page: Page) -> bool:
        """Auto-detect and execute search submission"""
        
        # Strategy 1: Look for explicit search button
        for selector in [
            'button[type="submit"]',
            '[aria-label*="Search" i]:has-text("Search")',
            'button:has-text("Search")',
            '.search-button',
            '#search-button'
        ]:
            try:
                if await page.locator(selector).is_visible(timeout=1000):
                    await page.locator(selector).click()
                    return True
            except:
                continue
        
        # Strategy 2: Press Enter (most common)
        try:
            await page.keyboard.press("Enter")
            # Use domcontentloaded instead of networkidle for dynamic sites
            try:
                await page.wait_for_load_state("domcontentloaded", timeout=3000)
            except:
                # If even domcontentloaded fails, just wait a bit
                await asyncio.sleep(1)
            return True
        except Exception as e:
            print(colored(f"  ⚠️ Enter key failed: {e}", "yellow"))
            pass
        
        return False
    
    def get_signature(self) -> Dict[str, Any]:
        return {
            "name": "perform_search",
            "description": "Search for a query. Automatically handles clicking/expanding the search bar if needed. DO NOT plan a separate click step before this.",
            "arguments": {
                "query": "str - The search query",
                "submit": "bool (optional) - Whether to submit the search (default True)"
            },
            "example": {
                "tool": "perform_search",
                "arguments": {"query": "Universal Gravity", "submit": True}
            }
        }
