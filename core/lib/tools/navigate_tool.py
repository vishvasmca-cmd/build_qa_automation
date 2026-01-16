"""
Navigation Tool - Handles page navigation and URL loading.
"""

import asyncio
from termcolor import colored
from .base_tool import Tool
from typing import Dict, Any
from playwright.async_api import Page


class NavigateTool(Tool):
    """
    Navigation tool for loading pages and handling redirects.
    """
    
    async def execute(
        self, 
        page: Page, 
        url: str,
        wait_until: str = "domcontentloaded",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Navigate to a URL.
        
        Args:
            page: Playwright page object
            url: Target URL
            wait_until: Wait strategy ('load', 'domcontentloaded', 'networkidle')
            
        Returns:
            Dict with status and navigation details
        """
        
        self._log(f"Navigating to: {url}")
        
        try:
            response = await page.goto(url, wait_until=wait_until, timeout=30000)
            
            if response and response.ok:
                self._log(f"Successfully navigated to {url}", "SUCCESS")
                return {
                    "status": "success",
                    "url": url,
                    "final_url": page.url,
                    "status_code": response.status
                }
            else:
                status = response.status if response else "unknown"
                return {
                    "status": "failure",
                    "error": f"Navigation failed with status {status}"
                }
                
        except Exception as e:
            # Fallback: If networkidle failed, try domcontentloaded
            if "Timeout" in str(e) and wait_until == "networkidle":
                 self._log(f"Navigation timed out on networkidle. Retrying with domcontentloaded...", "WARN")
                 try:
                     response = await page.goto(url, wait_until="domcontentloaded", timeout=15000)
                     if response and response.ok:
                        self._log(f"Fallback navigation succeeded to {url}", "SUCCESS")
                        return {
                            "status": "success",
                            "url": url,
                            "final_url": page.url,
                            "status_code": response.status
                        }
                 except: pass # Ignore fallback failure

            self.last_error = str(e)
            self._log(f"Navigation failed: {e}", "WARN")
            return {"status": "failure", "error": str(e)}
    
    def get_signature(self) -> Dict[str, Any]:
        return {
            "name": "navigate_to",
            "description": "Navigate to a specific URL",
            "arguments": {
                "url": "str - Target URL",
                "wait_until": "str (optional) - Wait strategy (default: 'networkidle')"
            },
            "example": {
                "tool": "navigate_to",
                "arguments": {"url": "https://example.com"}
            }
        }
