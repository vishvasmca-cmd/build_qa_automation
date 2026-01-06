import time
import random
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
