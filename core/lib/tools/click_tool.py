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
        coordinates: Optional[Dict[str, int]] = None,
        force: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute a click operation with multi-stage fallback.
        
        Args:
            page: Playwright page object
            selector: CSS/Playwright selector (priority 1)
            text: Text content to match (priority 2)
            element_id: Agent's element ID from DOM marker (priority 3)
            coordinates: {'x': int, 'y': int} for coordinate click (final fallback)
            force: Force click even if obscured
            
        Returns:
            Dict with status and click details
        """
        
        try:
            # Stage 1: Smart Selector/Text/ID Click
            if selector:
                result = await self._click_by_selector(page, selector, force)
                if result["status"] == "success": return result
            
            if text:
                result = await self._click_by_text(page, text, force)
                if result["status"] == "success": return result
                
            if element_id:
                result = await self._click_by_agent_id(page, element_id, force)
                if result["status"] == "success": return result

            # Stage 2: Coordinate Fallback (Precision Vision Mode)
            if coordinates and 'x' in coordinates and 'y' in coordinates:
                return await self._click_by_coordinates(page, coordinates['x'], coordinates['y'])
            
            # Stage 3: Attempt Coordinate fallback from target_el if provided in kwargs
            # (passed by Explorer from its own mindmap)
            target_el = kwargs.get('target_el')
            if target_el and target_el.get('center'):
                cx, cy = target_el['center']['x'], target_el['center']['y']
                return await self._click_by_coordinates(page, cx, cy)

            # Stage 4: Nuclear JS Dispatch (Bypasses overlays/visibility)
            if selector or element_id:
                target_sel = selector or f'[data-agent-id="{element_id}"]'
                result = await self._click_by_js_event(page, target_sel)
                if result["status"] == "success": return result

            return {"status": "failure", "error": "All {strategies} click strategies exhausted (including Coordinate and JS fallbacks)"}
                
        except Exception as e:
            self.last_error = str(e)
            self._log(f"Global click exception: {e}", "WARN")
            return {"status": "failure", "error": str(e)}
    
    async def _click_by_selector(self, page: Page, selector: str, force: bool) -> Dict[str, Any]:
        """Click using CSS/Playwright selector with JS and Force fallbacks"""
        self._log(f"Attempting Selector Click: {selector}")
        
        try:
            # 1. Standard Playwright Click with .first to handle multiple matches
            await page.locator(selector).first.wait_for(timeout=3000, state="visible")
            await page.locator(selector).first.click(timeout=3000, force=force)
            return {"status": "success", "method": "playwright_selector"}
        except Exception as e:
            self._log(f"Standard click failed: {str(e)[:50]}...", "WARN")
            
            # 2. JavaScript Click (Bypasses many overlays/strict checks)
            try:
                self._log("Attempting JavaScript Fallback Click...")
                await page.locator(selector).first.evaluate("el => el.click()")
                return {"status": "success", "method": "javascript_eval"}
            except:
                # 3. Last resort for selectors: Force click
                if not force:
                    try:
                        self._log("Attempting Force Click...")
                        await page.locator(selector).first.click(force=True, timeout=2000)
                        return {"status": "success", "method": "force_click"}
                    except: pass
        
        return {"status": "failure", "error": f"Selector click failed: {str(e)}"}

    async def _click_by_text(self, page: Page, text: str, force: bool) -> Dict[str, Any]:
        """Click using text content with robust matching"""
        self._log(f"Attempting Text Click: '{text}'")
        try:
            locator = page.get_by_text(text, exact=False).first
            await locator.click(timeout=3000, force=force)
            return {"status": "success", "method": "playwright_text"}
        except:
             # Try partial match or regex if exact failed
             try:
                 await page.locator(f"text='{text}'").first.click(timeout=2000)
                 return {"status": "success", "method": "legacy_text"}
             except: pass
        return {"status": "failure", "error": "Text click failed"}

    async def _click_by_coordinates(self, page: Page, x: int, y: int) -> Dict[str, Any]:
        """The 'Vision Truth' Click - bypasses DOM altogether"""
        self._log(f"🎯 VISION FALLBACK: Clicking coordinates ({x}, {y})")
        try:
            # Move mouse first (looks more human, triggers hover effects)
            await page.mouse.move(x, y, steps=5)
            await asyncio.sleep(0.1)
            await page.mouse.click(x, y)
            return {"status": "success", "method": "coordinate_precision"}
        except Exception as e:
            return {"status": "failure", "error": f"Coordinate click failed: {e}"}

    async def _click_by_agent_id(self, page: Page, element_id: int, force: bool) -> Dict[str, Any]:
        """Click using agent's internal DOM marker"""
        selector = f'[data-agent-id="{element_id}"]'
        return await self._click_by_selector(page, selector, force)
    
    async def _click_by_js_event(self, page: Page, selector: str) -> Dict[str, Any]:
        """Nuclear Fallback: Dispatches a raw JS MouseEvent to the element (Shadow DOM Aware)."""
        self._log(f"☢️ NUCLEAR FALLBACK: Dispatching JS click event to {selector}")
        try:
            success = await page.evaluate(f"""
                (sel) => {{
                    const findInShadow = (root, selector) => {{
                        const el = root.querySelector(selector);
                        if (el) return el;
                        const all = root.querySelectorAll('*');
                        for (let item of all) {{
                            if (item.shadowRoot) {{
                                const found = findInShadow(item.shadowRoot, selector);
                                if (found) return found;
                            }}
                        }}
                        return null;
                    }};
                    
                    const el = findInShadow(document, sel);
                    if (el) {{
                        el.scrollIntoView({{behavior: 'smooth', block: 'center'}});
                        el.dispatchEvent(new MouseEvent('click', {{
                            bubbles: true,
                            cancelable: true,
                            view: window
                        }}));
                        return true;
                    }}
                    return false;
                }}
            """, selector)
            if success:
                return {"status": "success", "method": "js_dispatch_event_shadow"}
        except Exception as e:
            self._log(f"JS Dispatch failed: {e}", "WARN")
        return {"status": "failure", "error": "JS Dispatch failed"}

    def get_signature(self) -> Dict[str, Any]:
        return {
            "name": "smart_click",
            "description": "Click an element using multi-stage fallback (Selector -> text -> ID -> JS -> Coordinates)",
            "arguments": {
                "selector": "str (optional) - CSS/Playwright selector",
                "text": "str (optional) - Text content",
                "element_id": "int (optional) - Agent element ID",
                "coordinates": "dict (optional) - {'x': int, 'y': int}",
                "force": "bool (optional) - Force click"
            },
            "example": {
                "tool": "smart_click",
                "arguments": {"selector": "#submit", "coordinates": {"x": 500, "y": 300}}
            }
        }
