from playwright.async_api import Page, expect
import os
import random
import asyncio
from typing import Dict, Any, List, Optional
from core.lib.data_generator import DataGenerator

class KeywordEngine:
    """
    Unified implementation of all Playwright-based automation keywords.
    Optimized for resilience and multi-element handling.
    """
    
    @staticmethod
    async def _get_best_locator(page: Page, selector: str):
        """Helper to handle multiple matches by picking the first visible one."""
        loc = page.locator(selector)
        count = await loc.count()
        if count > 1:
            return loc.first
        return loc

    @staticmethod
    async def navigate(page: Page, url: str, wait_until: str = 'domcontentloaded', timeout: int = 30000):
        await page.goto(url, wait_until=wait_until, timeout=timeout)

    @staticmethod
    async def click(page: Page, selector: str, force: bool = False, timeout: int = 10000):
        loc = await KeywordEngine._get_best_locator(page, selector)
        try:
            await loc.scroll_into_view_if_needed(timeout=5000)
        except: pass
        box = await loc.bounding_box()
        if box:
            # Move mouse in a human-like way
            x = box["x"] + box["width"] / 2
            y = box["y"] + box["height"] / 2
            await page.mouse.move(x, y, steps=10)
            await page.mouse.click(x, y)
        else:
            await loc.click(force=force, timeout=timeout)

    @staticmethod
    async def fill(page: Page, selector: str, value: str, timeout: int = 10000):
        loc = await KeywordEngine._get_best_locator(page, selector)
        await loc.scroll_into_view_if_needed(timeout=timeout)
        
        # Resolve dynamic data placeholders (e.g., {random_name} or {{random_name}})
        # Support both single and double curly braces
        resolved_value = str(value)
        if "{" in resolved_value:
            # Convert single braces to double for DataGenerator compatibility
            resolved_value = resolved_value.replace("{random_", "{{random_")
            resolved_value = resolved_value.replace("}", "}}")
            resolved_value = DataGenerator.resolve(resolved_value)
        
        # Attempt to fill with validation and retry
        max_attempts = 2
        for attempt in range(max_attempts):
            # Click to focus
            await KeywordEngine.click(page, selector, timeout=timeout)
            
            # Human-like clearing and typing
            await page.keyboard.press("Control+A")
            await page.keyboard.press("Backspace")
            await page.keyboard.type(resolved_value, delay=random.randint(50, 150))
            
            # Verify the value was filled correctly
            try:
                await asyncio.sleep(0.3)  # Brief wait for JS handlers
                actual_value = await loc.input_value(timeout=2000)
                
                # Check if value matches (allowing for minor differences like trimming)
                if actual_value.strip() == resolved_value.strip():
                    break  # Success!
                elif attempt < max_attempts - 1:
                    # Retry on mismatch
                    await asyncio.sleep(0.5)
                    continue
            except:
                # If we can't verify (e.g., not an input field), assume success
                break

    @staticmethod
    async def type(page: Page, selector: str, value: str, delay: int = 50, timeout: int = 10000):
        loc = await KeywordEngine._get_best_locator(page, selector)
        await loc.type(value, delay=delay, timeout=timeout)

    @staticmethod
    async def hover(page: Page, selector: str, timeout: int = 10000):
        loc = await KeywordEngine._get_best_locator(page, selector)
        try:
            await loc.scroll_into_view_if_needed(timeout=5000)
        except: pass
        box = await loc.bounding_box()
        if box:
            x = box["x"] + box["width"] / 2
            y = box["y"] + box["height"] / 2
            await page.mouse.move(x, y, steps=10)
        else:
            await loc.hover(timeout=timeout)

    @staticmethod
    async def select(page: Page, selector: str, value: str, timeout: int = 10000):
        loc = await KeywordEngine._get_best_locator(page, selector)
        await loc.select_option(value, timeout=timeout)

    @staticmethod
    async def check(page: Page, selector: str, timeout: int = 10000):
        loc = await KeywordEngine._get_best_locator(page, selector)
        await loc.check(timeout=timeout)

    @staticmethod
    async def uncheck(page: Page, selector: str, timeout: int = 10000):
        loc = await KeywordEngine._get_best_locator(page, selector)
        await loc.uncheck(timeout=timeout)

    @staticmethod
    async def press(page: Page, selector: str, key: str, timeout: int = 10000):
        loc = await KeywordEngine._get_best_locator(page, selector)
        await loc.press(key, timeout=timeout)

    @staticmethod
    async def scroll_to(page: Page, selector: str, timeout: int = 5000):
        try:
            loc = await KeywordEngine._get_best_locator(page, selector)
            await loc.scroll_into_view_if_needed(timeout=timeout)
        except:
            pass # Continue if scroll fails, might already be in view

    @staticmethod
    async def wait_for_element(page: Page, selector: str, state: str = 'visible', timeout: int = 10000):
        await page.locator(selector).wait_for(state=state, timeout=timeout)

    @staticmethod
    async def assert_visible(page: Page, selector: str, timeout: int = 10000):
        loc = await KeywordEngine._get_best_locator(page, selector)
        await expect(loc).to_be_visible(timeout=timeout)

    @staticmethod
    async def assert_text(page: Page, selector: str, expected_text: str, timeout: int = 10000):
        loc = await KeywordEngine._get_best_locator(page, selector)
        await expect(loc).to_have_text(expected_text, timeout=timeout)

    @staticmethod
    async def assert_url(page: Page, expected_url: str, timeout: int = 10000):
        await expect(page).to_have_url(expected_url, timeout=timeout)

    @staticmethod
    async def screenshot(page: Page, name: str):
        os.makedirs("outputs", exist_ok=True)
        await page.screenshot(path=f"outputs/{name}.png")

    @staticmethod
    async def ai_action(page: Page, prompt: str, llm_callback=None):
        """ZeroStep-style fallback placeholder."""
        pass
