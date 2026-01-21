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
    # 1. Background Cleanup (Ads, Cookie Banners, Chat Widgets)
    await page.evaluate("""
        () => {
            const noise = [
                // Ads & Iframes
                'iframe[id*="google"]', 'iframe[src*="doubleclick"]',
                '.ad', '.ads', '.advertisement', 
                
                // Cookie Banners & GDPR
                '#cookies-banner', '[class*="cookie-banner"]', '#onetrust-banner-sdk', 
                '.osano-cm-window', '#usercentrics-root',
                
                // Popups & Overlays
                '.vignette', '.modal-backdrop', '[class*="popup"]', '[class*="overlay"]',
                
                // Chat Widgets
                '#intercom-container', '#drift-widget', '.crisp-client', 
                'iframe[id*="chat"]', '[class*="chat-widget"]',
                
                // Newsletter / Sticky Bars
                '[class*="newsletter"]', '[class*="sticky-footer"]', '[class*="fixed-bottom"]'
            ];
            document.querySelectorAll(noise.join(',')).forEach(el => {
                try { el.remove(); } catch(e) {}
            });
        }
    """)

    # 2. Extract DOM Elements and Sort by Visual Prominence
    try:
        res = await page.evaluate(DOM_EXTRACTION_SCRIPT, 0)
        raw_elements = res.get('elements', [])
        
        # VISUAL PROMINENCE ALGORITHM:
        # 1. Calculate screen center
        viewport = page.viewport_size or {"width": 1280, "height": 720}
        center_x, center_y = viewport["width"] / 2, viewport["height"] / 2
        
        def calculate_score(el):
            # Distance from center (lower is better)
            el_x = el.get("center", {}).get("x", center_x)
            el_y = el.get("center", {}).get("y", center_y)
            dist = ((el_x - center_x)**2 + (el_y - center_y)**2)**0.5
            
            # Size (larger is usually more important)
            width = el.get("rect", {}).get("width", 10)
            height = el.get("rect", {}).get("height", 10)
            area = width * height
            
            # Boost specific interactive roles
            role_boost = 1.0
            if el.get("tagName") in ["button", "input", "a", "select", "textarea"]:
                role_boost = 1.2
            if el.get("role") in ["button", "link", "textbox", "listbox"]:
                role_boost = 1.2
                
            # Final Score: Area / (Distance + 100) * Boost
            # (Adding 100 to distance prevents division by zero and flattens very close items)
            return (area / (dist + 100)) * role_boost

        # Sort descending by score
        elements = sorted(raw_elements, key=calculate_score, reverse=True)[:100]  # Increased limit to 100
        
    except Exception as e:
        print(f"   ΓÜá∩╕Å DOM Extraction failed: {e}")
        elements = []

    # 3. Optimized Vision capture
    screenshot_b64 = None
    try:
        # OPTIMIZED: Resize to max 1024px width to save tokens while keeping readability
        # Quality reduced to 40 (sufficient for UI text)
        # Type jpeg is efficient
        screenshot_bytes = await page.screenshot(
            type="jpeg", 
            quality=40, 
            scale="css" # Use 1:1 CSS pixels, avoiding huge Retina screenshots
        )
        
        # Optional: Resize if needed (requires PIL/Pillow, avoiding extra deps if possible for now)
        # Using scale="css" usually keeps it manageable (e.g. 1280x720)
        
        import base64
        screenshot_b64 = base64.b64encode(screenshot_bytes).decode('utf-8')
    except Exception as e:
        print(f"   ΓÜá∩╕Å Screenshot failed: {e}")

    return {
        "summary": {"title": await page.title(), "status": "active"},
        "elements": elements, 
        "screenshot": screenshot_b64,
        "url": url
    }

if __name__ == "__main__":
    # Internal test logic
    pass
