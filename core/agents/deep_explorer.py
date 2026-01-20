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
        
        # ✅ Performance tracking
        self.perf_stats = {
            "total_locators_mined": 0,
            "total_locators_filtered_out": 0,
            "total_robust_locators_saved": 0,
            "filtering_reasons": {
                "low_confidence": 0,
                "positional": 0,
                "state_dependent": 0
            }
        }

    def log(self, msg: str, color: Optional[str] = None):
        if color:
            print(colored(msg, color), flush=True)
        else:
            print(msg, flush=True)
            
        with open(self.debug_log, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().isoformat()}] {msg}\n")
    
    def _filter_robust_locators(self, locators: List[Dict]) -> List[Dict]:
        """
        Filter out brittle/positional selectors that break across runs.
        Only keep semantic, stable selectors with high confidence.
        
        This creates the "golden path" - validated locators that work 100%.
        """
        if not locators:
            return []
        
        robust_locators = []
        self.perf_stats["total_locators_mined"] += len(locators)
        
        for loc in locators:
            selector = loc.get("value", "")
            confidence = loc.get("confidence", 0.0)
            
            # 🐛 FIX Bug #5: Assign default confidence if missing or zero
            if confidence == 0.0:
                confidence = self._assign_default_confidence(selector)
                loc["confidence"] = confidence
            
            method = loc.get("method", "")
            
            # Rule 1: Minimum confidence threshold
            # 🐛 FIX: Lowered from 0.75 to 0.65 to accept generic selectors (0.60)
            if confidence < 0.65:
                self.perf_stats["total_locators_filtered_out"] += 1
                self.perf_stats["filtering_reasons"]["low_confidence"] += 1
                self.log(f"      ⚠️ Skipping low-confidence locator ({confidence:.2f}): {selector[:50]}...", "yellow")
                continue
            
            # Rule 2: Filter brittle positional selectors, but allow SCOPED ones
            is_positional = any(pattern in selector for pattern in ["nth-child", ":nth-of-type", "nth-last-child", ":nth("])
            
            if is_positional:
                # RELAXATION: Allow if it's a short scoped selector or has an ID/TestID
                # e.g. "#todo-list > li:nth-child(2)" is GOOD
                # e.g. "body > div:nth-child(4) > div:nth-child(2)" is BAD
                
                is_scoped = (
                    "#" in selector or 
                    "[data-" in selector or 
                    len(selector.split(">")) <= 3  # Short chain
                )
                
                if not is_scoped:
                     self.perf_stats["total_locators_filtered_out"] += 1
                     self.perf_stats["filtering_reasons"]["positional"] += 1
                     self.log(f"      ⚠️ Skipping brittle positional locator: {selector[:50]}...", "yellow")
                     continue
                else:
                     self.log(f"      ✨ Accepting scoped positional locator: {selector[:50]}...", "cyan")
                     # Penalty for positional to prefer ID if available
                     loc["confidence"] = loc.get("confidence", 0.7) - 0.1
            
            # Rule 3: Avoid state-dependent selectors
            if ":visible" in selector or ":hidden" in selector:
                self.perf_stats["total_locators_filtered_out"] += 1
                self.perf_stats["filtering_reasons"]["state_dependent"] += 1
                self.log(f"      ⚠️ Skipping state-dependent locator: {selector[:50]}...", "yellow")
                continue
            
            # Rule 4: Calculate stability score (prefer semantic selectors)
            stability_score = confidence
            
            if "data-testid" in selector or "data-test" in selector:
                stability_score += 0.15  # Boost test IDs
            elif "id=" in selector and "id*=" not in selector:
                stability_score += 0.10  # Boost exact IDs
            elif "aria-label" in selector:
                stability_score += 0.08  # Boost ARIA
            elif "role=" in selector:
                stability_score += 0.05  # Boost roles
            
            # Slight penalty for xpath (less maintainable)
            if "xpath" in selector.lower():
                stability_score -= 0.03
            
            # Add stability score to locator
            loc["stability_score"] = min(stability_score, 1.0)
            
            robust_locators.append(loc)
            self.log(f"      ✅ Kept robust locator ({stability_score:.2f}): {selector[:50]}...", "green")
        
        # Sort by stability score (highest first)
        robust_locators.sort(key=lambda x: x.get("stability_score", 0), reverse=True)
        
        # Rule 5: Diversity Check (Ensure we don't return 3 almost identical locators)
        from core.lib.smart_locator import is_diverse_from_existing
        
        unique_locators = []
        unique_values = []
        
        for loc in robust_locators:
            if len(unique_locators) >= 3:
                break
                
            if is_diverse_from_existing(loc["value"], unique_values):
                unique_locators.append(loc)
                unique_values.append(loc["value"])
            else:
                 self.log(f"      ⚠️ Skipping similar duplicate: {loc['value'][:30]}...", "grey")
        
        # Return top diverse stable locators
        self.perf_stats["total_robust_locators_saved"] += len(unique_locators)
        return unique_locators
    
    def _assign_default_confidence(self, selector: str) -> float:
        """🐛 FIX Bug #5: Assign confidence based on selector type when missing."""
        # Semantic selectors: High confidence
        if "data-testid" in selector or "data-test" in selector:
            return 0.9
        elif "aria-label" in selector:
            return 0.85
        elif selector.startswith("#") or ("[id=" in selector and "nth-child" not in selector):
            return 0.85
        
        # Attribute-based: Medium-high
        elif "data-" in selector:
            return 0.80
        elif "[name=" in selector:
            return 0.75
        
        # Text-based: Medium (depends on uniqueness, assume OK)
        elif selector.startswith("text=") or "has-text" in selector or ":has-text" in selector:
            return 0.70
        
        # Role-based: Medium
        elif selector.startswith("role="):
            return 0.70
        
        # Href-based: Medium
        elif "[href" in selector:
            return 0.70
        
        # Generic selectors: Low but not zero
        else:
            return 0.60

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
        new_scenarios_map = {s["id"]: s for s in self.generated_scenarios if "id" in s}
        for s in self.generated_scenarios:
            if "id" not in s: 
                new_scenarios_map[s["name"]] = s
        
        for i, existing in enumerate(workflow_update.get("scenarios", [])):
            sid = existing.get("id")
            name = existing.get("name")
            
            scenario_source = None
            if sid in new_scenarios_map:
                scenario_source = new_scenarios_map[sid]
            elif name in new_scenarios_map:
                scenario_source = new_scenarios_map[name]
                
            if scenario_source:
                # Update scenario metadata
                if "name" in scenario_source:
                    existing["name"] = scenario_source["name"]
                if "description" in scenario_source:
                    existing["description"] = scenario_source["description"]
                
                # ✅ CRITICAL: Save validated locators to workflow for executor
                sanitized_steps = []
                steps_source = scenario_source.get("steps", [])
                
                self.log(f"\n📝 Processing scenario '{existing.get('name')}' with {len(steps_source)} steps", "cyan")
                
                for idx, step in enumerate(steps_source):
                    new_step = step.copy()
                    
                    # Normalize args vs arguments
                    if "arguments" in new_step and "args" not in new_step:
                         new_step["args"] = new_step.pop("arguments")
                    
                    # Ensure step has ID
                    if "id" not in new_step:
                        new_step["id"] = f"step_{idx}"
                    
                    # ✅ CRITICAL: Filter and save only robust locators
                    mined_locators = step.get("locators", [])
                    if mined_locators:
                        self.log(f"  🔍 Step {idx} ({new_step.get('keyword')}): Found {len(mined_locators)} mined locators", "white")
                        robust_locators = self._filter_robust_locators(mined_locators)
                        
                        if robust_locators:
                            new_step["locators"] = robust_locators
                            self.log(f"  💾 Saved {len(robust_locators)} robust locators (top stability: {robust_locators[0].get('stability_score', 0):.2f})", "green")
                        else:
                            self.log(f"  ⚠️  No robust locators passed filtering. Executor will use fallback strategies.", "yellow")
                            # Don't add empty locators array
                            if "locators" in new_step:
                                del new_step["locators"]
                    else:
                        # No locators found during exploration
                        if "locators" in new_step:
                            del new_step["locators"]
                    
                    sanitized_steps.append(new_step)
                
                workflow_update["scenarios"][i]["steps"] = sanitized_steps
                self.log(f"✅ Updated scenario '{existing.get('name')}' with {len(sanitized_steps)} validated steps","green")
        
        with open(self.workflow_path, "w", encoding="utf-8") as f:
            json.dump(workflow_update, f, indent=2)
        self.log(f"🔄 Updated workflow.json with discovered steps and locators.", "cyan")
        
        # ✅ Print Performance Summary
        self._print_performance_summary()
    
    def _print_performance_summary(self):
        """Print explorer performance metrics."""
        self.log("\n" + "="*60, "blue")
        self.log("📊 EXPLORER PERFORMANCE SUMMARY", "blue")
        self.log("="*60, "blue")
        
        total_mined = self.perf_stats["total_locators_mined"]
        total_filtered = self.perf_stats["total_locators_filtered_out"]
        total_saved = self.perf_stats["total_robust_locators_saved"]
        
        if total_mined > 0:
            saved_rate = (total_saved / total_mined) * 100
            filtered_rate = (total_filtered / total_mined) * 100
        else:
            saved_rate = 0
            filtered_rate = 0
        
        self.log(f"\n🔍 Locator Mining:", "cyan")
        self.log(f"   • Total Locators Mined: {total_mined}")
        self.log(f"   • Filtered Out (Brittle): {total_filtered} ({filtered_rate:.1f}%)", "yellow")
        self.log(f"   • Saved to Golden Path: {total_saved} ({saved_rate:.1f}%)", "green")
        
        if total_filtered > 0:
            reasons = self.perf_stats["filtering_reasons"]
            self.log(f"\n⚠️  Filtering Breakdown:", "yellow")
            if reasons["low_confidence"] > 0:
                self.log(f"   • Low Confidence (<0.75): {reasons['low_confidence']}")
            if reasons["positional"] > 0:
                self.log(f"   • Positional Selectors: {reasons['positional']}")
            if reasons["state_dependent"] > 0:
                self.log(f"   • State-Dependent: {reasons['state_dependent']}")
        
        self.log(f"\n✅ Golden Path Quality:", "green")
        if saved_rate >= 70:
            self.log(f"   🌟 EXCELLENT - {saved_rate:.1f}% of mined locators are robust!")
        elif saved_rate >= 50:
            self.log(f"   ✅ GOOD - {saved_rate:.1f}% of mined locators are robust.")
        elif saved_rate >= 30:
            self.log(f"   ⚠️  FAIR - Only {saved_rate:.1f}% of mined locators are robust.")
        else:
            self.log(f"   ❌ POOR - Only {saved_rate:.1f}% of mined locators are robust. Site may have weak semantic HTML.", "red")
        
        self.log("\n" + "="*60, "blue")

async def main():
    parser = argparse.ArgumentParser(description="Deep Explorer Agent")
    parser.add_argument("--project", required=True, help="Project directory")
    parser.add_argument("--headed", action="store_true", help="Run headed")
    
    args = parser.parse_args()
    agent = DeepExplorerAgent(args.project, headed=args.headed)
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
