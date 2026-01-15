
import io
import math
from PIL import Image, ImageChops, ImageStat

class VisualVerifier:
    """
    Provides local, non-LLM visual verification using Pillow.
    Calculates pixel differences to determine if an action had a visual effect.
    """
    
    @staticmethod
    def get_visual_diff(before_bytes: bytes, after_bytes: bytes) -> dict:
        """
        Compares two screenshots and returns quantitative difference metrics.
        Returns:
            dict: {
                "score": float (0.0 to 100.0), -- Percentage of pixels changed
                "changed": bool, -- True if score > threshold
                "reason": str
            }
        """
        if not before_bytes or not after_bytes:
            return {"score": 0.0, "changed": False, "reason": "Missing screenshot data"}

        try:
            img1 = Image.open(io.BytesIO(before_bytes)).convert('RGB')
            img2 = Image.open(io.BytesIO(after_bytes)).convert('RGB')

            # Ensure same size for comparison
            if img1.size != img2.size:
                img2 = img2.resize(img1.size, Image.Resampling.LANCZOS)

            # 1. Exact Difference (Pixel by Pixel)
            diff = ImageChops.difference(img1, img2)
            
            # 2. Calculate percentage of changed pixels
            # A completely black diff image means 0 difference.
            # We count non-black pixels.
            # Faster approach: Get bounding box. If None, images are identical.
            bbox = diff.getbbox()
            if not bbox:
                return {"score": 0.0, "changed": False, "reason": "Images are identical"}

            # Statistical Difference (Root Mean Square)
            stat = ImageStat.Stat(diff)
            # Average pixel difference intensity (0-255)
            mean_diff = sum(stat.mean) / len(stat.mean)
            
            # Basic Pixel Count implementation (slower but strictly accurate for % area)
            # Optimized: Convert to grayscale and count non-zero
            diff_gray = diff.convert('L')
            # Histogram returns list of pixel counts for value 0..255
            histogram = diff_gray.histogram()
            # Count pixels that are NOT 0 (black)
            # We verify 'change' only if pixel diff > 10 (ignore minor compression artifacts)
            changed_pixels = sum(histogram[k] for k in range(15, 256))
            total_pixels = img1.width * img1.height
            
            percentage = (changed_pixels / total_pixels) * 100
            
            # Heuristic Thresholds
            # < 0.1%: Likely just a cursor blink or tiny render jitter
            # > 1.0%: meaningful change
            is_changed = percentage > 0.5 
            
            return {
                "score": round(percentage, 4),
                "changed": is_changed,
                "intensity": round(mean_diff, 2),
                "reason": f"Visual difference: {percentage:.2f}% of screen changed."
            }

        except Exception as e:
            print(f"Visual Diff Error: {e}")
            return {"score": 0.0, "changed": False, "reason": f"Error: {e}"}
