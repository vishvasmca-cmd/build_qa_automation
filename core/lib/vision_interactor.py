import asyncio
import os
import re
import datetime
import cv2
import numpy as np
from termcolor import colored
from typing import Optional, Tuple, Dict, Any

class VisionInteractor:
    """
    Uses OCR and Computer Vision to interact with elements when DOM is inaccessible.
    """
    def __init__(self, page):
        self.page = page
        self.ocr_available = False
        try:
            import pytesseract
            self.pytesseract = pytesseract
            # Configure path for Windows
            tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            if os.path.exists(tesseract_path):
                self.pytesseract.pytesseract.tesseract_cmd = tesseract_path
                self.ocr_available = True
                print(colored(f"✅ [VisionInteractor] Tesseract found at {tesseract_path}", "green"))
        except ImportError:
            print(colored("⚠️ [VisionInteractor] pytesseract not installed", "yellow"))

    async def find_input_by_label(self, label_text: str) -> Optional[Tuple[int, int]]:
        """Finds an input field visually based on its label text."""
        if not self.ocr_available: return None
        
        try:
            print(colored(f"   🔍 [VisionOCR] Searching for input field: '{label_text}'", "cyan"))
            screenshot = await self.page.screenshot(type="png")
            img = cv2.imdecode(np.frombuffer(screenshot, np.uint8), cv2.IMREAD_COLOR)
            
            # --- IMPROVED PREPROCESSING ---
            scale_factor = 2
            h, w = img.shape[:2]
            scaled = cv2.resize(img, (w*scale_factor, h*scale_factor), interpolation=cv2.INTER_CUBIC)
            gray = cv2.cvtColor(scaled, cv2.COLOR_BGR2GRAY)
            # Use Otsu's thresholding for optimal binarization
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # OCR Data with bounding boxes
            data = self.pytesseract.image_to_data(thresh, output_type=self.pytesseract.Output.DICT)
            
            found_label = False
            label_x, label_y, label_w, label_h = 0, 0, 0, 0
            label_text_lower = label_text.lower().strip()
            clean_target = re.sub(r'[^a-z0-9]', '', label_text_lower)

            # --- FUZZY MATCHING & STITCHING ---
            tokens = []
            all_tokens_debug = []
            for i in range(len(data['text'])):
                txt = data['text'][i].strip().lower()
                if txt:
                    tokens.append({
                        'text': txt,
                        'x': data['left'][i] // scale_factor,
                        'y': data['top'][i] // scale_factor,
                        'w': data['width'][i] // scale_factor,
                        'h': data['height'][i] // scale_factor
                    })
                    all_tokens_debug.append(txt)

            for i in range(len(tokens)):
                # 1. Direct fuzzy match
                clean_token = re.sub(r'[^a-z0-9]', '', tokens[i]['text'])
                if clean_target == clean_token or clean_target in clean_token:
                    label_x, label_y, label_w, label_h = tokens[i]['x'], tokens[i]['y'], tokens[i]['w'], tokens[i]['h']
                    found_label = True
                    print(colored(f"      ✓ Found fuzzy label '{tokens[i]['text']}' at ({label_x}, {label_y})", "grey"))
                    break
                
                # 2. Horizontal stitching
                combined = tokens[i]['text']
                curr_w = tokens[i]['w']
                for j in range(i+1, min(i+4, len(tokens))):
                    dist = tokens[j]['x'] - (tokens[i]['x'] + curr_w)
                    v_diff = abs(tokens[j]['y'] - tokens[i]['y'])
                    if dist < 30 and v_diff < 15:
                        combined += tokens[j]['text']
                        curr_w = tokens[j]['x'] + tokens[j]['w'] - tokens[i]['x']
                        clean_combined = re.sub(r'[^a-z0-9]', '', combined)
                        if clean_target in clean_combined:
                            label_x, label_y, label_w, label_h = tokens[i]['x'], tokens[i]['y'], curr_w, tokens[i]['h']
                            found_label = True
                            print(colored(f"      ✓ Stitched label '{combined}' found at ({label_x}, {label_y})", "grey"))
                            break
                if found_label: break

            if not found_label:
                print(colored(f"      ❌ Label '{label_text}' not found. Tokens: {all_tokens_debug[:15]}...", "yellow"))
                return None

            # --- HYBRID FIELD DISCOVERY ---
            gray_orig = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray_orig, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            search_area = {
                'x_min': label_x - 50,
                'x_max': label_x + label_w + 300,
                'y_min': label_y - 20,
                'y_max': label_y + 150
            }
            
            best_field = None
            min_dist = 99999
            
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                if 80 < w < 600 and 20 < h < 100: # Typical input field size
                    if search_area['x_min'] < x < search_area['x_max'] and search_area['y_min'] < y < search_area['y_max']:
                        dist = abs(y - (label_y + label_h//2))
                        if dist < min_dist:
                            min_dist = dist
                            best_field = (x + w//2, y + h//2)
            
            def save_debug(tx, ty, tlabel):
                try:
                    debug_img = img.copy()
                    cv2.circle(debug_img, (tx, ty), 12, (0, 0, 255), 3)
                    cv2.putText(debug_img, tlabel, (tx+15, ty), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.imwrite(f"vision_debug_{datetime.datetime.now().strftime('%H%M%S')}.png", debug_img)
                except: pass

            if best_field:
                print(colored(f"      ✅ Found input field at {best_field}", "green"))
                save_debug(best_field[0], best_field[1], label_text)
                return best_field
                
            # Fallback
            fx, fy = label_x + label_w//2, label_y + label_h + 35
            print(colored(f"      ⚠️ No border found. Using offset ({fx}, {fy})", "yellow"))
            save_debug(fx, fy, f"{label_text} (Fallback)")
            return (fx, fy)
            
        except Exception as e:
            print(colored(f"   ❌ Vision search error: {e}", "red"))
            return None

    async def click_button_by_text(self, text: str) -> bool:
        """Finds and clicks a button visually by its text."""
        if not self.ocr_available: return False
        try:
            print(colored(f"   🔍 [VisionOCR] Searching for button: '{text}'", "cyan"))
            screenshot = await self.page.screenshot(type="png")
            img = cv2.imdecode(np.frombuffer(screenshot, np.uint8), cv2.IMREAD_COLOR)
            
            scale = 2
            scaled = cv2.resize(img, (img.shape[1]*scale, img.shape[0]*scale), interpolation=cv2.INTER_CUBIC)
            gray = cv2.cvtColor(scaled, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            data = self.pytesseract.image_to_data(thresh, output_type=self.pytesseract.Output.DICT)
            
            target = text.lower().strip()
            for i in range(len(data['text'])):
                if target in data['text'][i].lower():
                    x = (data['left'][i] + data['width'][i]//2) // scale
                    y = (data['top'][i] + data['height'][i]//2) // scale
                    await self.page.mouse.click(x, y)
                    print(colored(f"      ✅ Clicked button '{text}' at ({x}, {y})", "green"))
                    return True
            return False
        except Exception as e:
            print(colored(f"   ❌ Button Vision error: {e}", "red"))
            return False
