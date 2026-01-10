"""
Business Validator (The Self-Critic)
Validates whether the executed test actually achieved the business goal.
Distinguishes between "Code passed" (no errors) and "Goal met" (cart updated, login successful).
"""
import os
import json
import base64
from termcolor import colored
try:
    from .llm_utils import SafeLLM, try_parse_json
except ImportError:
    from llm_utils import SafeLLM, try_parse_json

class BusinessValidator:
    def __init__(self):
        self.llm = SafeLLM(model="gemini-2.0-flash", temperature=0.0)

    def validate_goal_completion(self, goal, trace_path, screenshot_path=None):
        """
        Analyzes trace and screenshot to confirm if the business goal was met.
        
        Args:
            goal (str): The original user objective (e.g. "Add to cart")
            trace_path (str): Path to the execution trace JSON
            screenshot_path (str): Path to the final state screenshot (optional)
            
        Returns:
            dict: {"status": "PASS/FAIL/AMBIGUOUS", "reason": "...", "confidence": 0-1}
        """
        print(colored("🕵️ Running Business Validation (Self-Critic)...", "cyan"))
        
        # 1. Load Trace Context
        trace_summary = "No trace available."
        last_url = "Unknown"
        if os.path.exists(trace_path):
            try:
                with open(trace_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    trace_list = []
                    if isinstance(data, list):
                        trace_list = data
                    elif isinstance(data, dict):
                        trace_list = data.get('trace', [])
                    
                    if trace_list:
                        # Summarize last 5 steps
                        steps = []
                        for i, step in enumerate(trace_list[-5:]):
                            action = step.get('action', 'unknown')
                            # Handle both 'selector' (Legacy) and 'locator_used' (Explorer)
                            target = step.get('selector') or step.get('locator_used') or step.get('element_context', {}).get('text') or ''
                            steps.append(f"Step {len(trace_list)-5+i}: {action} on {target}")
                        trace_summary = "\n".join(steps)
                        last_url = trace_list[-1].get('url', 'Unknown')
            except Exception as e:
                trace_summary = f"Error reading trace: {e}"

        # 2. visual Context (if available)
        image_context = []
        if screenshot_path and os.path.exists(screenshot_path):
            try:
                with open(screenshot_path, "rb") as img_file:
                    b64_data = base64.b64encode(img_file.read()).decode('utf-8')
                    image_context = [{"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_data}"}}]
            except:
                pass

        # 3. Construct Prompt
        prompt = f"""
        You are a strict QA Business Validator. Your job is to verify if the automated test achieved its goal.
        
        USER GOAL: "{goal}"
        
        FINAL APP STATE:
        - Last URL: {last_url}
        - Recent Actions:
        {trace_summary}
        
        TASK:
        Look at the screenshot (if provided) and the actions.
        Did the agent SUCCEED in accomplishing the goal?
        
        CRITERIA:
        - PASS: Clear evidence the goal was met (e.g. "Order Confirmation" seen for purchase goal).
        - FAIL: Clear evidence it failed or got stuck (e.g. still on login page for dashboard goal).
        - AMBIGUOUS: Not enough info to be sure.
        
        Return JSON:
        {{
            "status": "PASS" | "FAIL" | "AMBIGUOUS",
            "reason": "Brief explanation of your verdict",
            "confidence": 0.0 to 1.0
        }}
        """
        
        # 3. Construct Prompt (Use HumanMessage for Robustness)
        from langchain_core.messages import HumanMessage
        
        content_parts = [{"type": "text", "text": prompt}]
        if image_context:
            content_parts.extend(image_context)
            
        messages = [HumanMessage(content=content_parts)]
        
        # 4. Call LLM
        response = self.llm.invoke(messages)
        result = try_parse_json(response.content if hasattr(response, 'content') else response)
        
        if not result:
            return {"status": "AMBIGUOUS", "reason": "Validator failed to parse response", "confidence": 0.0}
            
        status = result.get("status", "AMBIGUOUS")
        color = "green" if status == "PASS" else "red" if status == "FAIL" else "yellow"
        print(colored(f"🕵️ Validator Verdict: {status} ({result.get('confidence')}) - {result.get('reason')}", color))
        
        return result
