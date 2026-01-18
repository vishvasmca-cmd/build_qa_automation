"""
LLM Response Cache
Content-addressed caching for vision API calls to reduce redundant queries.
"""
import hashlib
import json
import os
from typing import Optional, Dict, Any


class LLMCache:
    """Cache for LLM API responses based on prompt + image content"""
    
    def __init__(self, cache_dir: str = "outputs/llm_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_cache_key(self, prompt_text: str, image_bytes: Optional[bytes] = None) -> str:
        """
        Generate cache key from prompt text and optional image bytes.
        
        Args:
            prompt_text: The text prompt sent to LLM
            image_bytes: Optional image bytes for vision queries
            
        Returns:
            MD5 hash of combined prompt + image content
        """
        key_parts = [prompt_text]
        
        if image_bytes:
            # Hash image content for efficient comparison
            img_hash = hashlib.sha256(image_bytes).hexdigest()[:16]
            key_parts.append(img_hash)
        
        # Combine and hash
        combined = "|".join(key_parts)
        return hashlib.md5(combined.encode()).hexdigest()
    
    def get(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached response if exists.
        
        Args:
            cache_key: Cache key from get_cache_key()
            
        Returns:
            Cached response dict or None if not found
        """
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                # If cache file is corrupted, ignore and fetch fresh
                print(f"[CACHE] Error reading cache {cache_key[:8]}: {e}")
                return None
        
        return None
    
    def set(self, cache_key: str, response: str) -> None:
        """
        Store response in cache.
        
        Args:
            cache_key: Cache key from get_cache_key()
            response: LLM response text to cache
        """
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump({"response": response}, f, indent=2)
        except Exception as e:
            # Cache write failures shouldn't break execution
            print(f"[CACHE] Warning: Failed to write cache {cache_key[:8]}: {e}")
    
    def clear(self) -> int:
        """
        Clear all cached responses.
        
        Returns:
            Number of cache files deleted
        """
        count = 0
        if os.path.exists(self.cache_dir):
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    os.remove(os.path.join(self.cache_dir, filename))
                    count += 1
        return count
    
    def delete(self, cache_key: str) -> bool:
        """
        Delete a specific cached response.
        
        Args:
            cache_key: Cache key from get_cache_key()
            
        Returns:
            True if cache file was deleted, False otherwise
        """
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if os.path.exists(cache_file):
            try:
                os.remove(cache_file)
                return True
            except Exception as e:
                print(f"[CACHE] Warning: Failed to delete cache {cache_key[:8]}: {e}")
                return False
        
        return False
