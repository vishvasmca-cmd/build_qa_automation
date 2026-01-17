from .base_tool import Tool
from playwright.async_api import Page
from termcolor import colored

class VerifyTool(Tool):
    """
    Tool for verifying the presence of text or elements on the page without interacting.
    Useful for confirmation steps (e.g., "Verify 'Success' message appears").
    """
    
    def get_signature(self) -> dict:
        return {
            "description": "Verifies that specific text exists on the page. Use this for confirmation steps.",
            "arguments": {
                "text": "The text string to look for (case-insensitive)",
                "exact": "Boolean, whether to match exact text (default: False)"
            },
            "example": {
                "text": "Product added",
                "exact": False
            }
        }
    
    async def execute(self, page: Page, text: str, exact: bool = False, **kwargs) -> dict:
        print(colored(f"📋 [VerifyTool] checking for text: '{text}'...", "cyan"))
        
        try:
            # 1. Wait for content to be loosely visible
            # We use a broad timeout (10s) to allow for animations
            # 1. Search for all matches and find the first visible one
            locators = page.get_by_text(text, exact=exact)
            count = await locators.count()
            
            target_locator = None
            is_visible = False
            
            # Iterate to find the first visible instance
            for i in range(count):
                cand = locators.nth(i)
                try:
                    if await cand.is_visible():
                        target_locator = cand
                        is_visible = True
                        break
                except: pass
            
            # If none currently visible, fall back to waiting on the first one (standard behavior)
            if not target_locator and count > 0:
                target_locator = locators.first
                try:
                     await target_locator.wait_for(state="visible", timeout=10000)
                     is_visible = True
                except: is_visible = False
            
            locator = target_locator if target_locator else (locators.first if count > 0 else None)
            
            if is_visible and locator:
                # Highlight if headed
                try:
                    await locator.evaluate("el => { el.style.border = '4px solid #00FF00'; el.style.backgroundColor = 'rgba(0, 255, 0, 0.2)'; }")
                    await page.wait_for_timeout(500)
                except: pass
                
                return {
                    "status": "success",
                    "output": f"Verified: '{text}' is visible on the page."
                }
            else:
                # Fallback: Check page source if not strictly visible (sometimes text is there but hidden by CSS)
                content = await page.content()
                if text.lower() in content.lower():
                     print(colored(f"   ⚠️ Text found in DOM but not strictly visible.", "yellow"))
                     return {
                        "status": "success",
                        "output": f"Verified: '{text}' found in page source (though not fully visible)."
                    }
                
                return {
                    "status": "failure",
                    "error": f"Text '{text}' not found on the page."
                }
                
        except Exception as e:
            return {
                "status": "failure",
                "error": f"Verification failed: {str(e)}"
            }
