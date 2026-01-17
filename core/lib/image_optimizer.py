"""
Advanced Image Optimization Strategies to Reduce 429 Errors
Multiple approaches to minimize token usage while maintaining accuracy.
"""

from PIL import Image
import io
import base64
from typing import Tuple, Optional


class ImageOptimizer:
    """
    Advanced image optimization for LLM vision APIs.
    Reduces 429 rate limit errors by minimizing image size.
    """
    
    @staticmethod
    def aggressive_compress(image_bytes: bytes, max_kb: int = 10) -> str:
        """
        Strategy 1: Aggressive compression with lower quality.
        
        Current: Quality 50, ~84% reduction
        This: Quality 30, target <10KB
        """
        try:
            from PIL import Image
            
            img = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # Start with quality 30
            quality = 30
            output = io.BytesIO()
            
            # Iteratively compress until under target
            while quality > 10:
                output = io.BytesIO()
                img.save(output, format="JPEG", quality=quality, optimize=True)
                
                if len(output.getvalue()) <= max_kb * 1024:
                    break
                quality -= 5
            
            b64 = base64.b64encode(output.getvalue()).decode('utf-8')
            return b64
            
        except Exception as e:
            return base64.b64encode(image_bytes).decode('utf-8')
    
    @staticmethod
    def smart_crop(image_bytes: bytes, region: str = "top") -> str:
        """
        Strategy 2: Crop to relevant region only.
        
        Most important content is usually:
        - Top 60% (headers, nav, main content)
        - Center 60% (main content, modals)
        
        This can reduce size by 40-60% before compression.
        """
        try:
            from PIL import Image
            
            img = Image.open(io.BytesIO(image_bytes))
            width, height = img.size
            
            if region == "top":
                # Keep top 60%
                crop_box = (0, 0, width, int(height * 0.6))
            elif region == "center":
                # Keep center 60% vertically
                crop_start = int(height * 0.2)
                crop_end = int(height * 0.8)
                crop_box = (0, crop_start, width, crop_end)
            elif region == "bottom":
                # Keep bottom 60%
                crop_box = (0, int(height * 0.4), width, height)
            else:
                # Full image
                crop_box = (0, 0, width, height)
            
            img = img.crop(crop_box)
            
            # Convert and compress
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            output = io.BytesIO()
            img.save(output, format="JPEG", quality=35, optimize=True)
            
            return base64.b64encode(output.getvalue()).decode('utf-8')
            
        except Exception as e:
            return base64.b64encode(image_bytes).decode('utf-8')
    
    @staticmethod
    def adaptive_resolution(image_bytes: bytes, max_dimension: int = 800) -> str:
        """
        Strategy 3: Reduce resolution adaptively.
        
        Most LLM vision models work well with lower resolution.
        This reduces pixels by 50-75% while maintaining clarity.
        """
        try:
            from PIL import Image
            
            img = Image.open(io.BytesIO(image_bytes))
            width, height = img.size
            
            # Calculate new size
            if width > max_dimension or height > max_dimension:
                ratio = min(max_dimension / width, max_dimension / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert and compress
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            output = io.BytesIO()
            img.save(output, format="JPEG", quality=40, optimize=True)
            
            return base64.b64encode(output.getvalue()).decode('utf-8')
            
        except Exception as e:
            return base64.b64encode(image_bytes).decode('utf-8')
    
    @staticmethod
    def context_aware_optimization(
        image_bytes: bytes,
        step_type: str = "general"
    ) -> str:
        """
        Strategy 4: Optimize based on what we're looking for.
        
        Different optimization for different use cases:
        - search: Top region, low quality OK
        - form: Full page, medium quality
        - button: Center region, low quality OK
        - verification: Bottom region, medium quality
        """
        try:
            from PIL import Image
            
            img = Image.open(io.BytesIO(image_bytes))
            width, height = img.size
            
            # Define strategies per step type
            strategies = {
                "search": {
                    "crop": (0, 0, width, int(height * 0.4)),  # Top 40%
                    "quality": 30,
                    "max_dim": 600
                },
                "button": {
                    "crop": (0, int(height * 0.2), width, int(height * 0.8)),  # Center
                    "quality": 35,
                    "max_dim": 800
                },
                "form": {
                    "crop": (0, 0, width, height),  # Full
                    "quality": 40,
                    "max_dim": 1000
                },
                "verification": {
                    "crop": (0, int(height * 0.6), width, height),  # Bottom 40%
                    "quality": 30,
                    "max_dim": 600
                },
                "general": {
                    "crop": (0, 0, width, height),
                    "quality": 35,
                    "max_dim": 800
                }
            }
            
            strategy = strategies.get(step_type, strategies["general"])
            
            # Crop
            img = img.crop(strategy["crop"])
            
            # Resize
            w, h = img.size
            if w > strategy["max_dim"] or h > strategy["max_dim"]:
                ratio = min(strategy["max_dim"] / w, strategy["max_dim"] / h)
                img = img.resize((int(w * ratio), int(h * ratio)), Image.Resampling.LANCZOS)
            
            # Convert and compress
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            output = io.BytesIO()
            img.save(output, format="JPEG", quality=strategy["quality"], optimize=True)
            
            return base64.b64encode(output.getvalue()).decode('utf-8')
            
        except Exception as e:
            return base64.b64encode(image_bytes).decode('utf-8')
    
    @staticmethod
    def skip_image_if_cached(
        image_bytes: bytes,
        prev_url: Optional[str],
        current_url: str
    ) -> Optional[str]:
        """
        Strategy 5: Skip image entirely if page didn't change.
        
        If URL is the same as previous step, and we have DOM,
        we might not need the screenshot at all.
        
        Returns None if image should be skipped.
        """
        if prev_url == current_url:
            # Same page - skip image to save tokens
            return None
        
        # Different page - return optimized image
        return ImageOptimizer.adaptive_resolution(image_bytes)


# Recommended configuration for production
RECOMMENDED_CONFIG = {
    "strategy": "context_aware",  # Best balance
    "fallback": "adaptive_resolution",  # If context unknown
    "max_kb_target": 8,  # Target size
    "skip_duplicates": True  # Skip if URL unchanged
}
