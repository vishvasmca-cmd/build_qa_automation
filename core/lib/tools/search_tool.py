"""
Smart Search Tool - Handles search operations with auto-detection of submit method.
"""

import asyncio
from termcolor import colored
from .base_tool import Tool
from typing import Dict, Any
from playwright.async_api import Page


class SearchTool(Tool):
    """
    Intelligent search tool that:
    1. Finds search input (multiple strategies)
    2. Fills the query
    3. Auto-detects how to submit (Enter vs Button)
    """
    
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
        
        try:
            # Step 1: Find the search input
            search_input = await self._find_search_input(page)
            if not search_input:
                return {"status": "failure", "error": "Could not find search input"}
            
            # Step 2: Fill the search query
            await search_input.click()  # Focus
            await search_input.fill("")  # Clear
            await search_input.type(query, delay=50)  # Natural typing
            
            self._log(f"Entered query: '{query}'", "SUCCESS")
            
            # Step 3: Submit if requested
            if submit:
                submitted = await self._submit_search(page)
                if not submitted:
                    return {"status": "failure", "error": "Could not submit search"}
                
                # Wait for results
                await asyncio.sleep(2)
                self._log("Search submitted successfully", "SUCCESS")
            
            return {
                "status": "success",
                "query": query,
                "submitted": submit
            }
            
        except Exception as e:
            self.last_error = str(e)
            self._log(f"Search failed: {e}", "WARN")
            return {"status": "failure", "error": str(e)}
    
    async def _find_search_input(self, page: Page):
        """Find search input using multiple strategies (priority order)"""
        
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
            "description": "Search for a query on the current page",
            "arguments": {
                "query": "str - The search query",
                "submit": "bool (optional) - Whether to submit the search (default True)"
            },
            "example": {
                "tool": "perform_search",
                "arguments": {"query": "Universal Gravity", "submit": True}
            }
        }
