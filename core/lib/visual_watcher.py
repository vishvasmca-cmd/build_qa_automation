import asyncio
import cv2
import numpy as np
from termcolor import colored
from playwright.async_api import Page
import time

class VisualWatcher:
    """
    Monitors visual changes on the page to detect animations, modals, and overlays.
    """
    def __init__(self, page: Page):
        self.page = page
        self.last_frame = None
        self.last_change_percent = 0.0
        self.stable_frames = 0
        self.is_monitoring = False
        
    def get_last_change_percent(self):
        return self.last_change_percent
        
    async def wait_for_visual_stability(self, timeout_ms=5000, check_interval_ms=500):
        """Waits until the page stops changing (e.g. modal animation finished)."""
        print(colored("   ⏳ [VisualWatcher] Waiting for visual stability...", "cyan"))
        start_time = time.time()
        consecutive_stable_frames = 0
        
        while (time.time() - start_time) * 1000 < timeout_ms:
            screenshot = await self.page.screenshot(type="jpeg", quality=50)
            frame = cv2.imdecode(np.frombuffer(screenshot, np.uint8), cv2.IMREAD_GRAYSCALE)
            
            if self.last_frame is not None:
                # Resize to common small size for fast comparison
                f1 = cv2.resize(self.last_frame, (320, 180))
                f2 = cv2.resize(frame, (320, 180))
                
                diff = cv2.absdiff(f1, f2)
                change = np.count_nonzero(diff > 25) / (320 * 180)
                self.last_change_percent = change
                
                if change < 0.01: # Less than 1% change
                    consecutive_stable_frames += 1
                    print(colored(f"      ✓ Stable frame {consecutive_stable_frames}/3 ({change*100:.1f}%)", "grey"))
                    if consecutive_stable_frames >= 3:
                        return True
                else:
                    consecutive_stable_frames = 0
                    print(colored(f"      ⏳ Still changing ({change*100:.1f}%)...", "grey"))
            
            self.last_frame = frame
            await asyncio.sleep(check_interval_ms / 1000)
            
        return False

    def is_overlay_present(self) -> bool:
        """Heuristic check for modal/overlay based on the last frame."""
        if self.last_frame is None: return False
        
        # Check for darker/dimmed background (common for modals)
        avg_brightness = np.mean(self.last_frame)
        # If the page changed significantly (>80%) and is relatively dark/uniform, likely a modal
        if self.last_change_percent > 0.8:
            return True
        return False

    async def dismiss_by_vision(self) -> bool:
        """Minimal visual dismissal logic."""
        try:
            print(colored("   🎯 [VisualWatcher] Attempting visual dismissal...", "cyan"))
            await self.page.keyboard.press("Escape")
            await asyncio.sleep(0.5)
            return True
        except: return False
