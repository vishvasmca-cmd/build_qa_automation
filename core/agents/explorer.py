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

# Add project root to path (parent of core/agents directory)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)



from core.agents.miner import analyze_page
from core.lib.keywords import KeywordEngine
from core.lib.llm_utils import SafeLLM, try_parse_json
from core.lib.error_handler import ErrorHandler
from core.lib.domain_expert import DomainExpert
from core.lib.exploration_context import ExplorationContext

class ExplorerAgent:
    """
    Validates workflow steps and mines stable locators by actually executing the steps.
    Uses AI (Gemini) when deterministic matching fails to ensure high-quality locator discovery.
    """
    def __init__(self, project_dir: str, headed: bool = False, shallow: bool = False):
        self.project_dir = os.path.abspath(project_dir)
        self.workflow_path = os.path.join(self.project_dir, "workflow.json")
        self.debug_log = os.path.join(self.project_dir, "explorer_debug.log")
        self.headed = headed
        self.shallow = shallow
        
        # Initialize Debug Log
        with open(self.debug_log, 'w', encoding='utf-8') as f:
            f.write(f"Explorer Session started at {datetime.now()}\n")
            f.write("-" * 50 + "\n")

        if not os.path.exists(self.workflow_path):
             self.workflow = {
                "project": os.path.basename(self.project_dir),
                "base_url": "",
                "scenarios": []
            }
        else:
            with open(self.workflow_path, 'r', encoding='utf-8') as f:
                self.workflow = json.load(f)

        self.llm = SafeLLM(
            model="gemini-2.0-flash",
            temperature=0.0,
            model_kwargs={"response_mime_type": "application/json"}
        )
        
        # Initialize exploration context (will be created per scenario)
        self.exploration_context = None

    def log(self, msg: str, color: Optional[str] = None, attrs: Optional[List[str]] = None):
        """Unified logging to console and debug file."""
        if color:
            print(colored(msg, color, attrs=attrs), flush=True)
        else:
            print(msg, flush=True)
            
        with open(self.debug_log, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().isoformat()}] {msg}\n")

    async def explore(self):
        self.log("\n🧭 [EXPLORE] Starting AI-Guided Exploration & Mining", "blue", attrs=["bold"])
        self.log(f"📍 Project: {os.path.basename(self.project_dir)}")
        
        # Track discoveries
        discovery_stats = {"passed": 0, "healed": 0, "failed": 0, "details": []}

        async with async_playwright() as p:
            # Slow-mo for better visibility
            browser = await p.chromium.launch(headless=not self.headed, slow_mo=500)
            context = await browser.new_context(viewport={"width": 1280, "height": 720})
            page = await context.new_page()
            
            if self.shallow:
                self.log("🌊 [SHALLOW] Performing quick landing page mapping...", "cyan")
                url = self.workflow.get("base_url") or "about:blank"
                if url != "about:blank":
                    await page.goto(url, wait_until="domcontentloaded")
                    self.log(f"    🔍 Mapping landmarks on {url}...")
                    # Capture a general mindmap of the homepage
                    mindmap = await analyze_page(page, url, "Homepage landmarks")
                    self.workflow["landmarks"] = mindmap.get("elements", [])[:50] # Store key elements
                
                # Save and exit discovery
                with open(self.workflow_path, 'w', encoding='utf-8') as f:
                    json.dump(self.workflow, f, indent=2)
                await browser.close()
                self.log("🏁 Shallow mapping complete.", "green")
                return

            for scenario in self.workflow.get("scenarios", []):
                self.log(f"\n--- Exploring Scenario: {scenario['name']} ---", "cyan", attrs=["bold"])
                
                await self._explore_scenario(page, scenario, discovery_stats)
                await asyncio.sleep(1)

            # Save updated workflow
            self.log(f"💾 Saving {len(self.workflow.get('scenarios', []))} scenarios to {self.workflow_path}", "cyan")
            with open(self.workflow_path, 'w', encoding='utf-8') as f:
                json.dump(self.workflow, f, indent=2)
            
            await browser.close()
            
            # --- FINAL EXPLORATION SUMMARY ---
            self.log("\n" + "="*40, "blue")
            self.log("📋 EXPLORATION SUMMARY", "blue", attrs=["bold"])
            self.log(f"✅ Successfully Mined: {discovery_stats['passed']}")
            self.log(f"✨ AI Assisted/Healed: {discovery_stats['healed']}")
            self.log(f"❌ Discovery Failures: {discovery_stats['failed']}")
            if discovery_stats["details"]:
                self.log("\nFailure Details:", "red")
                for detail in discovery_stats["details"]:
                    self.log(f"  - {detail}")
            self.log("="*40 + "\n", "blue")
            # ----------------------------------
            
            self.log(f"🏁 Exploration Complete. Locators saved to: {self.workflow_path}", "green", attrs=["bold"])

    async def _explore_scenario(self, page: Page, scenario: Dict, discovery_stats: Dict, depth: int = 0):
        """Recursively explores a scenario, supporting dynamic step injection."""
        
        # SAFETY: Prevent infinite recursion loops
        if depth > 3:
            self.log("    ⛔ Recursion limit reached. Aborting self-healing loop.", "red")
            return

        # Initialize exploration context on first call (depth 0)
        if depth == 0:
            goal = self.workflow.get("goal", "Complete scenario")
            base_url = self.workflow.get("base_url", "")
            self.exploration_context = ExplorationContext(goal, base_url)
            self.log(f"    🧠 Initialized exploration context for goal: '{goal}'", "cyan")

        i = 0
        steps = scenario.get("steps", [])
        while i < len(steps):
            step = steps[i]
            if step.get("skipped"): 
                i += 1
                continue
            keyword = step["keyword"]
            args = step["args"]
            description = args.get("description")
            step_id = step.get("id", f"step_{i+1}")
            is_healed = False
            
            try:
                self.log(f"  ▶️ [STEP {step_id}] {keyword.upper()}: {description or ''}", "white")
                
                # Dismiss overlays/ads before each step
                await self._dismiss_vignettes(page)
                
                # 1. Navigation
                if keyword == "navigate":
                    await page.goto(args["url"], wait_until="domcontentloaded")
                    self.log(f"    ✅ Navigated to {args['url']}", "green")
                    i += 1
                    continue
                
                # 2. Locator Mining (Hybrid Vision + DOM)
                if description:
                    mining_retries = 0
                    max_mining_retries = 3
                    found_stable_locator = False
                    attempted_fix_targets = set()
                    
                    while mining_retries < max_mining_retries and not found_stable_locator:
                        if mining_retries > 0:
                            self.log(f"    🔄 Retry {mining_retries}/{max_mining_retries} mining locators for '{description}'...", "yellow")
                            # Refresh page analysis on retry
                            await asyncio.sleep(1)
                        
                        pre_locator = args.get("locator")
                        candidates = []
                        
                        if pre_locator and mining_retries == 0:
                            self.log(f"    🎯 Using AI-provided locator: {pre_locator}", "cyan")
                            # Quick visibility check - if it works, skip mining
                            try:
                                if await page.is_visible(pre_locator):
                                    candidates = [{"value": pre_locator, "confidence": 0.95, "priority": 0}]
                            except:
                                pass
                        
                        if not candidates:
                            if mining_retries == 0:
                                self.log(f"    🔍 Mining locators for: '{description}'", "magenta")
                            mindmap = await analyze_page(page, page.url, description)
                            elements = mindmap.get("elements", [])
                            screenshot = mindmap.get("screenshot")
                            
                            candidates = self._find_candidates_deterministically(elements, description)
                        
                        if not candidates:
                            self.log(f"    🧠 Consulting AI (Vision-First) to find '{description}'...", "yellow")
                            ai_locators = await self._find_candidates_with_ai(elements, description, scenario['name'], screenshot)
                            if ai_locators:
                                    # Check for Navigation Suggestion
                                if "suggest_navigation" in ai_locators[0]:
                                    nav = ai_locators[0]["suggest_navigation"]
                                    nav_target = nav["target"]
                                    
                                    # DUPLICATE CHECK: Don't inject if we just did this
                                    is_local_dupe = nav_target in attempted_fix_targets
                                    is_global_dupe = (i > 0 and scenario["steps"][i-1].get("keyword") == nav["action"] and \
                                                      scenario["steps"][i-1].get("args", {}).get("description") == nav_target)
                                    
                                    if is_local_dupe or is_global_dupe:
                                        self.log(f"    ⚠️ Skipping duplicate injection: {nav_target}", "yellow")
                                    else:
                                        self.log(f"    💡 Expert Suggestion: {nav['reasoning']}", "cyan")
                                        self.log(f"    🛠️ Executing corrective action: {nav['action']} -> '{nav_target}'", "yellow")
                                        attempted_fix_targets.add(nav_target)
                                        
                                        # Execute the suggested navigation INLINE
                                        await self._dismiss_vignettes(page)
                                        mindmap_nav = await analyze_page(page, page.url, nav["target"])
                                        nav_candidates = self._find_candidates_deterministically(mindmap_nav.get("elements", []), nav["target"])
                                        
                                        if nav_candidates:
                                            # Validate and execute
                                            for cand in nav_candidates:
                                                if "value" not in cand: continue
                                                # Inline validation instead of locator_engine
                                                try:
                                                    loc = page.locator(cand["value"])
                                                    count = await loc.count()
                                                    if count > 0 and await loc.first.is_visible():
                                                        await page.click(cand["value"], timeout=5000, force=True)
                                                        self.log(f"    ✅ Executed corrective navigation", "green")
                                                        await asyncio.sleep(2)
                                                        # Now retry the current step's mining
                                                        break
                                                except Exception:
                                                    continue
                                    
                                    # Since we navigated, we force a retry of mining immediately (or next loop)
                                    # Setting candidates empty ensures we loop again if not stable
                                    candidates = []
                                    
                                else:
                                    is_healed = True
                                    candidates = ai_locators
                        
                        if candidates:
                            # VALIDATION GATE: Filter out hallucinations/stale locators
                            valid_locators = []
                            for cand in candidates:
                                if "value" not in cand: continue
                                # Inline validation instead of locator_engine
                                try:
                                    loc = page.locator(cand["value"])
                                    count = await loc.count()
                                    val = {"exists": count > 0, "unique": count == 1, "visible": False}
                                    if count > 0:
                                        val["visible"] = await loc.first.is_visible()
                                except Exception:
                                    val = {"exists": False, "unique": False, "visible": False}
                                if val["exists"]:
                                    # Update candidate with visibility/uniqueness info
                                    cand["is_unique"] = val["unique"]
                                    cand["is_visible"] = val["visible"]
                                    valid_locators.append(cand)
                            
                            if valid_locators:
                                step["locators"] = sorted({c["value"]: c for c in valid_locators}.values(), key=lambda x: x["priority"])
                                self.log(f"    ✅ Found {len(step['locators'])} verified locators", "green")
                                found_stable_locator = True
                            else:
                                # Only log error if this was the last retry
                                if mining_retries == max_mining_retries - 1:
                                    # ADVANCED SELF-HEALING: Verify step validity if all attempts fail
                                    self.log(f"    🧠 Verifying step validity for '{description}' after mining failure...", "magenta")
                                    verification = await self._verify_step_validity(page, description, screenshot)
                                    
                                    if verification.get("is_valid") and verification.get("new_locator"):
                                        self.log(f"    🛠️ Self-Correction: Step is valid. Using new locator: {verification['new_locator']}", "green")
                                        step["locators"] = [{"value": verification["new_locator"], "confidence": 0.9, "priority": 0}]
                                        found_stable_locator = True
                                    else:
                                        self.log(f"    🗑️ Step deemed INVALID: {verification.get('reason')}. Removing from workflow.", "red")
                                        step["skipped"] = True
                                        break # Exit mining retries
                        else:
                            if mining_retries == max_mining_retries - 1:
                                # ADVANCED SELF-HEALING: Verify step validity if no candidates ever found
                                self.log(f"    🧠 Verifying step validity for '{description}' after no candidates found...", "magenta")
                                verification = await self._verify_step_validity(page, description, screenshot)
                                
                                if verification.get("is_valid") and verification.get("new_locator"):
                                    self.log(f"    🛠️ Self-Correction: Step is valid. Using new locator: {verification['new_locator']}", "green")
                                    step["locators"] = [{"value": verification["new_locator"], "confidence": 0.9, "priority": 0}]
                                    found_stable_locator = True
                                else:
                                    self.log(f"    🗑️ Step deemed INVALID: {verification.get('reason')}. Removing from workflow.", "red")
                                    step["skipped"] = True
                                    break # Exit mining retries
                        
                        mining_retries += 1
    
                # Check if step was skipped (removed) during self-healing
                if step.get("skipped"):
                    self.log(f"    ⏭️ Skipping execution of invalid step: {description}", "yellow")
                    i += 1
                    continue
    
                # 3. Perform Action to transition state
                try:
                    # Re-dismiss just in case action triggers one (though usually happens AFTER)
                    await self._dismiss_vignettes(page)
                    await self._execute_exploration_action(page, step, keyword, args, description)
                    self.log(f"    ✅ State transitioned.", "green")
                    
                    # Record successful action in context
                    if self.exploration_context:
                        selector = step.get("locators", [{}])[0].get("value") if step.get("locators") else None
                        confidence = step.get("locators", [{}])[0].get("confidence") if step.get("locators") else None
                        self.exploration_context.add_action(
                            step_id=step_id, keyword=keyword, description=description or "",
                            selector=selector, success=True, page_url=page.url, confidence=confidence
                        )
                    if is_healed: discovery_stats["healed"] += 1
                    else: discovery_stats["passed"] += 1
                    
                    # PARALLEL AI OPTIMIZATION: Run page analysis and next step suggestion simultaneously
                    analyze_task = analyze_page(page, page.url, "")
                    
                    # Wait for page analysis to complete (needed for next step suggestion)
                    mindmap = await analyze_task
                    
                    # Build context from exploration history
                    if self.exploration_context:
                        context_summary = self.exploration_context.to_prompt_summary()
                    else:
                        context_summary = f"Just completed: {keyword} {description or ''}"
                    
                    # Ask AI for next step using the same mindmap (no duplicate analyze_page call)
                    next_suggestion = await self._ask_llm_next_step(
                        page, 
                        self.workflow.get("goal", ""),
                        context_summary,  # Enhanced with exploration history
                        mindmap.get("elements", []),
                        mindmap.get("screenshot")
                    )
                    
                    if next_suggestion and next_suggestion.get("action") != "done":
                        # ---- Loop detection ----
                        cur_tuple = (next_suggestion.get("action"), next_suggestion.get("target"))
                        if cur_tuple == getattr(self, "_last_ai_suggestion", None):
                            self._repeat_ai_counter = getattr(self, "_repeat_ai_counter", 0) + 1
                        else:
                            self._repeat_ai_counter = 1
                            self._last_ai_suggestion = cur_tuple
                        if self._repeat_ai_counter >= 3:
                            self.log(
                                f"⚠️ Loop detected: same AI suggestion repeated {self._repeat_ai_counter} times. Moving to next step.",
                                "red",
                            )
                            # Reset counters for future suggestions
                            self._repeat_ai_counter = 0
                            self._last_ai_suggestion = None
                            # Skip injecting this suggestion and continue with next step
                            i += 1
                            continue
                            
                        # DUPLICATE CHECK: If the suggestion is exactly what we JUST executed, and we haven't looped, 
                        # we should likely inhibit it to avoid redundancy.
                        
                        # Normalize for comparison
                        je_key = keyword.lower() if keyword else ""
                        je_desc = description.lower() if description else ""
                        
                        sa_key = next_suggestion["action"].lower()
                        sa_desc = (next_suggestion.get("target") or "").lower()
                        
                        just_executed = (je_key, je_desc)
                        suggested_action = (sa_key, sa_desc)
                        
                        if just_executed == suggested_action:
                             self.log(f"    ⚠️ Skipping duplicate AI suggestion (just executed): {suggested_action}", "yellow")
                        else:
                            is_duplicate = False 
                            
                            if not is_duplicate:
                                # Inject AI-suggested step with clean ID
                                if "_ai_" in str(step_id):
                                    parts = str(step_id).split("_ai_")
                                    base = parts[0]
                                    try:
                                        count = int(parts[1])
                                        new_id = f"{base}_ai_{count + 1}"
                                    except:
                                        new_id = f"{step_id}_ai_1"
                                else:
                                    new_id = f"{step_id}_ai_1"
                                    
                                suggested_step = {
                                    "id": new_id,  # Fractional/Suffix ID
                                    "keyword": next_suggestion["action"],
                                    "args": {
                                        "description": next_suggestion.get("target", ""),
                                        "locator": next_suggestion.get("locator"), 
                                        "value": next_suggestion.get("value", "")
                                    }
                                }
                                
                                self.log(f"    ➕ Injected AI step: {suggested_step['keyword']} -> {suggested_step['args']['description']}", "cyan")
                                
                                # Modify the scenario in-place
                                steps.insert(i + 1, suggested_step)
                                
                                # No recursion needed! The while loop will naturally pick up steps[i+1]
                                # on the next iteration after we do i += 1.
                                # We break the current 'after-action' logic to proceed to the next step.
                                i += 1
                                continue
                        
                except Exception as e:
                    self.log(f"    ⚠️ Action failed: {str(e)[:50]}...", "yellow")
                    
                    # Record failed action in context
                    if self.exploration_context:
                        selector = step.get("locators", [{}])[0].get("value") if step.get("locators") else None
                        self.exploration_context.add_action(
                            step_id=step_id, keyword=keyword, description=description or "",
                            selector=selector, success=False, page_url=page.url, error=str(e)[:100]
                        )
                    healed_selector = await self._heal_exploration_action(page, step, description, scenario['name'], keyword)
                    if healed_selector:
                         self.log(f"    ✨ AI healed exploration action! New selector: {healed_selector}", "green")
                         try:
                             await self._execute_exploration_action(page, step, keyword, args, description, healed_selector)
                             discovery_stats["healed"] += 1
                         except: 
                             discovery_stats["failed"] += 1
                             discovery_stats["details"].append(f"Step {step_id}: Action failed after healing")
                    else:
                        discovery_stats["failed"] += 1
                        discovery_stats["details"].append(f"Step {step_id}: Action failed and no healing")
            except Exception as outer_e:
                err_msg = str(outer_e)
                if "Target page, context or browser has been closed" in err_msg or "Connection closed" in err_msg:
                    self.log(f"    🛑 Critical: Browser disconnected or closed. Aborting exploration.", "red")
                    break
                else:
                    self.log(f"    ⚠️ Critical step failure: {err_msg[:100]}", "red")
                    discovery_stats["failed"] += 1
                    discovery_stats["details"].append(f"Step {step_id}: {err_msg}")

            # Move to next step
            i += 1

        await asyncio.sleep(1)

    def _find_candidates_deterministically(self, elements: List[Dict], description: str) -> List[Dict]:
        """Builds a list of candidate locators for an element, prioritizing stable CSS & patient locators."""
        candidates = []
        desc_lower = description.lower()
        
        for el in elements:
            attrs = el.get("attributes", {})
            semantic_label = (el.get("text") or "").strip() # accessible name
            semantic_lower = semantic_label.lower()
            
            placeholder = (attrs.get("placeholder") or "").lower()
            title = (attrs.get("title") or "").lower()
            aria = (getattr(el, "aria_label", "") or "").lower() # some miners put it top level? Check miner.
            # Miner puts aria-label in getSemanticLabel/text, but also maybe in attributes?
            # Let's rely on semantic_label for the primary text match.
            
            val = (attrs.get("value") or "").lower()
            tag = el.get("tagName", "").lower()
            
            # Semantic Match
            id_val = (attrs.get("id") or "").lower()
            name_val = (attrs.get("name") or "").lower()
            
            # Check for direct semantic match OR common functional keywords in IDs/Names
            is_match = (desc_lower in semantic_lower or desc_lower in placeholder or desc_lower in title or 
                        desc_lower in val or
                        (desc_lower == "search" and ("search" in id_val or "search" in name_val)) or
                        (desc_lower == "submit" and ("submit" in id_val or "submit" in name_val)))

            if is_match:
                # 1. Test IDs (Gold Standard)
                if attrs.get("data-testid"):
                    candidates.append({"type": "testid", "value": f"[data-testid='{attrs['data-testid']}']", "priority": 1})
                elif attrs.get("data-qa"):
                    candidates.append({"type": "testid", "value": f"[data-qa='{attrs['data-qa']}']", "priority": 1})
                
                # 2. Playwright Patient Locators (Roles)
                # Infer implicit roles if explicit role is missing
                inferred_role = el.get("role")
                if not inferred_role:
                    if tag == "button": inferred_role = "button"
                    elif tag == "a": inferred_role = "link"
                    elif tag == "header": inferred_role = "heading" # approximate
                    elif tag == "input":
                        itype = attrs.get("type", "text")
                        if itype == "checkbox": inferred_role = "checkbox"
                        elif itype == "radio": inferred_role = "radio"
                        elif itype in ["submit", "button", "reset", "image"]: inferred_role = "button"
                        elif itype in ["text", "email", "password", "search", "tel", "url"]: inferred_role = "textbox"
                    elif tag == "textarea": inferred_role = "textbox"
                    elif tag == "img": inferred_role = "img"
                
                if inferred_role:
                    # escape single quotes for the selector string
                    safe_label = semantic_label.replace("'", "\\'")
                    if safe_label:
                        candidates.append({"type": "role", "value": f"role={inferred_role}[name='{safe_label}']", "priority": 1})
                    else:
                        # Role without name is weak, but maybe unique?
                        candidates.append({"type": "role", "value": f"role={inferred_role}", "priority": 4})

                # 3. Exact Text (Patient)
                if semantic_label:
                     safe_text = semantic_label.replace("'", "\\'")
                     if desc_lower == semantic_lower:
                        candidates.append({"type": "text", "value": f"text='{safe_text}'", "priority": 2})
                     else:
                        # Partial match via internal text engine
                        candidates.append({"type": "text", "value": f"text={safe_text}", "priority": 3})

                # 4. Form Attributes (Patient/CSS)
                if attrs.get("placeholder"):
                    candidates.append({"type": "placeholder", "value": f"[placeholder='{attrs['placeholder']}']", "priority": 2})
                if attrs.get("title"):
                    candidates.append({"type": "title", "value": f"[title='{attrs['title']}']", "priority": 3})
                if attrs.get("alt"):
                     candidates.append({"type": "alt", "value": f"[alt='{attrs['alt']}']", "priority": 3})

                # 5. Unique IDs
                if attrs.get("id") and not any(c.isdigit() for c in attrs["id"][-3:]): # Skip dynamic IDs
                    candidates.append({"type": "css", "value": f"#{attrs['id']}", "priority": 2})
                
                # 6. Fallback CSS
                tag = el.get("tagName", "*")
                if attrs.get("name"):
                    candidates.append({"type": "css", "value": f"{tag}[name='{attrs['name']}']", "priority": 3})

                # 7. Clean CSS Selectors from Miner (Weakest if generated path is brittle)
                if el.get("selector") and "nth=" not in el["selector"]:
                    candidates.append({"type": "css", "value": el["selector"], "priority": 4})

        return candidates

    async def _find_candidates_with_ai(self, elements: List[Dict], description: str, scenario_name: str, screenshot: str = None) -> List[Dict]:
        """Uses LLM (Vision + DOM) to find multiple potential elements, ranked by priority."""
        try:
            goal = self.workflow.get("goal", "Complete the scenario")
            url = self.workflow.get("base_url", "")
            
            # Domain Expert Persona Injection
            domain = DomainExpert.detect_domain(url, "", goal)
            persona = DomainExpert.get_persona_prompt(domain)
            
            # VISIBLE FEEDBACK for the user
            self.log(f"    🧠 [EXPERT] Strategy: {persona}", "cyan")
            
            message_content = [
                {
                    "type": "text", 
                    "text": f"""
                    **ROLE & STRATEGY:**
                    {persona}
                    
                    **MISSION:**
                    Goal: "{goal}"
                    Current Task: Find "{description}"
                    
                    **YOUR TASK:**
                    1. Identify the *best* CSS selectors for "{description}".
                    2. **CRITICAL:** If "{description}" is NOT on this page, suggest a NAVIGATION BUTTON that leads to it (e.g. "Click 'Products' to find search").
                    
                    **LOCATOR REQUIREMENTS:**
                    1. Provide MULTIPLE high-quality CSS selectors with CONFIDENCE SCORES (0.0-1.0).
                    2. Confidence 1.0 = Perfect match (e.g., unique ID, data-testid).
                    3. Confidence 0.5-0.8 = Good match (e.g., stable class, semantic attribute).
                    4. Confidence <0.5 = Weak match (e.g., generic class, text-based).
                    5. If action is 'fill', finding an <input> is MANDATORY.
                    6. Focus on what is VISIBLE.
                    
                    **RESPONSE FORMAT (Strict JSON):**
                    {{
                        "found": true,
                        "locators": [...],
                        "suggest_navigation": {{ "needed": false }}
                    }}
                    OR IF MISSING:
                    {{
                        "found": false,
                        "suggest_navigation": {{
                            "needed": true,
                            "action": "click",
                            "target": "Products",
                            "reasoning": "Search bar is likely on the Products page."
                        }}
                    }}
                    """
                }
            ]
            
            if screenshot:
                message_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{screenshot}"}})

            resp = await self.llm.ainvoke([{"role": "user", "content": message_content}])
            fix = try_parse_json(resp.content)
            
            if fix:
                if fix.get("found") and fix.get("locators"):
                    return fix["locators"]
                elif fix.get("suggest_navigation", {}).get("needed"):
                    # Return special signal for navigation injection
                    return [{"suggest_navigation": fix["suggest_navigation"]}]
                    
        except Exception as e:
            self.log(f"    ⚠️ AI Vision Mining Error: {e}", "red")
        return []

    async def _ask_llm_next_step(self, page: Page, goal: str, current_context: str, elements: List[Dict], screenshot: str = None) -> Optional[Dict]:
        """Ask LLM what the next action should be based on current page state."""
        try:
            url = page.url
            
            # Domain Expert Persona Injection
            domain = DomainExpert.detect_domain(url, "", goal)
            persona = DomainExpert.get_persona_prompt(domain)
            
            # Extract visible text from elements with selectors for LLM context
            visible_text = []
            for el in elements[:25]:  # Slightly more elements
                text = (el.get("text") or "").strip()
                tag = el.get("tagName", "").lower()
                sel = el.get("selector", "")
                
                # Build a descriptive element string
                parts = [f"<{tag}"]
                if el.get("attributes", {}).get("id"):
                    parts.append(f" id='{el['attributes']['id']}'")
                if el.get("attributes", {}).get("name"):
                    parts.append(f" name='{el['attributes']['name']}'")
                parts.append(">")
                
                label = f"{' '.join(parts)}: \"{text}\"" if text else ' '.join(parts)
                # Add selector in parenthesis for LLM to use
                if sel:
                    label += f" [Selector: {sel}]"
                
                visible_text.append(label)
            
            visible_summary = "\n".join(visible_text) if visible_text else "No interactive elements identified in DOM."
            
            message_content = [
                {
                    "type": "text",
                    "text": f"""
                    **ROLE & STRATEGY:**
                    {persona}
                    
                    **MISSION:**
                    Overall Goal: "{goal}"
                    Current Context: {current_context}
                    
                    **CURRENT PAGE STATE:**
                    URL: {url}
                    Visible Elements:
                    {visible_summary}

                    **ACTION HISTORY (Last 5 Steps):**
                    {current_context}

                    **YOUR TASK:**
                    Based on the current page state and history, what is the NEXT immediate action to progress toward expectations?
                    
                    **RESPONSE FORMAT (Strict JSON):**
                    {{
                        "action": "click" | "fill" | "navigate" | "done",
                        "target": "description of element to interact with",
                        "locator": "CSS selector (optional but preferred)",
                        "value": "value to fill (only for 'fill' action)",
                        "reasoning": "why this is the logical next step"
                    }}
                    
                    **CRITICAL GUIDELINES:**
                    1. **ANTI-LOOPING:** Do NOT suggest an action that appears in the 'ACTION HISTORY' as ✅ (Success) unless it's a form input or strictly necessary repetitive task. 
                    2. If the last action was 'click Products' and you are on the Products page, DO NOT suggest 'click Products' again. Look for the next step (e.g. Search, Add to Cart).
                    3. **SPECIFICITY:** Avoid suggesting actions on generic text like "here", "click here", "read more" or "learn more" unless they are uniquely and obviously the only path forward. Favor named buttons/links (e.g., "Add to Cart", "Checkout", "Products").
                    4. If the goal is checkout and a popup asks to 'Login / Register', you MUST click 'Register / Login'.
                    5. Only dismiss popups if they are actual ads.
                    6. If the goal is achievable with the visible elements, do it.
                    7. **HALLUCINATIONS:** Only suggest acting on elements listed in 'Visible Elements' or strongly implied by the DOM. Do NOT invent 'All Products' buttons if they don't exist.
                    
                    If the goal is unlikely to be achieved from here or is already done, return {{"action": "done"}}.
                    """
                }
            ]
            
            if screenshot:
                message_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{screenshot}"}})
            
            resp = await self.llm.ainvoke([{"role": "user", "content": message_content}])
            suggestion = try_parse_json(resp.content)
            
            if suggestion:
                action = suggestion.get("action")
                target = suggestion.get("target", "N/A")
                locator = suggestion.get("locator")
                
                self.log(f"    🤖 AI Next Step Suggestion: {action} -> {target}", "magenta")
                if locator:
                    self.log(f"    🧩 Suggested Locator: {locator}", "cyan")
                self.log(f"    💭 Reasoning: {suggestion.get('reasoning', 'No reasoning provided')}", "blue")
                return suggestion
                
        except Exception as e:
            self.log(f"    ⚠️ Contextual Planning Error: {e}", "red")
        return None

    async def _highlight_element(self, page: Page, selector: str):
        """Visually highlights an element on the page for debugging."""
        try:
            await page.evaluate(f"""
                (selector) => {{
                    const el = document.querySelector(selector);
                    if (el) {{
                        const prevOutline = el.style.outline;
                        const prevBg = el.style.backgroundColor;
                        el.style.outline = '4px solid #f39c12';
                        el.style.backgroundColor = 'rgba(243, 156, 18, 0.4)';
                        setTimeout(() => {{
                            el.style.outline = prevOutline;
                            el.style.backgroundColor = prevBg;
                        }}, 1500);
                    }}
                }}
            """, selector)
            await asyncio.sleep(0.5) # Wait for highlight to be seen
        except:
            pass

    async def _dismiss_vignettes(self, page: Page):
        """Attempts to dismiss ad overlays (google_vignette) if they appear."""
        try:
            overlay_selectors = ["#google_vignette", ".google-vignette-container", "ins.adsbygoogle"]
            for sel in overlay_selectors:
                if await page.is_visible(sel, timeout=1000):
                    self.log(f"    📢 Detected overlay ({sel}). Dismissing...", "yellow")
                    await page.keyboard.press("Escape")
                    await asyncio.sleep(1)
                    dismiss_btn = "div[id='dismiss-button'], div.dismiss-button"
                    if await page.is_visible(dismiss_btn, timeout=1000):
                        await page.click(dismiss_btn, force=True)
                        self.log("    ✅ Dismiss button clicked.", "green")
        except:
            pass

    async def _execute_exploration_action(self, page: Page, step: Dict, keyword: str, args: Dict, description: str, override_selector: str = None):
        selector = override_selector or (step["locators"][0]["value"] if step.get("locators") else f"text={description}")
        
        # Handle collections (e.g., multiple products)
        if not override_selector and step.get("locators") and step["locators"][0].get("is_collection"):
            try:
                count = await page.locator(selector).count()
                if count > 1:
                    idx = 0 # Default to first
                    
                    # Detect ordinal intent in description
                    desc = description.lower() if description else ""
                    if "random" in desc:
                        import random
                        idx = random.randint(0, count - 1)
                        self.log(f"    🎲 Randomly selected item {idx+1} of {count} from collection.", "blue")
                    elif "second" in desc or "2nd" in desc:
                        idx = 1
                    elif "third" in desc or "3rd" in desc:
                        idx = 2
                    else:
                        self.log(f"    🎯 Defaulting to first item (1 of {count}) in collection.", "blue")
                    
                    selector = f"{selector} >> nth={idx}"
                    
                    # Persist this specific choice
                    step["locators"][0]["value"] = selector
                    step["locators"][0]["is_collection"] = False
            except: pass

        # Pre-interaction highlight
        await self._highlight_element(page, selector)

        # HUMAN-LIKE INTERACTIONS
        target = page.locator(selector).first
        try:
            await target.scroll_into_view_if_needed(timeout=5000)
        except:
            self.log(f"    ⚠️ Scroll into view failed for {selector}. Proceeding anyway.", "yellow")
        
        if keyword == "click":
            # Move mouse to element and click
            box = await target.bounding_box(timeout=5000)
            if box:
                await page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                await page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            else:
                # Force click if no bounding box (likely obscured/hidden)
                await target.click(force=True, timeout=5000)
            
            # Wait for potential navigation
            try:
                await page.wait_for_load_state("domcontentloaded", timeout=3000)
            except: pass
            
        elif keyword in ["fill", "type"]:
            val = args.get("value", "test")
            await target.click(timeout=5000) # Focus first
            await page.keyboard.press("Control+A")
            await page.keyboard.press("Backspace")
            import random
            await page.keyboard.type(str(val), delay=random.randint(50, 150))
        elif keyword == "hover":
            box = await target.bounding_box(timeout=5000)
            if box:
                await page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            else:
                await target.hover(timeout=5000)
        
        await asyncio.sleep(2.0) # Increased stability wait

    async def _heal_exploration_action(self, page: Page, step: Dict, description: str, scenario_name: str, keyword: str = "") -> Optional[str]:
        """Vision-centric healing during discovery."""
        try:
            goal = self.workflow.get("goal", "Complete the scenario")
            mindmap = await analyze_page(page, page.url, description)
            elements = mindmap.get("elements", [])
            screenshot = mindmap.get("screenshot")
            
            message_content = [
                {
                    "type": "text",
                    "text": f"""
                    **MISSION:**
                    Goal: "{goal}"
                    
                    **TASK:**
                    Identify the best VISIBLE element for "{description}" on the current page to perform "{keyword}".
                    If action is "fill", it MUST be an input/textarea.
                    
                    **RESPONSE FORMAT (JSON):**
                    {{
                        "found": true,
                        "selector": "css selector",
                        "reasoning": "how this element matches visually"
                    }}
                    """
                }
            ]
            
            if screenshot:
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{screenshot}"}
                })

            resp = await self.llm.ainvoke([{"role": "user", "content": message_content}])
            fix = try_parse_json(resp.content)
            
            if fix and fix.get("found") and fix.get("selector"):
                self.log(f"    ✨ AI Heal Reasoning: {fix.get('reasoning')}", "blue")
                return fix["selector"]
        except Exception as e:
            self.log(f"    ⚠️ AI Healing Error: {e}", "red")
        return None

    async def _verify_step_validity(self, page: Page, description: str, screenshot: str = None) -> Dict:
        """Uses AI (Vision) to verify if a step is valid or should be removed."""
        try:
            url = page.url
            goal = self.workflow.get("goal", "Complete the scenario")
            
            message_content = [
                {
                    "type": "text", 
                    "text": f"""
                    **MISSION:**
                    Goal: "{goal}"
                    Current Page URL: {url}
                    Current Task: Locate and interact with "{description}"
                    
                    **CONTEXT:**
                    We have failed to find a stable locator for "{description}" after multiple attempts.
                    
                    **YOUR TASK:**
                    Analyze the current page state (see screenshot). 
                    1. Does "{description}" (the intended interaction target) actually exist on this page?
                    2. Is this step logical and valid given the current page state?
                    3. If YES, provide a new high-quality CSS selector.
                    4. If NO, explain why (e.g., "We are on the wrong page", "The element doesn't exist").
                    
                    **RESPONSE FORMAT (Strict JSON):**
                    {{
                        "is_valid": true | false,
                        "new_locator": "CSS selector if valid, otherwise null",
                        "reason": "Short explanation for your decision"
                    }}
                    """
                }
            ]
            
            if screenshot:
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{screenshot}"}
                })

            resp = await self.llm.ainvoke([{"role": "user", "content": message_content}])
            result = try_parse_json(resp.content)
            
            if result:
                return {
                    "is_valid": result.get("is_valid", False),
                    "new_locator": result.get("new_locator"),
                    "reason": result.get("reason", "No reason provided")
                }
        except Exception as e:
            self.log(f"    ⚠️ AI Step Verification Error: {e}", "red")
            
        return {"is_valid": True, "new_locator": None, "reason": "Error during verification"}

async def main():
    parser = argparse.ArgumentParser(description="AI Explorer Agent")
    parser.add_argument("--project", required=True, help="Project directory")
    parser.add_argument("--headed", action="store_true", help="Run in headed mode")
    parser.add_argument("--shallow", action="store_true", help="Quick landing page scan only")
    
    args = parser.parse_args()
    
    agent = ExplorerAgent(args.project, headed=args.headed, shallow=args.shallow)
    await agent.explore()

if __name__ == "__main__":
    asyncio.run(main())
