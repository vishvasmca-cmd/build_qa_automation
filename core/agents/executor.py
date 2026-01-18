import asyncio
import json
import os
import sys
import argparse
from datetime import datetime
from termcolor import colored
from typing import Dict, Any, List, Optional
from playwright.async_api import async_playwright, Page, expect

# Force UTF-8 for console output on Windows
if sys.platform == "win32":
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.lib.keywords import KeywordEngine
from core.lib.failure_kb import FailureKnowledgeBase
from core.lib.data_generator import DataGenerator
from core.lib.error_handler import ErrorHandler, ErrorType
from core.lib.llm_utils import SafeLLM, try_parse_json
from core.agents.miner import analyze_page
from core.lib.domain_expert import DomainExpert

class ExecutorAgent:
    """
    Executes test scenarios from workflow.json with AI-powered self-healing and detailed logging.
    """
    def __init__(self, project_dir: str, headed: bool = False, max_retries: int = 3):
        self.project_dir = os.path.abspath(project_dir)
        self.workflow_path = os.path.join(self.project_dir, "workflow.json")
        self.execution_path = os.path.join(self.project_dir, "execution.json")
        self.debug_log = os.path.join(self.project_dir, "executor_debug.log")
        self.headed = headed
        self.max_retries = max_retries
        
        self.failure_kb = FailureKnowledgeBase()
        
        # Initialize Debug Log
        with open(self.debug_log, 'w', encoding='utf-8') as f:
            f.write(f"Executor Session started at {datetime.now()}\n")
            f.write("-" * 50 + "\n")

        # Load Workflow
        if not os.path.exists(self.workflow_path):
            raise FileNotFoundError(f"Workflow file not found: {self.workflow_path}")
        with open(self.workflow_path, 'r', encoding='utf-8') as f:
            self.workflow = json.load(f)
            
        self.llm = SafeLLM(
            model="gemini-2.0-flash",
            temperature=0.0,
            model_kwargs={"response_mime_type": "application/json"}
        )

        self.results = {
            "run_id": f"run_{int(datetime.now().timestamp())}",
            "start_time": datetime.now().isoformat(),
            "scenarios": []
        }

    def log(self, msg: str, color: Optional[str] = None, attrs: Optional[List[str]] = None):
        """Unified logging to console (with color) and debug file."""
        plain_msg = msg
        if color:
            print(colored(msg, color, attrs=attrs))
        else:
            print(msg)
            
        with open(self.debug_log, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().isoformat()}] {plain_msg}\n")

    async def execute(self):
        self.log("\n🚀 [EXECUTE] Starting Automation Execution Engine", "blue", attrs=["bold"])
        self.log(f"📍 Project: {os.path.basename(self.project_dir)}")
        self.log(f"🎬 Mode: {'Headed' if self.headed else 'Headless'}")
        
        async with async_playwright() as p:
            # Slow-mo for better visibility
            browser = await p.chromium.launch(headless=not self.headed, slow_mo=500)
            
            for scenario in self.workflow.get("scenarios", []):
                self.log(f"\n--- Scenario: {scenario['name']} ---", "cyan", attrs=["bold"])
                
                # New context for isolation
                context = await browser.new_context()
                page = await context.new_page()
                
                scenario_result = {
                    "id": scenario["id"],
                    "status": "passed",
                    "steps": []
                }
                
                try:
                    for step in scenario.get("steps", []):
                        # Dismiss overlays/ads before each step
                        await self._dismiss_vignettes(page)
                        
                        step_result = await self.execute_step(page, step, scenario["name"])
                        scenario_result["steps"].append(step_result)
                        
                        if step_result["status"] == "failed":
                            scenario_result["status"] = "failed"
                            self.log(f"🛑 Scenario '{scenario['name']}' aborted due to step failure.", "red")
                            break 
                    
                    if scenario_result["status"] == "passed":
                        self.log(f"✅ Scenario '{scenario['name']}' completed successfully!", "green")
                        
                except Exception as e:
                    scenario_result["status"] = "failed"
                    scenario_result["error"] = str(e)
                    self.log(f"💥 Fatal scenario error: {e}", "red")
                
                self.results["scenarios"].append(scenario_result)
                await context.close()
                
            self.results["end_time"] = datetime.now().isoformat()
            
            # Save final execution result
            with open(self.execution_path, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2)
            
            await browser.close()
            self.log(f"\n🏁 Execution Finished. Report: {self.execution_path}", "green", attrs=["bold"])

    async def execute_step(self, page: Page, step: Dict, scenario_name: str) -> Dict:
        keyword = step["keyword"]
        # Compatibility handling: args vs arguments
        args = step.get("args") or step.get("arguments", {})
        locators = step.get("locators", [])
        step_id = step.get("id") # Use get() to enable fallback if missing
        if not step_id:
             step_id = "unknown"
        
        description = args.get("description") or f"Step {step_id}"
        self.log(f"  ▶️ [STEP {step_id}] {keyword.upper()}: {description}", "white")
        
        # 1. Resolve Dynamic Data
        resolved_args = {k: DataGenerator.resolve(v) for k, v in args.items()}
        
        # 2. Extract best selector from mined locators
        best_selector = None
        if locators:
            # Sort candidates by priority (lower is better)
            candidate_selectors = sorted(locators, key=lambda x: x.get("priority", 5))
            
            # Simple validation loop
            for candidate in candidate_selectors:
                sel_value = candidate["value"]
                try:
                    if await page.locator(sel_value).count() > 0:
                        best_selector = sel_value
                        self.log(f"    🎯 Using mined locator: {best_selector}", "cyan")
                        break
                except:
                    continue
            
            if not best_selector:
                self.log("    ⚠️ Mined locators not found on page. Falling back to semantic search.", "yellow")

        # 3. Execution with AI Healing Loop
        for attempt in range(self.max_retries):
            try:
                # Target selector for this attempt
                selector = best_selector or f"text={description}"
                
                # Visual highlight before action
                await self._highlight_element(page, selector)

                # Dispatch keyword to engine
                if keyword == "navigate":
                    nav_url = resolved_args.get("url") or resolved_args.get("description")
                    if nav_url:
                        await KeywordEngine.navigate(page, nav_url)
                    else:
                        raise ValueError("No URL provided for navigation")
                elif keyword == "click":
                    await KeywordEngine.click(page, selector)
                elif keyword == "fill":
                    await KeywordEngine.fill(page, selector, resolved_args["value"])
                elif keyword == "assert_visible":
                    await KeywordEngine.assert_visible(page, selector)
                elif keyword == "wait_for_element":
                    await KeywordEngine.wait_for_element(page, selector)
                elif keyword == "screenshot":
                    await KeywordEngine.screenshot(page, resolved_args.get("name", f"step_{step_id}"))
                # ... other keywords mapping ...
                
                self.log(f"    ✅ Step {step_id} Passed.", "green")
                return {"id": step_id, "status": "passed", "attempt": attempt + 1}
                
            except Exception as e:
                error_type = ErrorHandler.categorize(e)
                self.log(f"    ❌ Attempt {attempt+1} failed ({error_type.value}): {str(e)[:100]}...", "yellow")
                
                # If last attempt, give up
                if attempt == self.max_retries - 1:
                    self.log(f"    💀 Step {step_id} failed after all retries.", "red", attrs=["bold"])
                    self.failure_kb.record_failure(scenario_name, step_id, description, str(e))
                    return {"id": step_id, "status": "failed", "error": str(e), "error_type": error_type.value}
                
                # --- AI HEALING TRIGGER ---
                self.log(f"    🔧 [AUTO-HEAL] Re-mining page to find '{description}'...", "magenta")
                # Capture fresh mindmap
                description = resolved_args.get("description") or keyword
                new_selector = await self.heal_step(page, step, description, scenario_name, keyword)
                
                if new_selector:
                    best_selector = new_selector
                    self.log(f"    ✨ AI successfully healed the step! New selector: {best_selector}", "green")
                else:
                    self.log("    ❌ AI could not re-locate the element. Waiting 1s before next retry.", "yellow")
                    await asyncio.sleep(1)

    async def heal_step(self, page: Page, step: Dict, description: str, scenario_name: str = "", keyword: str = "") -> Optional[str]:
        """Vision-centric healing when execution fails. Returns the best new selector."""
        try:
            mindmap = await analyze_page(page, page.url, description)
            screenshot = mindmap.get("screenshot")

            # 2. Consult the Oracle (Multi-Locator Vision)
            goal = self.workflow.get("goal", "Complete the scenario")
            url = self.workflow.get("base_url", "")
            
            # Domain Expert Persona
            domain = DomainExpert.detect_domain(url, "", goal)
            persona = DomainExpert.get_persona_prompt(domain)
            
            message_content = [
                {
                    "type": "text",
                    "text": f"""
                    {persona}
                    
                    **MISSION:**
                    Goal: "{goal}"
                    
                    **FAILURE:**
                    Step: "{description}"
                    Action: "{keyword}"
                    
                    **TASK:**
                    Identify the best VISIBLE elements on the current page that match the intent.
                    Provide MULTIPLE high-quality CSS selectors (Primary, Secondary).
                    
                    **RESPONSE FORMAT (Strict JSON):**
                    {{
                        "found": true,
                        "locators": [
                            {{"type": "css", "value": "#id", "priority": 0, "reasoning": "..."}},
                            {{"type": "css", "value": ".class", "priority": 1, "reasoning": "..."}}
                        ]
                    }}
                    """
                }
            ]
            
            if screenshot:
                message_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{screenshot}"}})

            resp = await self.llm.ainvoke([{"role": "user", "content": message_content}])
            fix = try_parse_json(resp.content)
            
            if fix and fix.get("found") and fix.get("locators"):
                new_locators = fix["locators"]
                self.log(f"    ✨ AI successfully healed the step! Found {len(new_locators)} alternatives.", "blue")
                
                # Update Workflow
                step["locators"] = new_locators
                with open(self.workflow_path, 'w', encoding='utf-8') as f:
                    json.dump(self.workflow, f, indent=2)
                
                return new_locators[0]["value"]
        except Exception as e:
            self.log(f"    ⚠️ Healing Error: {e}", "red")
        return None

    async def _dismiss_vignettes(self, page: Page):
        """Attempts to dismiss ad overlays (google_vignette) if they appear."""
        try:
            # Check for common vignette IDs/classes
            overlay_selectors = ["#google_vignette", ".google-vignette-container", "ins.adsbygoogle"]
            for sel in overlay_selectors:
                if await page.is_visible(sel, timeout=500):
                    self.log(f"    📢 Detected overlay ({sel}). Attempting to dismiss...", "yellow")
                    # Try clicking outside or pressing ESC
                    await page.keyboard.press("Escape")
                    await asyncio.sleep(1)
                    # If it's a specific 'dismiss' button, try to click it (site specific, but often there)
                    dismiss_btn = "div[id='dismiss-button'], div.dismiss-button"
                    if await page.is_visible(dismiss_btn, timeout=500):
                        await page.click(dismiss_btn, force=True)
                        self.log("    ✅ Dismiss button clicked.", "green")
        except:
            pass

    async def _highlight_element(self, page: Page, selector: str):
        """Visually highlights an element on the page for debugging."""
        try:
            await page.evaluate(f"""
                (selector) => {{
                    const el = document.querySelector(selector);
                    if (el) {{
                        const prevOutline = el.style.outline;
                        const prevBg = el.style.backgroundColor;
                        el.style.outline = '4px solid #3498db';
                        el.style.backgroundColor = 'rgba(52, 152, 219, 0.4)';
                        setTimeout(() => {{
                            el.style.outline = prevOutline;
                            el.style.backgroundColor = prevBg;
                        }}, 1500);
                    }}
                }}
            """, selector)
            await asyncio.sleep(0.5) 
        except:
            pass

async def main():
    parser = argparse.ArgumentParser(description="AI Test Executor")
    parser.add_argument("--project", required=True, help="Project path")
    parser.add_argument("--headed", action="store_true", help="Run headed")
    parser.add_argument("--retries", type=int, default=3, help="Max retries")
    
    args = parser.parse_args()
    
    agent = ExecutorAgent(args.project, headed=args.headed, max_retries=args.retries)
    await agent.execute()

if __name__ == "__main__":
    asyncio.run(main())
