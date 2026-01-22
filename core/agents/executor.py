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
            model=None,
            temperature=0.0,
            model_kwargs={"response_mime_type": "application/json"}
        )

        self.results = {
            "run_id": f"run_{int(datetime.now().timestamp())}",
            "start_time": datetime.now().isoformat(),
            "scenarios": []
        }
        
        # ✅ Performance tracking (Explorer vs Executor comparison)
        self.perf_stats = {
            "total_steps": 0,
            "first_attempt_success": 0,
            "required_healing": 0,
            "final_failures": 0,
            "golden_path_hits": 0,  # Steps where mined locator worked
            "golden_path_misses": 0,  # Steps where mined locator failed
            "fallback_used": 0,  # Steps with no mined locators
            "locator_methods_used": {}
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
                
                # New context for isolation with Ad Blocking
                context = await browser.new_context()
                await self._setup_ad_blocking(context)
                page = await context.new_page()
                
                scenario_result = {
                    "id": scenario["id"],
                    "status": "passed",
                    "steps": []
                }
                
                try:
                    for step_idx, step in enumerate(scenario.get("steps", [])):
                        # Dismiss overlays/ads before each step
                        await self._dismiss_vignettes(page)
                        
                        step_result = await self.execute_step(page, step, scenario["name"], step_idx)
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
            
            # --- EXECUTION SUMMARY ---
            total_scenarios = len(self.workflow.get("scenarios", []))
            executed_scenarios = len(self.results["scenarios"])
            passed_scenarios = sum(1 for s in self.results["scenarios"] if s["status"] == "passed")
            failed_scenarios = executed_scenarios - passed_scenarios
            
            self.log("\n" + "="*60, "blue")
            self.log("🎯 EXECUTION SUMMARY", "blue", attrs=["bold"])
            self.log("="*60, "blue")
            
            # High-level overview
            self.log(f"\n📋 Scenario Overview:", "cyan", attrs=["bold"])
            self.log(f"   • Total Scenarios Planned: {total_scenarios}")
            self.log(f"   • Scenarios Executed: {executed_scenarios}")
            self.log(f"   • Total Steps Executed: {sum(len(s.get('steps', [])) for s in self.results['scenarios'])}")
            
            # Pass/Fail breakdown
            self.log(f"\n✅ Results:", "cyan", attrs=["bold"])
            if passed_scenarios > 0:
                self.log(f"   ✅ Passed: {passed_scenarios} ({int(passed_scenarios/executed_scenarios*100)}%)" if executed_scenarios > 0 else "   ✅ Passed: 0", "green")
            if failed_scenarios > 0:
                self.log(f"   ❌ Failed: {failed_scenarios} ({int(failed_scenarios/executed_scenarios*100)}%)" if executed_scenarios > 0 else "   ❌ Failed: 0", "red")
            
            # List failed scenarios
            if failed_scenarios > 0:
                self.log(f"\n⚠️  Failed Scenarios:", "red", attrs=["bold"])
                for scenario_result in self.results["scenarios"]:
                    if scenario_result["status"] == "failed":
                        scenario_name = next((s["name"] for s in self.workflow.get("scenarios", []) if s["id"] == scenario_result["id"]), "Unknown")
                        self.log(f"   • {scenario_name}")
                        if "error" in scenario_result:
                            self.log(f"     Error: {scenario_result['error'][:100]}...", "red")
            
            self.log("\n" + "="*60, "blue")
            self.log(f"\n🏁 Execution Finished. Report: {self.execution_path}", "green", attrs=["bold"])
            
            # ✅ Print Performance Comparison
            self._print_performance_summary()

    async def execute_step(self, page: Page, step: Dict, scenario_name: str, step_index: int = 0) -> Dict:
        keyword = step["keyword"]
        # Compatibility handling: args vs arguments
        args = step.get("args") or step.get("arguments", {})
        locators = step.get("locators", [])
        
        # ✅ Better step ID handling
        step_id = step.get("id") or f"step_{step_index}"
        
        description = args.get("description") or f"{keyword.upper()}"
        self.log(f"  ▶️  [STEP {step_id}] {keyword.upper()}: {description}", "white")
        
        # 1. Resolve Dynamic Data
        resolved_args = {k: DataGenerator.resolve(v) for k, v in args.items()}
        
        # 2. ✅ Enhanced: Extract best selector from mined locators using stability score
        best_selector = None
        if locators:
            # Sort by stability_score (if exists, from exploration) or confidence
            candidate_selectors = sorted(
                locators,
                key=lambda x: (
                    x.get("stability_score", x.get("confidence", 0)),  # Primary: stability/confidence
                    -x.get("priority", 5)  # Secondary: priority (lower is better, so negate)
                ),
                reverse=True  # Higher stability/confidence first
            )
            
            self.log(f"    🔍 Trying {len(candidate_selectors)} validated locators from golden path...", "cyan")
            
            # ✅ Try each validated locator with detailed logging
            for idx, candidate in enumerate(candidate_selectors):
                sel_value = candidate["value"]
                method = candidate.get("method", "unknown")
                confidence = candidate.get("confidence", 0.0)
                stability = candidate.get("stability_score", confidence)
                
                try:
                    count = await page.locator(sel_value).count()
                    
                    # 🐛 FIX Bug #3: Validate uniqueness (exactly 1 match)
                    if count == 1:
                        best_selector = sel_value
                        self.log(
                            f"    ✅ SUCCESS! Locator #{idx+1}: {sel_value[:60]}... "
                            f"(method: {method}, stability: {stability:.2f})",
                            "green"
                        )
                        break
                    elif count > 1:
                        self.log(
                            f"    ⚠️  Locator #{idx+1} matched {count} elements (need exactly 1): {sel_value[:40]}...",
                            "yellow"
                        )
                        # 🐛 FIX Bug #3: Try making it more specific
                        if count == 2:
                            # Try .first
                            specific_selector = f"({sel_value}).first"
                            try:
                                specific_count = await page.locator(specific_selector).count()
                                if specific_count == 1:
                                    best_selector = specific_selector
                                    self.log(f"    🔧 Made specific: {specific_selector[:40]}...", "cyan")
                                    break
                            except:
                                pass
                    elif count == 0:
                        self.log(
                            f"    ❌ Locator #{idx+1} found 0 elements: {sel_value[:40]}...",
                            "grey"
                        )
                except Exception as e:
                    self.log(
                        f"    ⚠️  Locator #{idx+1} error: {str(e)[:50]}...",
                        "grey"
                    )
                    continue
            
            if not best_selector:
                self.log("    ⚠️  All golden path locators failed. Will try text-based fallback.", "yellow")
                self.perf_stats["golden_path_misses"] += 1
            else:
                self.perf_stats["golden_path_hits"] += 1
        else:
            # No mined locators - using fallback from start
            self.perf_stats["fallback_used"] += 1
        
        # Track total steps
        self.perf_stats["total_steps"] += 1

        # 3. Execution with AI Healing Loop
        for attempt in range(self.max_retries):
            try:
                # Target selector for this attempt
                selector = best_selector or f"text={description}"
                
                # ✅ Support explicit index argument
                if "index" in resolved_args:
                    idx = resolved_args["index"]
                    if selector and "nth=" not in selector:
                        selector = f"{selector} >> nth={idx}"
                        self.log(f"    🎯 Applied explicit index {idx}: {selector}", "cyan")
                
                # Visual highlight before action
                await self._highlight_element(page, selector)

                # Dispatch keyword to engine
                if keyword == "navigate":
                    nav_url = resolved_args.get("url") or resolved_args.get("description")
                    base_url = self.workflow.get("base_url", "")
                    
                    if nav_url and nav_url.startswith("/") and base_url:
                        full_url = base_url.rstrip("/") + nav_url
                        self.log(f"    🔗 Joining relative URL: {nav_url} -> {full_url}", "grey")
                        nav_url = full_url
                        
                    if nav_url:
                        await KeywordEngine.navigate(page, nav_url)
                    else:
                        raise ValueError("No URL provided for navigation")
                elif keyword == "click":
                    # 🐛 FIX Bug #1: Try force click if element not visible (modal handling)
                    try:
                        await KeywordEngine.click(page, selector)
                    except Exception as click_err:
                        if "not visible" in str(click_err) or "hidden" in str(click_err).lower():
                            self.log(f"    🔧 Element not visible, trying force click...", "yellow")
                            await page.locator(selector).click(force=True, timeout=10000)
                        else:
                            raise
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
                # ✅ Track first-attempt success
                if attempt == 0:
                    self.perf_stats["first_attempt_success"] += 1
                return {"id": step_id, "status": "passed", "attempt": attempt + 1}
                
            except Exception as e:
                error_type = ErrorHandler.categorize(e)
                self.log(f"    ❌ Attempt {attempt+1} failed ({error_type.value}): {str(e)[:100]}...", "yellow")
                
                # If last attempt, give up
                if attempt == self.max_retries - 1:
                    self.log(f"    💀 Step {step_id} failed after all retries.", "red", attrs=["bold"])
                    self.failure_kb.record_failure(scenario_name, step_id, description, str(e))
                    # ✅ Track final failure
                    self.perf_stats["final_failures"] += 1
                    return {"id": step_id, "status": "failed", "error": str(e), "error_type": error_type.value}
                
                # --- AI HEALING TRIGGER ---
                self.log(f"    🔧 [AUTO-HEAL] Re-mining page to find '{description}'...", "magenta")
                # ✅ Track healing attempt
                self.perf_stats["required_healing"] += 1
                
                # Capture fresh mindmap
                description = resolved_args.get("description") or keyword
                new_selector = await self.heal_step(page, step, description, scenario_name, keyword)
                
                if new_selector:
                    best_selector = new_selector
                    self.log(f"    ✨ AI successfully healed the step! New selector: {best_selector}", "green")
                else:
                    self.log("    ❌ AI could not re-locate the element. Waiting 1s before next retry.", "yellow")
                    await asyncio.sleep(1)
    
    def _print_performance_summary(self):
        """Print executor performance metrics and compare with golden path expectations."""
        self.log("\n" + "="*60, "blue")
        self.log("📊 EXECUTOR PERFORMANCE SUMMARY", "blue", attrs=["bold"])
        self.log("="*60, "blue")
        
        total = self.perf_stats["total_steps"]
        first_success = self.perf_stats["first_attempt_success"]
        healing = self.perf_stats["required_healing"]
        failures = self.perf_stats["final_failures"]
        
        golden_hits = self.perf_stats["golden_path_hits"]
        golden_misses = self.perf_stats["golden_path_misses"]
        fallback = self.perf_stats["fallback_used"]
        
        if total > 0:
            first_success_rate = (first_success / total) * 100
            healing_rate = (healing / total) * 100
            failure_rate = (failures / total) * 100
        else:
            first_success_rate = 0
            healing_rate = 0
            failure_rate = 0
        
        # Golden Path Effectiveness
        golden_total = golden_hits + golden_misses
        if golden_total > 0:
            golden_hit_rate = (golden_hits / golden_total) * 100
        else:
            golden_hit_rate = 0
        
        self.log(f"\n🎯 Execution Results:", "cyan")
        self.log(f"   • Total Steps: {total}")
        self.log(f"   • First-Attempt Success: {first_success} ({first_success_rate:.1f}%)", "green" if first_success_rate >= 90 else "yellow")
        self.log(f"   • Required AI Healing: {healing} ({healing_rate:.1f}%)", "yellow" if healing > 0 else "green")
        self.log(f"   • Final Failures: {failures} ({failure_rate:.1f}%)", "red" if failures > 0 else "green")
        
        self.log(f"\n🛤️  Golden Path Effectiveness:", "cyan")
        self.log(f"   • Steps with Mined Locators: {golden_total}")
        self.log(f"   • Golden Path Hits: {golden_hits} ({golden_hit_rate:.1f}%)", "green" if golden_hit_rate >= 90 else "yellow")
        self.log(f"   • Golden Path Misses: {golden_misses}", "yellow" if golden_misses > 0 else "green")
        self.log(f"   • Fallback Used (No Locators): {fallback}", "yellow" if fallback > 0 else "green")
        
        # Overall Assessment
        self.log(f"\n📈 Overall Assessment:", "cyan")
        if first_success_rate >= 90 and golden_hit_rate >= 90:
            self.log(f"   🌟 EXCELLENT! Golden path is working perfectly.", "green")
        elif first_success_rate >= 75 and golden_hit_rate >= 75:
            self.log(f"   ✅ GOOD! Most steps following golden path successfully.", "green")
        elif first_success_rate >= 60 and golden_hit_rate >= 60:
            self.log(f"   ⚠️  FAIR. Golden path needs improvement.", "yellow")
        else:
            self.log(f"   ❌ POOR. Golden path is not effective. Explorer may need better locator mining.", "red")
        
        # Comparison with target
        self.log(f"\n🎯 vs Target (100% Flawless):", "cyan")
        if first_success_rate >= 100:
            self.log(f"   ✅ TARGET ACHIEVED! 100% first-attempt success!", "green")
        else:
            gap = 100 - first_success_rate
            self.log(f"   📊 Gap: {gap:.1f}% from target", "yellow" if gap <= 25 else "red")
            if golden_misses > 0:
                self.log(f"   💡 Recommendation: Review {golden_misses} golden path misses", "cyan")
            if fallback > 0:
                self.log(f"   💡 Recommendation: Explorer needs to mine locators for {fallback} steps", "cyan")
        
        self.log("\n" + "="*60, "blue")

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
                self.log(f"    ✨ AI heal found {len(new_locators)} alternatives. Validating...", "blue")
                
                # 🐛 FIX Bug #2: Validate AI suggestions before accepting
                validated_locators = []
                for loc in new_locators:
                    if await self._validate_healed_locator(page, loc, description, keyword):
                        validated_locators.append(loc)
                
                if not validated_locators:
                    self.log(f"    ⚠️ All AI suggestions failed validation. Using original.", "yellow")
                    return None
                
                self.log(f"    ✅ {len(validated_locators)} validated locators.", "green")
                
                # Update Workflow
                step["locators"] = validated_locators
                with open(self.workflow_path, 'w', encoding='utf-8') as f:
                    json.dump(self.workflow, f, indent=2)
                
                return validated_locators[0]["value"]
        except Exception as e:
            self.log(f"    ⚠️ Healing Error: {e}", "red")
        return None
    
    async def _validate_healed_locator(self, page: Page, locator: Dict, description: str, keyword: str) -> bool:
        """🐛 FIX Bug #2: Validate AI heal suggestions to prevent hallucinations."""
        try:
            selector = locator.get("value")
            if not selector:
                return False
            
            # Check if element exists
            count = await page.locator(selector).count()
            if count == 0:
                self.log(f"      ❌ Rejected: Element not found", "grey")
                return False
            
            # Get element type and text
            element = page.locator(selector).first
            tag_name = await element.evaluate("el => el.tagName.toLowerCase()")
            text_content = (await element.text_content() or "").strip().lower()
            
            # Validation 1: Element type must match action
            if keyword in ["click", "view", "submit"]:
                # Clickable elements should be buttons, links, or divs with click handlers
                if tag_name in ["input", "textarea"] and "type" not in selector:
                    # Input/textarea OK if it has onclick or is wrapped
                    has_click = await element.evaluate("el => el.onclick != null || el.parentElement.onclick != null")
                    if not has_click:
                        self.log(f"      ❌ Rejected: {tag_name} for click action", "grey")
                        return False
            
            # Validation 2: Text content should contain keywords from description
            desc_lower = description.lower()
            keywords = desc_lower.split()
            # At least one keyword should match (filter short words)
            meaningful_keywords = [kw for kw in keywords if len(kw) > 2]
            
            if text_content:
                # Check for strong keyword match
                matched_keywords = [kw for kw in meaningful_keywords if kw in text_content]
                if matched_keywords:
                    self.log(f"      ✅ Validated: '{text_content[:30]}...' matches '{description}'", "green")
                    return True
                else:
                    # 🐛 FIX: More lenient - accept if element type matches action
                    # Don't reject just because keywords don't match exactly
                    if keyword in ["click", "view"] and tag_name in ["button", "a", "div", "span", "li"]:
                        self.log(f"      ✅ Validated: Clickable {tag_name} (lenient)", "green")
                        return True
                    if keyword in ["fill"] and tag_name in ["input", "textarea", "select"]:
                        self.log(f"      ✅ Validated: Input {tag_name} (lenient)", "green")
                        return True
                    
                    # Still reject if really no match
                    self.log(f"      ❌ Rejected: No keyword match in '{text_content[:30]}' for '{description}'", "grey")
                    return False
            
            # If no text match, check if selector itself contains relevant terms
            selector_lower = selector.lower()
            if any(kw in selector_lower for kw in meaningful_keywords):
                self.log(f"      ✅ Validated: Selector contains relevant terms", "green")
                return True
           
            # 🐛 FIX: Reject weak matches instead of accepting
            self.log(f"      ❌ Rejected: No match for '{description}'", "grey")
            return False
            
        except Exception as e:
            self.log(f"      ❌ Validation error: {str(e)[:40]}", "grey")
            return False

    async def _setup_ad_blocking(self, context):
        """Blocks common ad domains to prevent overlays and save bandwidth."""
        ad_domains = [
            "googleads.g.doubleclick.net",
            "google-analytics.com",
            "googletagmanager.com",
            "adsbygoogle.js",
            "amazon-adsystem.com",
            "adnxs.com",
            "pagead2.googlesyndication.com"
        ]
        
        async def block_ads(route):
            if any(domain in route.request.url for domain in ad_domains):
                await route.abort()
            else:
                await route.continue_()
                
        await context.route("**/*", block_ads)

    async def _dismiss_vignettes(self, page: Page):
        """Attempts to dismiss ad overlays (google_vignette) if they appear."""
        try:
            # Check for common vignette IDs/classes
            overlay_selectors = ["#google_vignette", ".google-vignette-container", "ins.adsbygoogle", "div[id^='aswift_']"]
            for sel in overlay_selectors:
                if await page.is_visible(sel, timeout=500):
                    self.log(f"    📢 Detected overlay ({sel}). Forcing removal...", "yellow")
                    # Try to remove the element from DOM to be sure
                    await page.evaluate(f"document.querySelectorAll('{sel}').forEach(el => el.remove())")
                    # Try clicking outside or pressing ESC
                    await page.keyboard.press("Escape")
                    await asyncio.sleep(0.5)
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
