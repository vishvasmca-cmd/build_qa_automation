import time
import os
import random
import json
import re
from functools import wraps
from termcolor import colored
import google.generativeai as genai
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
    def __init__(self, model="gemini-flash-latest", temperature=0.1, **kwargs):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment")
        genai.configure(api_key=api_key)
        self.model_name = model
        self.temperature = temperature
        self.model = genai.GenerativeModel(model)

    @safe_llm_call()
    def invoke(self, messages):
        # Free Tier Throttling: Aggressive 10s delay to stay under RPM limits
        time.sleep(10)

        # Convert Langchain-style messages to direct SDK prompt
        if isinstance(messages, list):
            # Try to concatenate messages or use content
            prompt = ""
            for msg in messages:
                if isinstance(msg, tuple):
                    prompt += f"{msg[0].upper()}: {msg[1]}\n"
                elif hasattr(msg, "content"):
                    prompt += f"{msg.content}\n"
                elif isinstance(msg, dict):
                     prompt += f"{msg.get('role', '').upper()}: {msg.get('content', '')}\n"
                else:
                    prompt += str(msg) + "\n"
        else:
            prompt = str(messages)

        resp = self.model.generate_content(
            prompt, 
            generation_config={"temperature": self.temperature},
            request_options={"timeout": 120}
        )
        
        # Mock Langchain response object
        from types import SimpleNamespace
        return SimpleNamespace(content=resp.text)

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
