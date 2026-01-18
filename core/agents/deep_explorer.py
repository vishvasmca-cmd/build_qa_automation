import asyncio
import json
import os
import sys
import argparse
from datetime import datetime
from termcolor import colored
from typing import Dict, Any, List, Optional
from playwright.async_api import async_playwright

# Force UTF-8 for console output on Windows
# (Handled by imported modules or environment)
if sys.platform == "win32":
    pass

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.agents.explorer import ExplorerAgent
from core.lib.llm_utils import SafeLLM, try_parse_json

class DeepExplorerAgent:
    """
    Orchestrates the ExplorerAgent to drive deep semantic exploration 
    and generate regression test scenarios.
    """
    def __init__(self, project_dir: str, headed: bool = False):
        self.project_dir = os.path.abspath(project_dir)
        self.workflow_path = os.path.join(self.project_dir, "workflow.json")
        self.debug_log = os.path.join(self.project_dir, "deep_explorer_debug.log")
        self.headed = headed
        
        # Initialize Debug Log
        with open(self.debug_log, 'w', encoding='utf-8') as f:
            f.write(f"Deep Explorer Session started at {datetime.now()}\n")
            f.write("-" * 50 + "\n")
            
        # Re-use the underlying Explorer for execution logic
        self.explorer = ExplorerAgent(project_dir, headed=self.headed, shallow=False)
        self.generated_scenarios = []

    def log(self, msg: str, color: Optional[str] = None):
        if color:
            print(colored(msg, color), flush=True)
        else:
            print(msg, flush=True)
            
        with open(self.debug_log, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().isoformat()}] {msg}\n")

    async def run(self):
        self.log("\n🕵️ [DEEP EXPLORER] Starting Multi-Scenario Exploration", "magenta")
        
        if not os.path.exists(self.workflow_path):
            self.log("❌ workflow.json not found.", "red")
            return

        with open(self.workflow_path, 'r', encoding='utf-8') as f:
            workflow = json.load(f)
            
        scenarios = workflow.get("scenarios", [])
        if not scenarios:
            self.log("⚠️ No scenarios found in workflow.json to explore.", "yellow")
            return

        self.log(f"📋 Found {len(scenarios)} scenarios to explore.", "cyan")

        # Check if already done
        out_path = os.path.join(self.project_dir, "tests", "generated_scenarios.json")
        if os.path.exists(out_path):
            with open(out_path, 'r', encoding='utf-8') as f:
                existing = json.load(f)
            # Only skip if we have results
            if existing and len(existing) > 0:
                 self.log(f"⚡ [SKIP] Deep Exploration already completed ({len(existing)} scenarios found).", "yellow")
                 self.generated_scenarios = existing
                 self._save_results() # Ensure workflow.json is synced
                 return

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=not self.headed, slow_mo=500)
            # Iterate through each planned scenario
            for i, scenario in enumerate(scenarios):
                context = None
                try:
                    # Request a new context/page for each scenario to ensure isolation and stability
                    context = await browser.new_context(viewport={"width": 1280, "height": 720})
                    page = await context.new_page()
                    
                    try:
                        # Ensure ID exists for tracking
                        if "id" not in scenario:
                            scenario["id"] = f"TC_AUTO_{i+1}"
                        
                        # Pre-process steps: Add IDs and fix URLs
                        base_url = workflow.get("base_url", "")
                        for idx, step in enumerate(scenario.get("steps", [])):
                            if "id" not in step:
                                step["id"] = f"step_{idx+1}"
                            
                            if "args" not in step:
                                step["args"] = {}
                                
                            # Fix relative URLs
                            if step.get("keyword") == "navigate":
                                url = step["args"].get("url", "")
                                if url.startswith("/"):
                                    # Ensure base_url doesn't end with / if url starts with /
                                    if base_url.endswith("/"):
                                        step["args"]["url"] = base_url + url[1:]
                                    elif base_url:
                                        step["args"]["url"] = base_url + url
                                elif not url.startswith("http") and base_url:
                                     step["args"]["url"] = base_url
                            
                        self.log(f"\n[{i+1}/{len(scenarios)}] Exploring Scenario: {scenario.get('name')}", "blue")
                        
                        # Goal: Explore this specific scenario to confirm validity and find locators
                        stats = {"passed": 0, "healed": 0, "failed": 0, "details": []}
                        
                        try:
                            await self.explorer._explore_scenario(page, scenario, stats)
                        except Exception as e:
                            self.log(f"❌ critical error processing scenario '{scenario.get('name')}': {e}", "red")
                            if "Target page, context or browser has been closed" in str(e) or "Connection closed" in str(e):
                                raise 
    
                        # Store the result (Explorer modifies 'scenario' dict in-place)
                        scenario["steps"] = [s for s in scenario.get("steps", []) if not s.get("skipped")]
                        self.generated_scenarios.append(scenario)
                        
                    finally:
                        if context:
                            try:
                                await context.close()
                            except:
                                pass
                except Exception as sc_e:
                    self.log(f"❌ Critical error processing scenario '{scenario.get('name', i)}': {sc_e}", "red")
                    if "Connection closed" in str(sc_e) or "Target closed" in str(sc_e):
                        self.log("🛑 Browser connection lost. Stopping deep exploration.", "red")
                        break
                
                await asyncio.sleep(1)

            await browser.close()
            
            # Persist all generated tests
            self._save_results()
            self.log("\n✅ Deep Exploration Complete.", "green")

    def _save_results(self):
        # 1. Save to generated_scenarios.json (Backup)
        out_path = os.path.join(self.project_dir, "tests", "generated_scenarios.json")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(self.generated_scenarios, f, indent=2)
        self.log(f"🗂️  All generated tests written to {out_path}", "cyan")
        
        # 2. Update workflow.json for Executor
        workflow_update = {"project": os.path.basename(self.project_dir), "scenarios": []}
        if os.path.exists(self.workflow_path):
                 with open(self.workflow_path, "r", encoding="utf-8") as f:
                    workflow_update = json.load(f)
        
        # Map generated scenarios to workflow.json
        new_scenarios_map = {s["id"]: s["steps"] for s in self.generated_scenarios if "id" in s}
        for s in self.generated_scenarios:
            if "id" not in s: new_scenarios_map[s["name"]] = s["steps"]
        
        for i, existing in enumerate(workflow_update.get("scenarios", [])):
            sid = existing.get("id")
            name = existing.get("name")
            
            steps_source = None
            if sid in new_scenarios_map:
                steps_source = new_scenarios_map[sid]
            elif name in new_scenarios_map:
                steps_source = new_scenarios_map[name]
                
            if steps_source:
                sanitized_steps = []
                for idx, step in enumerate(steps_source):
                    new_step = step.copy()
                    if "arguments" in new_step and "args" not in new_step:
                         new_step["args"] = new_step.pop("arguments")
                    if "id" not in new_step:
                        new_step["id"] = f"step_{idx+1}"
                    sanitized_steps.append(new_step)
                workflow_update["scenarios"][i]["steps"] = sanitized_steps
        
        with open(self.workflow_path, "w", encoding="utf-8") as f:
            json.dump(workflow_update, f, indent=2)
        self.log(f"🔄 Updated workflow.json with discovered steps and locators.", "cyan")

async def main():
    parser = argparse.ArgumentParser(description="Deep Explorer Agent")
    parser.add_argument("--project", required=True, help="Project directory")
    parser.add_argument("--headed", action="store_true", help="Run headed")
    
    args = parser.parse_args()
    agent = DeepExplorerAgent(args.project, headed=args.headed)
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
