"""
Smart Click Tool - Clicks elements using robust selector fallback chain.
"""

import asyncio
from termcolor import colored
from .base_tool import Tool
from typing import Dict, Any, Optional
from playwright.async_api import Page


class ClickTool(Tool):
    """
    Intelligent click tool that:
    1. Tries multiple selector strategies
    2. Handles overlays and pop-ups
    3. Falls back to coordinate-based clicking
    """
    
    async def execute(
        self, 
        page: Page, 
        selector: Optional[str] = None,
        text: Optional[str] = None,
        element_id: Optional[int] = None,
        force: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute a click operation.
        
        Args:
            page: Playwright page object
            selector: CSS/Playwright selector (priority 1)
            text: Text content to match (priority 2)
            element_id: Agent's element ID from DOM marker (priority 3)
            force: Force click even if obscured
            
        Returns:
            Dict with status and click details
        """
        
        try:
            # Determine click strategy
            if selector:
                return await self._click_by_selector(page, selector, force)
            elif text:
                return await self._click_by_text(page, text, force)
            elif element_id:
                return await self._click_by_agent_id(page, element_id, force)
            else:
                return {"status": "failure", "error": "No target specified"}
                
        except Exception as e:
            self.last_error = str(e)
            self._log(f"Click failed: {e}", "WARN")
            return {"status": "failure", "error": str(e)}
    
    async def _click_by_selector(self, page: Page, selector: str, force: bool) -> Dict[str, Any]:
        """Click using CSS/Playwright selector"""
        self._log(f"Clicking selector: {selector}")
        
        try:
            # Wait for element
            await page.wait_for_selector(selector, timeout=5000, state="visible")
            
            # Try normal click first
            if not force:
                await page.click(selector, timeout=3000)
            else:
                await page.click(selector, force=True, timeout=3000)
            
            self._log(f"Clicked: {selector}", "SUCCESS")
            
            # Give UI time to respond
            await asyncio.sleep(1)
            
            return {"status": "success", "selector": selector, "method": "selector"}
            
        except Exception as e:
            # Retry with force if normal click failed
            if not force:
                self._log("Normal click failed, trying force click...", "WARN")
                return await self._click_by_selector(page, selector, force=True)
            raise e
    
    async def _click_by_text(self, page: Page, text: str, force: bool) -> Dict[str, Any]:
        """Click using text content"""
        self._log(f"Clicking text: '{text}'")
        
        try:
            # Playwright's text selector
            locator = page.get_by_text(text, exact=False).first
            
            if force:
                await locator.click(force=True, timeout=3000)
            else:
                await locator.click(timeout=3000)
            
            self._log(f"Clicked: '{text}'", "SUCCESS")
            await asyncio.sleep(1)
            
            return {"status": "success", "text": text, "method": "text"}
            
        except Exception as e:
            if not force:
                return await self._click_by_text(page, text, force=True)
            raise e
    
    async def _click_by_agent_id(self, page: Page, element_id: int, force: bool) -> Dict[str, Any]:
        """Click using agent's DOM marker ID"""
        self._log(f"Clicking element ID: {element_id}")
        
        selector = f'[data-agent-id="{element_id}"]'
        return await self._click_by_selector(page, selector, force)
    
    def get_signature(self) -> Dict[str, Any]:
        return {
            "name": "smart_click",
            "description": "Click an element using robust fallback strategies",
            "arguments": {
                "selector": "str (optional) - CSS or Playwright selector",
                "text": "str (optional) - Text content to match",
                "element_id": "int (optional) - Agent's element ID",
                "force": "bool (optional) - Force click even if obscured"
            },
            "example": {
                "tool": "smart_click",
                "arguments": {"text": "Submit"}
            }
        }
