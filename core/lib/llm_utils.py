import asyncio
import time
import os
import random
import json
import re
from functools import wraps
from termcolor import colored
from google import genai
from dotenv import load_dotenv

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
                        print(colored(f"⚠️ 429 Rate Limit Hit. Cooling down for 60s...", "yellow"))
                        time.sleep(60)
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

    def __init__(self, model="gemini-2.0-flash", temperature=0.1, **kwargs):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment")
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = model
        self.temperature = temperature
        
        # Capture model_kwargs (like response_mime_type)
        self.config = {"temperature": temperature}
        if "model_kwargs" in kwargs:
            self.config.update(kwargs["model_kwargs"])
        elif "response_mime_type" in kwargs:
             self.config["response_mime_type"] = kwargs["response_mime_type"]

    @safe_llm_call()
    def invoke(self, messages):
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
                    return max(0, 5.0 - elapsed) # 12 RPM target
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
                            if isinstance(part, dict) and part.get('type') == 'image_url':
                                b64_data = part['image_url']['url'].split(',')[-1]
                                parts.append({"inline_data": {"mime_type": "image/jpeg", "data": b64_data}})
                            else:
                                parts.append(part.get('text', str(part)))
                    else:
                        parts.append(msg.content)
                elif isinstance(msg, dict):
                    parts.append(msg.get('content', ''))
                else:
                    parts.append(str(msg))
                
                # In google-genai, we can pass a list of strings/dicts directly as content parts
                contents.extend(parts)
        else:
            contents = [str(messages)]

        resp = self.client.models.generate_content(
            model=self.model_name,
            contents=contents,
            config=self.config
        )
        
        from types import SimpleNamespace
        return SimpleNamespace(content=resp.text)

    async def ainvoke(self, messages):
        """
        Async wrapper for invoke. 
        Runs the blocking invoke() in a separate thread to prevent event loop blocking.
        """
        return await asyncio.to_thread(self.invoke, messages)

    @safe_llm_call()
    def batch(self, prompts):
        return [self.invoke(p) for p in prompts]

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
