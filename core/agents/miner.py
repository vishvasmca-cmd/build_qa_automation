import asyncio
import json
import os
import sys
from typing import Dict, Any, List
from playwright.async_api import Page
from termcolor import colored


# Add project root to path

# Add project root to path
sys.path.append(os.getcwd())

from core.lib.dom_driver import DOM_EXTRACTION_SCRIPT

async def analyze_page(page: Page, url: str, user_goal: str = None) -> Dict:
    """
    Hybrid mining: DOM + Vision (Optimized).
    """
    # 1. Background Cleanup (Ads, Cookie Banners)
    await page.evaluate("""
        () => {
            const noise = [
                'iframe[id*="google"]', 'iframe[src*="doubleclick"]',
                '.ad', '.ads', '.advertisement', '#cookies-banner', 
                '[class*="cookie-banner"]', '.vignette'
            ];
            document.querySelectorAll(noise.join(',')).forEach(el => {
                try { el.remove(); } catch(e) {}
            });
        }
    """)

    # 2. Extract DOM Elements (Reduced set for context)
    try:
        res = await page.evaluate(DOM_EXTRACTION_SCRIPT, 0)
        elements = res.get('elements', [])[:60] # Increased for better CSS matching
    except Exception:
        elements = []

    # 3. Optimized Vision capture
    screenshot_b64 = None
    try:
        # Lower resolution and quality to save tokens/cost
        screenshot_bytes = await page.screenshot(
            type="jpeg", 
            quality=50, 
            scale="device" 
        )
        import base64
        screenshot_b64 = base64.b64encode(screenshot_bytes).decode('utf-8')
    except Exception as e:
        print(f"   ⚠️ Screenshot failed: {e}")

    return {
        "summary": {"title": await page.title(), "status": "active"},
        "elements": elements, # Limited DOM for semantic hints
        "screenshot": screenshot_b64,
        "url": url
    }

if __name__ == "__main__":
    # Internal test logic
    pass
