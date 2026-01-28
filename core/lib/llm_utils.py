import sys
import os
import asyncio
import time
import random
import json
import re
import base64
from functools import wraps
from termcolor import colored
from google import genai
from dotenv import load_dotenv

try:
    from .llm_cache import LLMCache
except ImportError:
    from llm_cache import LLMCache

load_dotenv()

def safe_llm_call(max_retries=10, initial_delay=1, backoff_factor=2):
# ... (decorator logic remains same, but we use it below)
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt == max_retries: raise e
                    
                    # Special handling for Rate Limits (429)
                    if "429" in str(e) or "ResourceExhausted" in str(e):
                        print(colored(f"[LIMIT] 429 Rate Limit Hit. Cooling down for 60s...", "yellow"))
                        time.sleep(60)
                    elif "INVALID_ARGUMENT" in str(e) or "image" in str(e).lower():
                        # Don't retry invalid requests (like bad images), fail fast so fallback kicks in
                        raise e
                    else:
                        time.sleep(delay)
                        delay *= backoff_factor
            return None
        return wrapper
    return decorator

class SafeLLM:
    """
    Wrapper for google-generativeai that behaves like ChatGoogleGenerativeAI.
    Bypasses Langchain/Pydantic version conflicts in the current environment.
    """

    def __init__(self, model=None, temperature=0.1, **kwargs):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment")
        
        self.client = genai.Client(api_key=api_key)
        
        #   DEFAULT MODEL: Use env var or Lite preview for better free tier limits
        if model is None:
            env_model = os.environ.get("LLM_MODEL")
            if env_model and env_model.lower() != "none" and env_model.strip() != "":
                model = env_model
            else:
                model = "gemini-2.0-flash"
            
        self.model_name = model.strip()
        print(colored(f"[LLM] SafeLLM Initialized: model={self.model_name}", "cyan"))
        self.temperature = temperature
        
        # Capture model_kwargs (like response_mime_type, max_output_tokens)
        self.config = {"temperature": temperature}
        if "model_kwargs" in kwargs:
            self.config.update(kwargs["model_kwargs"])
        elif "response_mime_type" in kwargs:
             self.config["response_mime_type"] = kwargs["response_mime_type"]
        
        #   FIX: Add default max_output_tokens if not specified
        # Prevents overly large responses that cause JSON parsing failures
        if "max_output_tokens" not in self.config:
            self.config["max_output_tokens"] = 4096  # Reasonable default
        
        # Initialize LLM cache
        self.cache = LLMCache()
        self.cache_hits = 0
        self.cache_misses = 0

    @safe_llm_call()
    def invoke(self, messages):
        # --- LLM CACHE CHECK ---
        cache_key = self._get_request_cache_key(messages)
        cached_response = self.cache.get(cache_key)
        
        if cached_response:
            self.cache_hits += 1
            print(f"[CACHE HIT] {cache_key[:8]}... (hits: {self.cache_hits}, misses: {self.cache_misses})")
            from types import SimpleNamespace
            return SimpleNamespace(content=cached_response["response"])
        
        self.cache_misses += 1
        # -----------------------
        
        # --- MULTI-PROCESS RATE LIMITING (Free Tier) ---
        # Coordinate across processes using a shared timestamp file
        lock_path = os.path.join(os.path.dirname(__file__), "..", "..", "outputs", "llm_throttle.json")
        os.makedirs(os.path.dirname(lock_path), exist_ok=True)

        def get_wait():
            try:
                if os.path.exists(lock_path):
                    with open(lock_path, "r") as f:
                        last_call = json.load(f).get("last_call", 0)
                    elapsed = time.time() - last_call
                    
                    #   THROTTLE: Configurable RPM (Default to ~25 RPM for Lite model)
                    rpm_limit = float(os.environ.get("LLM_RPM_LIMIT", 25))
                    wait_seconds = 60.0 / rpm_limit if rpm_limit > 0 else 0
                    return max(0, wait_seconds - elapsed) 
            except: pass
            return 0

        # Dynamic Wait
        wait_time = get_wait()
        if wait_time > 0:
            time.sleep(wait_time)

        # Update Lock
        try:
            with open(lock_path, "w") as f:
                json.dump({"last_call": time.time()}, f)
        except: pass
        # ---------------------------------------------

        # Convert Langchain-style messages to direct SDK prompt
        contents = []
        if isinstance(messages, list):
            for msg in messages:
                parts = []
                if isinstance(msg, tuple):
                    parts.append(f"{msg[0].upper()}: {msg[1]}")
                elif hasattr(msg, "content"):
                    if isinstance(msg.content, list):
                        for part in msg.content:
                            print(f"[DEBUG] Part Type: {part.get('type') if isinstance(part, dict) else 'non-dict'}")
                            if isinstance(part, dict) and part.get('type') == 'image_url':
                                url = part['image_url']['url']
                                mime_type = "image/png" # Default
                                b64_data = url
                                
                                # Handle data URI prefix: data:image/jpeg;base64,....
                                if url.startswith('data:'):
                                    header, b64_data = url.split(',', 1)
                                    # Extract mime_type from header
                                    match = re.search(r'data:(.*?);base64', header)
                                    if match:
                                        mime_type = match.group(1)
                                
                                # Sanitize Base64: Remove newlines and whitespace
                                b64_data = "".join(b64_data.split())
                                print(f"[DEBUG] Image Detected: {mime_type}, Data Length: {len(b64_data)} characters")
                                
                                # CRITICAL: SDK expects raw BYTES for inline_data.data, not a b64 string.
                                # If we pass a string, it might double-encode or fail.
                                import base64 as b64_lib
                                try:
                                    img_bytes = b64_lib.b64decode(b64_data)
                                    print(f"[DEBUG] Decoded to {len(img_bytes)} bytes")
                                    parts.append({"inline_data": {"mime_type": mime_type, "data": img_bytes}})
                                except Exception as e:
                                    print(f"[DEBUG] Base64 Decode Error: {e}")
                                    parts.append(url) # Fallback to raw string if it wasn't actually b64
                            else:
                                parts.append(part.get('text', str(part)))
                    else:
                        parts.append(msg.content)
                elif isinstance(msg, dict):
                    inner_content = msg.get('content', '')
                    if isinstance(inner_content, list):
                        for part in inner_content:
                            if isinstance(part, dict) and part.get('type') == 'image_url':
                                url = part['image_url']['url']
                                mime_type = "image/png"
                                b64_data = url
                                if url.startswith('data:'):
                                    header, b64_data = url.split(',', 1)
                                    match = re.search(r'data:(.*?);base64', header)
                                    if match: mime_type = match.group(1)
                                b64_data = "".join(b64_data.split())
                                import base64 as b64_lib
                                try:
                                    img_bytes = b64_lib.b64decode(b64_data)
                                    parts.append({"inline_data": {"mime_type": mime_type, "data": img_bytes}})
                                except: parts.append(url)
                            elif isinstance(part, dict) and part.get('type') == 'text':
                                parts.append(part.get('text', ''))
                            else:
                                parts.append(str(part))
                    else:
                        parts.append(str(inner_content))
                else:
                    parts.append(str(msg))
                
                contents.extend(parts)
        else:
            contents = [str(messages)]

        print(f"[DEBUG] Sending request to {self.model_name}. Number of parts: {len(contents)}")
        try:
            resp = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=self.config
            )
            text = resp.text
            print(f"[DEBUG] Received response (Length: {len(text) if text else 0})")
            if not text:
                # Handle cases where safety filters might have blocked it or empty response
                text = "{}" 
            
            # Cache the response
            self.cache.set(cache_key, text)
            
            from types import SimpleNamespace
            return SimpleNamespace(content=text)
        except Exception as e:
            print(f"[DEBUG] LLM Error: {e}")
            raise e

    async def ainvoke(self, messages):
        """
        Async wrapper for invoke. 
        Runs the blocking invoke() in a separate thread to prevent event loop blocking.
        """
        return await asyncio.to_thread(self.invoke, messages)
    
    def invalidate_last_cache(self, messages):
        """
        Invalidate the cache for the last request to force a fresh query.
        
        Args:
            messages: Same messages format used in invoke/ainvoke
            
        Returns:
            True if cache was invalidated, False otherwise
        """
        cache_key = self._get_request_cache_key(messages)
        deleted = self.cache.delete(cache_key)
        if deleted:
            print(f"[CACHE INVALIDATED] {cache_key[:8]}... Forcing fresh query on next call.")
        return deleted

    @safe_llm_call()
    def batch(self, prompts):
        return [self.invoke(p) for p in prompts]

    def _get_request_cache_key(self, messages):
        """
        Extract prompt text and image bytes for cache key generation.
        
        Args:
            messages: LLM messages in various formats
            
        Returns:
            Cache key string from LLMCache.get_cache_key()
        """
        prompt_parts = []
        image_bytes = None
        
        if isinstance(messages, list):
            for msg in messages:
                # Handle tuple format: ("system", "text")
                if isinstance(msg, tuple):
                    prompt_parts.append(f"{msg[0].upper()}: {msg[1]}")
                
                # Handle dict/object with content attribute
                elif hasattr(msg, 'content'):
                    if isinstance(msg.content, list):
                        for part in msg.content:
                            if isinstance(part, dict):
                                if part.get('type') == 'text':
                                    prompt_parts.append(part.get('text', ''))
                                elif part.get('type') == 'image_url':
                                    url = part['image_url']['url']
                                    if url.startswith('data:'):
                                        _, b64_data = url.split(',', 1)
                                        b64_data = "".join(b64_data.split())  # Remove whitespace
                                        try:
                                            import base64
                                            image_bytes = base64.b64decode(b64_data)
                                        except:
                                            pass  # Ignore malformed base64
                    else:
                        prompt_parts.append(str(msg.content))
                
                # Handle raw dict format
                elif isinstance(msg, dict):
                    content = msg.get('content', '')
                    if isinstance(content, list):
                        for part in content:
                            if isinstance(part, dict):
                                if part.get('type') == 'text':
                                    prompt_parts.append(part.get('text', ''))
                                elif part.get('type') == 'image_url':
                                    url = part['image_url']['url']
                                    if url.startswith('data:'):
                                        _, b64_data = url.split(',', 1)
                                        b64_data = "".join(b64_data.split())
                                        try:
                                            import base64
                                            image_bytes = base64.b64decode(b64_data)
                                        except:
                                            pass
                    else:
                        prompt_parts.append(str(content))
        else:
            # Handle string-based messages
            prompt_parts.append(str(messages))
        
        # Combine all prompts and hash
        combined_prompt = "\n---\n".join(prompt_parts)
        return self.cache.get_cache_key(combined_prompt, image_bytes)

