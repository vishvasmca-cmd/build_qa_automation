
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
        Detects rectangular blobs in the image that look like buttons or inputs.
        Returns a list of bounding boxes: {'x', 'y', 'width', 'height', 'type'}
        """
        start_time = time.time()
        
        try:
            # 1. Load Image
            img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            width, height = img.size
            
            # 2. Preprocessing for Edge Detection
            # Convert to grayscale
            gray = img.convert("L")
            
            # Find Edges (Gradient)
            edges = gray.filter(ImageFilter.FIND_EDGES)
            
            # Threshold to get strong edges (High Contrast)
            # This creates a binary image where edges are white
            binary = edges.point(lambda p: 255 if p > 30 else 0)
            
            # REMOVED: Inverting. We want white edges on black background for bounding box logic usually,
            # but Pillow's getbbox works on non-zero pixels.
            
            # 3. Simple Contour / Blob Detection Simulation
            # Since Pillow doesn't have cv2.findContours, we can use a heuristic:
            # - Divide image into grid or use floodfill? 
            # - actually, a better pillow-only approach for "boxes" is hard without OpenCV.
            # - Let's use a simpler heuristic: High Contrast Regions.
            
            # ALTERNATIVE: Use ImageOps.colorize or look for solid color blocks?
            # A robust "button detector" without OpenCV is tricky.
            # Let's try a "Contrast Scanner"
            
            detected = []
            
            # Heuristic: Scan for rectangular regions of high contrast
            # For a production system without OpenCV, we might just look for distinct colors.
            # verification_targets = []
            
            # For now, let's implement a 'mock' detector that assumes 
            # if we see a high-contrast rect, it's an element.
            # But accurately getting the box coordinates purely with Pillow is computationally heavy in python loops.
            
            # FALLBACK: If we can't use OpenCV, we can use the 'edges' image to validate existing DOM elements.
            # This is safer than trying to 'discover' them from scratch with slow python loops.
            
            return {
                "success": True,
                "elements": [], # TODO: Requires OpenCV for efficient contour detection
                "message": "Pure Pillow detection is limited. Please install opencv-python for full bounding-box detection."
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def verify_visibility(image_bytes: bytes, x, y, w, h):
        """
        Verifies if a specific region has content (edges/contrast) vs being flat (invisible/white-on-white).
        """
        try:
            img = Image.open(io.BytesIO(image_bytes)).convert("L")
            crop = img.crop((x, y, x+w, y+h))
            
            # Calculate standard deviation of pixel intensity
            # Flat regions (invisible) will have low std dev.
            # Text/Buttons will have high std dev.
            stat = ImageOps.grayscale(crop).getextrema()
            # This is range, lets get variance.
            
            import math
            pixels = list(crop.getdata())
            avg = sum(pixels) / len(pixels)
            variance = sum([((x - avg) ** 2) for x in pixels]) / len(pixels)
            std_dev = math.sqrt(variance)
            
            return {
                "is_visible": std_dev > 5.0, # Threshold for "something is there"
                "contrast_score": std_dev
            }
            
        except Exception as e:
            return {"is_visible": False, "error": str(e)}
