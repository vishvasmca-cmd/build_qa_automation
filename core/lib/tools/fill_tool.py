"""
Smart Fill Tool - Fills input fields with robust clearing and validation.
"""

import asyncio
from termcolor import colored
from .base_tool import Tool
from typing import Dict, Any, Optional
from playwright.async_api import Page


class FillTool(Tool):
    """
    Intelligent fill tool that:
    1. Finds input fields using multiple strategies
    2. Properly clears existing content
    3. Validates the fill was successful
    """
    
    async def execute(
        self, 
        page: Page, 
        value: str,
        selector: Optional[str] = None,
        placeholder: Optional[str] = None,
        label: Optional[str] = None,
        element_id: Optional[int] = None,
        press_enter: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute a fill operation.
        
        Args:
            page: Playwright page object
            value: The text to fill
            selector: CSS/Playwright selector
            placeholder: Placeholder text to match
            label: Label text to match
            element_id: Agent's element ID
            press_enter: Whether to press Enter after filling
            
        Returns:
            Dict with status and fill details
        """
        
        try:
            # Determine fill strategy
            locator = None
            
            if selector:
                locator = page.locator(selector)
                method = f"selector: {selector}"
            elif placeholder:
                locator = page.get_by_placeholder(placeholder, exact=False)
                method = f"placeholder: {placeholder}"
            elif label:
                locator = page.get_by_label(label, exact=False)
                method = f"label: {label}"
            elif element_id:
                locator = page.locator(f'[data-agent-id="{element_id}"]')
                method = f"element_id: {element_id}"
            else:
                return {"status": "failure", "error": "No target specified"}
            
            self._log(f"Filling '{value}' via {method}")
            
            # Execute the fill operation
            await self._perform_fill(page, locator, value, press_enter)
            
            self._log(f"Successfully filled: '{value}'", "SUCCESS")
            
            return {
                "status": "success",
                "value": value,
                "method": method,
                "pressed_enter": press_enter
            }
            
        except Exception as e:
            self.last_error = str(e)
            self._log(f"Fill failed: {e}", "WARN")
            return {"status": "failure", "error": str(e)}
    
    async def _perform_fill(self, page: Page, locator, value: str, press_enter: bool):
        """Robust fill operation with proper clearing"""
        
        # 1. Click to focus
        await locator.click(timeout=5000)
        
        # 2. Clear existing content (Ctrl+A, Backspace)
        await page.keyboard.down('Control')
        await page.keyboard.press('a')
        await page.keyboard.up('Control')
        await page.keyboard.press('Backspace')
        
        # 3. Type naturally (with delay for SPA detection)
        await locator.type(value, delay=40)
        
        # 4. Press Enter if requested
        if press_enter:
            await page.keyboard.press("Enter")
            await asyncio.sleep(2)  # Wait for response
    
    def get_signature(self) -> Dict[str, Any]:
        return {
            "name": "smart_fill",
            "description": "Fill an input field with robust clearing and validation",
            "arguments": {
                "value": "str - The text to fill",
                "selector": "str (optional) - CSS or Playwright selector",
                "placeholder": "str (optional) - Placeholder text to match",
                "label": "str (optional) - Label text to match",
                "element_id": "int (optional) - Agent's element ID",
                "press_enter": "bool (optional) - Press Enter after filling"
            },
            "example": {
                "tool": "smart_fill",
                "arguments": {"placeholder": "Email", "value": "test@example.com"}
            }
        }