def try_parse_json(content):
    """
    Robustly parses JSON from LLM output, handling markdown blocks and common escape errors.
    """
    if not content:
        return None
        
    # Handle AIMessage or other objects with .content
    if hasattr(content, 'content'):
        content = content.content
        
    if not isinstance(content, str):
        try:
            content = str(content)
        except:
            return None
        
    # 1. Strip Markdown Blocks
    content = re.sub(r'```json\s*', '', content)
    content = re.sub(r'\s*```', '', content)
    content = content.strip()
    
    # 2. Direct Parse
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        # 3. Handle Invalid Escapes (Common on Windows/Paths)
        # If it's an "Invalid \escape" error, we try to escape solo backslashes
        if "Invalid \\escape" in str(e):
            # Replace single \ with \\ unless it's already part of a valid escape
            # This is a bit risky but often works for path-heavy LLM output
            fixed_content = re.sub(r'\\(?![\\"/bfnrtu])', r'\\\\', content)
            try:
                return json.loads(fixed_content)
            except: pass
            
        # 4. Try Regex for first object
        match = re.search(r'(\{.*\})', content, re.DOTALL)
        if match:
            try: 
                return json.loads(match.group(1))
            except:
                # Try fixed version of regex match
                try:
                    fixed_match = re.sub(r'\\(?![\\"/bfnrtu])', r'\\\\', match.group(1))
                    return json.loads(fixed_match)
                except: pass
                
    # 5. Last Resort: YAML (More forgiving)
    try:
        import yaml
        return yaml.safe_load(content)
    except:
        pass
        
    return None
