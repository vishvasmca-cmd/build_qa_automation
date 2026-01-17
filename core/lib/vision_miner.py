
import io
import time
from PIL import Image, ImageFilter, ImageOps, ImageDraw

class VisionMiner:
    """
    detects interactive elements purely from visual signals (pixels),
    ignoring the DOM code. Useful for verifying if an element is actually visible.
    """

    @staticmethod
    def detect_elements(image_bytes: bytes, min_area=100, max_area=100000):
        """
        Detects rectangular blobs in the image that look like buttons or inputs using OpenCV.
        """
        try:
            import cv2
            import numpy as np
            
            # Decode image
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                return {"success": False, "error": "Failed to decode image"}
                
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Edge Detection (Canny)
            edges = cv2.Canny(gray, 50, 150)
            
            # Dilate to connect broken edges of same element
            kernel = np.ones((3,3), np.uint8)
            dilated = cv2.dilate(edges, kernel, iterations=1)
            
            # Find Contours
            contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            elements = []
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                area = w * h
                
                if min_area < area < max_area:
                    # Aspect ratio check (buttons are usually wider than tall, inputs too)
                    aspect = w / float(h)
                    if 0.5 < aspect < 20: # Wide range to include icons and long bars
                        elements.append({
                            'x': x, 'y': y, 'width': w, 'height': h,
                            'area': area,
                            'type': 'detected_region'
                        })
            
            return {
                "success": True,
                "elements": elements,
                "count": len(elements)
            }

        except ImportError:
            return {"success": False, "error": "OpenCV not installed"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def verify_visibility(image_bytes: bytes, x, y, w, h):
        """
        Verifies if a specific region has content using OpenCV statistical analysis.
        """
        try:
            import cv2
            import numpy as np
            
            nparr = np.frombuffer(image_bytes, np.uint8)
            # Flag IMREAD_GRAYSCALE is faster
            img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
            
            if img is None:
               return {"is_visible": False, "error": "Decode failed"}
               
            # Crop
            # Ensure ROI is within bounds
            h_img, w_img = img.shape
            x = max(0, x); y = max(0, y)
            w = min(w, w_img - x); h = min(h, h_img - y)
            
            if w <= 0 or h <= 0:
                return {"is_visible": False, "reason": "Invalid ROI"}

            roi = img[y:y+h, x:x+w]
            
            # 1. Standard Deviation (Contrast)
            # Solid color bg = low std_dev. Text/Borders = high std_dev.
            mean, std_dev = cv2.meanStdDev(roi)
            std_val = std_dev[0][0]
            
            # 2. Edge Density
            edges = cv2.Canny(roi, 50, 150)
            edge_pixels = cv2.countNonZero(edges)
            density = edge_pixels / (w * h)
            
            # Thresholds
            # std_dev > 2.0 implies some contrast variation
            # density > 0.001 implies some edges
            is_visible = std_val > 2.0 and density > 0.001

            
            return {
                "is_visible": bool(is_visible),
                "contrast_score": float(std_val),
                "edge_density": float(density)
            }
            
        except ImportError:
            # Fallback to Pillow if CV2 missing (though we verified it exists)
            return {"is_visible": True, "note": "OpenCV missing, assuming visible"}
        except Exception as e:
            return {"is_visible": False, "error": str(e)}
