"""
Visual Locator - Template matching for element location without LLM
Uses OpenCV to find elements visually when CSS/text selectors fail
"""

import cv2
import numpy as np
import os
from typing import Optional, Dict, Any, Tuple
from termcolor import colored


class VisualLocator:
    """
    Fast visual element matching using OpenCV template matching.
    Provides fallback element location when CSS/text selectors fail.
    """
    
    def __init__(self, confidence_threshold: float = 0.8):
        """
        Initialize visual locator.
        
        Args:
            confidence_threshold: Minimum match confidence (0-1) to accept a match
        """
        self.confidence_threshold = confidence_threshold
        
    def find_element(
        self, 
        screenshot_path: str, 
        template_path: str,
        scale_range: Tuple[float, float] = (0.8, 1.2)
    ) -> Optional[Dict[str, Any]]:
        """
        Find an element in a screenshot using template matching.
        
        Args:
            screenshot_path: Path to full page screenshot
            template_path: Path to element template image
            scale_range: Min/max scale factors to try (for responsive layouts)
            
        Returns:
            Dict with bounding box and confidence, or None if not found
        """
        
        if not os.path.exists(screenshot_path):
            print(colored(f"⚠️ Screenshot not found: {screenshot_path}", "yellow"))
            return None
            
        if not os.path.exists(template_path):
            print(colored(f"⚠️ Template not found: {template_path}", "yellow"))
            return None
        
        try:
            # Load images
            screenshot = cv2.imread(screenshot_path)
            template = cv2.imread(template_path)
            
            if screenshot is None or template is None:
                return None
                
            # Convert to grayscale for better matching
            screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            
            template_h, template_w = template_gray.shape
            
            best_match = None
            best_confidence = 0
            
            # Try multiple scales (handles responsive design changes)
            for scale in np.linspace(scale_range[0], scale_range[1], 5):
                # Resize template
                new_w = int(template_w * scale)
                new_h = int(template_h * scale)
                
                if new_w <= 0 or new_h <= 0:
                    continue
                    
                resized_template = cv2.resize(template_gray, (new_w, new_h))
                
                # Skip if template is larger than screenshot
                if resized_template.shape[0] > screenshot_gray.shape[0] or \
                   resized_template.shape[1] > screenshot_gray.shape[1]:
                    continue
                
                # Perform template matching
                result = cv2.matchTemplate(
                    screenshot_gray, 
                    resized_template, 
                    cv2.TM_CCOEFF_NORMED
                )
                
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                
                if max_val > best_confidence:
                    best_confidence = max_val
                    best_match = {
                        'x': int(max_loc[0] + new_w / 2),  # Center X
                        'y': int(max_loc[1] + new_h / 2),  # Center Y
                        'width': new_w,
                        'height': new_h,
                        'confidence': float(max_val),
                        'scale': scale
                    }
            
            if best_match and best_confidence >= self.confidence_threshold:
                print(colored(
                    f"✅ Visual match found: confidence={best_confidence:.2f}, "
                    f"position=({best_match['x']}, {best_match['y']})",
                    "green"
                ))
                return best_match
            else:
                print(colored(
                    f"❌ No confident match (best: {best_confidence:.2f} < {self.confidence_threshold})",
                    "yellow"
                ))
                return None
                
        except Exception as e:
            print(colored(f"⚠️ Visual locator error: {e}", "red"))
            return None
    
    def extract_element_template(
        self,
        screenshot: np.ndarray,
        bounding_box: Dict[str, int],
        output_path: str
    ) -> bool:
        """
        Extract and save an element's visual template from a screenshot.
        
        Args:
            screenshot: Full page screenshot as numpy array
            bounding_box: Dict with x, y, width, height
            output_path: Where to save the template image
            
        Returns:
            True if successful, False otherwise
        """
        try:
            x = bounding_box['x']
            y = bounding_box['y']
            w = bounding_box['width']
            h = bounding_box['height']
            
            # Ensure coordinates are within bounds
            img_h, img_w = screenshot.shape[:2]
            x = max(0, min(x, img_w - 1))
            y = max(0, min(y, img_h - 1))
            w = min(w, img_w - x)
            h = min(h, img_h - y)
            
            if w <= 0 or h <= 0:
                return False
            
            # Crop element
            template = screenshot[y:y+h, x:x+w]
            
            # Create output directory if needed
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save template
            cv2.imwrite(output_path, template)
            return True
            
        except Exception as e:
            print(colored(f"⚠️ Failed to extract template: {e}", "red"))
            return False
