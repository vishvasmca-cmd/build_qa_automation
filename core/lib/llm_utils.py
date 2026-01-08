import time
import random
import json
import re
from functools import wraps
from termcolor import colored
from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core.exceptions import ResourceExhausted, ServiceUnavailable, InternalServerError, DeadlineExceeded

def safe_llm_call(max_retries=3, initial_delay=1, backoff_factor=2):
    """
    Decorator for robust LLM calls with exponential backoff.
    Handles ResourceExhausted (429), ServiceUnavailable (503), and Internal errors.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except (ResourceExhausted, ServiceUnavailable, InternalServerError, DeadlineExceeded) as e:
                    last_exception = e
                    if attempt == max_retries:
                        print(colored(f"❌ LLM Call Failed after {max_retries} retries: {e}", "red"))
                        raise e
                    
                    sleep_time = delay + random.uniform(0, 0.5) # Add jitter
                    print(colored(f"⚠️ LLM Error ({type(e).__name__}). Retrying in {sleep_time:.2f}s... (Attempt {attempt+1}/{max_retries})", "yellow"))
                    time.sleep(sleep_time)
                    delay *= backoff_factor
                except Exception as e:
                    # Don't retry on other errors (e.g. InvalidArgument)
                    print(colored(f"❌ Unrecoverable LLM Error: {e}", "red"))
                    raise e
            return None
        return wrapper
    return decorator

class SafeLLM:
    """
    Wrapper for ChatGoogleGenerativeAI that automatically adds retry logic to invoke.
    """
    def __init__(self, model="gemini-2.0-flash", temperature=0.1, **kwargs):
        self.internal_llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            **kwargs
        )
    
    @safe_llm_call()
    def invoke(self, prompt):
        return self.internal_llm.invoke(prompt)

    @safe_llm_call()
    def batch(self, prompts):
        return self.internal_llm.batch(prompts)

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
