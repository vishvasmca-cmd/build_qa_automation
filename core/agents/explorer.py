import re
import asyncio
import json
import sys
from urllib.parse import urlparse

# Windows Unicode Fix
try:
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

import os
import sys
import base64
import hashlib
import time
import traceback
from playwright.async_api import async_playwright, Page, Frame
from dotenv import load_dotenv
from termcolor import colored

# Force UTF-8 for console output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Import robust LLM wrapper
# Import robust LLM wrapper
from core.lib.llm_utils import SafeLLM, try_parse_json

# Import agents
# Import agents
from core.agents.miner import analyze_page, extract_all_elements
from core.knowledge.knowledge_bank import KnowledgeBank

# Import Metrics Logger
# Import Metrics Logger
from core.lib.metrics_logger import logger

load_dotenv()

# Initialize 2026-ready LLM
# Initialize 2026-ready LLM
llm = SafeLLM(
    model="gemini-2.0-flash",
    temperature=0.0,
    model_kwargs={"response_mime_type": "application/json"}
)

SYSTEM_PROMPT_PLANNER = """
You are a Senior Automation Planner. 
Your goal is to complete the user's workflow by deciding the single next best action.

**INPUTS:**
1. `goal`: The user's workflow goal.
2. `page_context`: A summary of the current page.
3. `elements`: A list of interactive elements found.
4. `history`: Past actions and their outcomes.
5. `test_data`: Available credentials or input data.
6. `knowledge_bank`: Strategic insights and lessons learned from PREVIOUS failures on this site.

**THINKING PROCESS:**
1. Observe: What page am I on?
2. History Check: Review `history` carefully. What have I ALREADY DONE? Use element text and URLs to verify.
3. **KNOWLEDGE CHECK (CRITICAL)**: Analyze `knowledge_bank`. If it contains "Proven Locators" for specific elements, PRIORITIZE them. If it contains "Learned Rules" or "Strategic Insights", you **MUST** follow them to avoid repeating past failures (e.g., "Always close popup X before Y").
4. Validate: Did my LAST action work? Note: On SPAs, the URL might not change even if the content does.
5. Multi-Goal Check: Look at the `goal`. Does it have multiple steps (e.g., '1. Home, 2. Price')? Check off completed steps based on history.
6. **Login Check**: If I encounter a login page and NO credentials are in `test_data` AND NO credentials are in the `goal`, SKIP login entirely. Instead, explore publicly accessible areas. However, if credentials are provided in either `test_data` or the `goal` description, proceed with login.
7. Select: Which element ID from the list corresponds to the NEXT unfulfilled part of the goal? 
8. **STEP TRACKING (CRITICAL)**: You MUST complete the workflow steps IN ORDER. If you land on a page that belongs to a LATER step (e.g., login page but you haven't added to cart yet), you MUST attempt to navigate BACK to the correct page for the EARLIEST unfulfilled step. DO NOT skip ahead just because you are on a convenient page.

**OUTPUT SCHEMA (JSON only)**:
{
  "thought": "Direct explanation of which part of the goal is being addressed and why this action moves us closer, citing any applied knowledge from the Knowledge Bank.",
  "action": "click | fill | scroll | long_press | navigate | done",
  "target_id": 5, 
  "value": "...", 
  "expected_outcome": "Description of expected UI change",
  "is_goal_achieved": false 
}
**CRITICAL**: Set `is_goal_achieved` to `true` ONLY if EVERY part of the user's workflow description is completed. 
- For "Onboarding" goals, filling a form is NOT enough; you MUST click the 'Save' or 'Submit' button.
- You are ONLY done when you see a confirmation message (e.g., "Successfully Saved") or land on the resulting target page (e.g., Employee Profile).
- If the goal involves multiple modules (e.g., PIM and Admin), you MUST navigate to the second module AFTER completing the first.
- **FORBIDDEN**: Do not set `is_goal_achieved: true` if you have not at least visited EVERY top-level feature mentioned in the goal (e.g. if the goal says 'PIM and Admin', you MUST visit both).
"""


class ExplorerAgent:
    def __init__(self, config_path, headed=False):
        with open(config_path, "r") as f:
            self.config = json.load(f)
        self.workflow = self.config.get("workflow_description") or self.config.get("goal") or "Explore the site"
        self.test_data = self.config.get("test_data", {})
        
        # Force headless in CI environments to prevent crashes
        if os.environ.get("GITHUB_ACTIONS") == "true":
            print(colored("🤖 CI Environment detected: Forcing Headless Mode", "yellow"))
            self.headed = False
        else:
            self.headed = headed
            
        self.trace = []
        self.kb = KnowledgeBank()
        # RAG context if available
        self.total_cost = {"input": 0, "output": 0}
        self.output_dir = os.path.join(os.path.dirname(config_path), "outputs")
        os.makedirs(self.output_dir, exist_ok=True)
        
        logger.log_event("Explorer", "init", 0.0, metadata={"config": config_path})
        self.history = []
        
        # State deduplication and loop detection
        self.visited_states = set()  # Track unique page states
        self.loop_detection_window = 3  # Check last N steps for patterns
        
        # Phase 1 Enhancements: Project-Specific Artifacts
        self.project_root = os.path.dirname(config_path)
        self.snapshot_dir = os.path.join(self.project_root, "snapshots")
        os.makedirs(self.snapshot_dir, exist_ok=True)
        self.last_error = None  # Track the last action failure
        
    async def run(self):
        print(colored(f"Explorer: Starting Strategy 2026. Goal: {self.workflow}", "blue", attrs=["bold"]))
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=not self.headed,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-infobars"
                    ]
                )
                
                # Enhanced stealth configuration for headless mode
                context = await browser.new_context(
                    viewport={"width": 1280, "height": 800},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    ignore_https_errors=True,
                    bypass_csp=True,
                    locale="en-US",
                    timezone_id="America/New_York",
                    permissions=["geolocation", "notifications"],
                    # Add realistic browser features
                    extra_http_headers={
                        "Accept-Language": "en-US,en;q=0.9",
                        "Accept-Encoding": "gzip, deflate, br",
                        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                        "sec-ch-ua-mobile": "?0",
                        "sec-ch-ua-platform": '"Windows"',
                    }
                )
                
                # Override navigator properties to hide automation
                await context.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                    Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                    Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                    window.chrome = {runtime: {}};
                """)
                page = await context.new_page()
                page.set_default_timeout(60000) # Standard timeout
                
                try:
                    print(colored(f"🌐 Initial Navigation: {self.config['target_url']}", "cyan"))
                    await page.goto(self.config["target_url"], wait_until="domcontentloaded", timeout=90000)
                except Exception as e:
                    print(colored(f"⚠️ Initial load warning: {e}. Proceeding with current state.", "yellow"))
                    try: await page.wait_for_load_state("domcontentloaded", timeout=30000)
                    except: pass
                
                # --- NAVIGATION GUARD ---
                # If we landed on a vignette or a different page, force back to target
                if "#google_vignette" in page.url or ("/login" in page.url and "/login" not in self.config["target_url"]):
                    print(colored("🛡️ Navigation Guard: Redirect detected. Re-forcing target URL...", "magenta"))
                    await self._dismiss_overlays(page)
                    try: await page.goto(self.config["target_url"], wait_until="domcontentloaded", timeout=90000)
                    except: pass
                
                step = 0
                max_steps = 50 
                lock_retries = 0
                
                # Define target domain for lock
                target_url = self.config.get("target_url")
                target_domain = urlparse(target_url).netloc if target_url else ""
                
                while step < max_steps:
                    # --- DOMAIN LOCK ---
                    current_url = page.url
                    current_domain = urlparse(current_url).netloc
                    
                    # Special check for error pages or blank pages
                    is_error_page = "chromewebdata" in current_url or current_url == "about:blank"
                    
                    if is_error_page or (current_domain and target_domain and current_domain != target_domain):
                        lock_retries += 1
                        if lock_retries > 5:
                            print(colored("❌ Domain Lock: Too many failures. Breaking.", "red"))
                            break
                            
                        reason = "Error Page" if is_error_page else f"External Domain ({current_domain})"
                        print(colored(f"🚫 Domain Lock Triggered! {reason}. Returning to {target_domain} (Attempt {lock_retries}/5)...", "red"))
                        try:
                            await page.goto(self.config.get("target_url"), wait_until="commit", timeout=90000)
                            await asyncio.sleep(5) # Let redirects settle
                        except: pass
                        continue
                    
                    lock_retries = 0 # Reset on success
                    # ------------------
                    print(colored("\n" + "─"*40, "blue"), flush=True)
                    print(colored(f"🚀 [STEP {step + 1}] PROCESSING...", "blue", attrs=["bold"]), flush=True)
                    print(colored("─"*40, "blue"), flush=True)
                    
                    # 1. ANALYZE (Miner) with Timeout Protection
                    try:
                        mindmap = await asyncio.wait_for(
                            analyze_page(page, page.url, self.workflow),
                            timeout=120
                        )
                    except asyncio.TimeoutError:
                        print(colored("⚠️ Vision analysis timed out. Falling back to raw DOM extraction.", "yellow"))
                        try:
                            # Emergency Raw Extraction
                            raw_elements = await extract_all_elements(page)
                            mindmap = {
                                "summary": {"title": await page.title(), "mission_status": "Vision timed out - Raw Mode"},
                                "elements": raw_elements,
                                "blocking_elements": []
                            }
                            print(colored(f"   🚑 Recovered {len(raw_elements)} raw elements.", "green"))
                        except Exception as e:
                            print(colored(f"   ❌ Raw extraction also failed: {e}", "red"))
                            mindmap = {
                                "summary": {"title": "Error", "mission_status": "Fatal Error"},
                                "elements": [],
                                "blocking_elements": []
                            }
                    
                    # Save screenshot for trace
                    page_title = mindmap['summary'].get('title', 'Unknown')
                    page_name = self._get_page_name(page.url, page_title)
                    img_name = f"step_{step:02d}_{page_name}.png"
                    img_path = os.path.join(self.snapshot_dir, img_name)
                    await page.screenshot(path=img_path)
                    
                    print(colored(f"📍 PAGE: {page_title}", "white", attrs=["bold"]), flush=True)
                    print(colored(f"🔍 URL: {page.url}", "grey"), flush=True)
                    
                    # Check for duplicate states (infinite loop prevention)
                    if self.is_duplicate_state(page.url, mindmap):
                        print(colored(f"⚠️ Duplicate state detected (Count: {self.consecutive_duplicate_count}). Attempting rescue...", "yellow"))
                        print(f"   Fingerprint: {self.last_state_fingerprint}")
                        await self._dismiss_overlays(page)
                        await asyncio.sleep(2)
                        # Re-mine after rescue
                        mindmap = await analyze_page(page, page.url, self.workflow)
                        if self.is_duplicate_state(page.url, mindmap) and self.consecutive_duplicate_count >= 20:
                            print(colored(f"❌ Rescue failed: Duplicate limit reached ({self.consecutive_duplicate_count}). Breaking loop.", "red"), flush=True)
                            break
                        print(colored("🚑 Rescue successful! State changed.", "green"))
                    
                    # Check for stuck loops (circular navigation)
                    if self.detect_stuck_loop():
                        print(colored("⚠️ Stuck in repetitive pattern. Breaking out.", "yellow"))
                        break
                    
                    # 2. PLAN (Decider)
                    print(f"📡 Sending {len(mindmap['elements'])} elements to the Planner...")
                    
                    decision_start = time.time()
                    decision = await self._make_decision(mindmap, page.url)
                    
                    decision_duration = time.time() - decision_start
                    print(colored(f"⏱️ Thinking Time: {decision_duration:.1f}s", "grey"), flush=True)
                    
                    if hasattr(self, 'last_rag_context') and self.last_rag_context:
                        print(colored(f"📚 Knowledge Applied: {len(self.last_rag_context)} site-specific rules/locators considered.", "yellow"), flush=True)

                    logger.log_event(
                        agent="Explorer",
                        action="make_decision",
                        duration=decision_duration,
                        metadata={"step": step, "url": page.url}
                    )
                    if not decision: 
                        print(colored("❌ Failed to make a decision. Breaking loop.", "red"), flush=True)
                        break
                    
                    # --- RESCUE MODE (MODAL BLINDNESS FIX) ---
                    # If target_id is null OR not in elements, and we aren't done, try clearing overlays
                    target_id = decision.get('target_id')
                    is_done = decision.get('is_goal_achieved') or decision.get('action') == 'done'
                    
                    if not is_done and target_id is not None:
                        target_exists = any(str(e['elementId']) == str(target_id) for e in mindmap['elements'])
                        if not target_exists:
                            print(colored("🚑 RESCUE MODE: Planner target not found. Clearing overlays and re-mining...", "magenta"))
                            await self._dismiss_overlays(page)
                            await asyncio.sleep(1.5) # Wait for modal settlement
                            mindmap = await analyze_page(page, page.url, self.workflow)
                            print(f"🔄 Re-mined {len(mindmap['elements'])} elements.")
                    # ----------------------------------------
                    
                    thought = decision.get('thought', '')
                    print(colored(f"🧠 MISSION STATUS: {thought}", "cyan"), flush=True)
                    
                    if decision.get('is_goal_achieved') or decision.get('action') == 'done':
                        # Log final state before exiting
                        self.trace.append({
                            "step": step,
                            "thought": decision.get('thought', 'Goal already achieved.'),
                            "action": "done",
                            "url": page.url,
                            "screenshot": img_name,
                            "elements_found": len(mindmap['elements'])
                        })
                        print(colored("🎯 MISSION ACCOMPLISHED: Goal Achieved!", "green", attrs=["bold"]), flush=True)
                        break
                    
                    # 3. ACT
                    action_start = time.time()
                    target_id = decision.get('target_id')
                    target_info = next((f"[{e['tagName']}] {e['text'][:30]}..." for e in mindmap['elements'] if str(e['elementId']) == str(target_id)), "None")
                    print(colored(f"🔨 EXECUTION: {decision.get('action')} target {target_id} ({target_info})", "magenta"), flush=True)
                    
                    action_result = await self._execute_action(page, decision, mindmap['elements'])
                    logger.log_event(
                        agent="Explorer",
                        action="execute_action",
                        duration=time.time() - action_start,
                        success=action_result.get('success'),
                        metadata={"step": step, "action": decision.get('action'), "target": decision.get('target_id'), "locator": action_result.get('locator')}
                    )
                    
                    # 4. VALIDATE & LOG
                    page_title = mindmap['summary'].get('title', 'Unknown')
                    page_name = self._get_page_name(page.url, page_title)
                    
                    self.history.append({
                        "step": step,
                        "action": decision['action'],
                        "target_text": next((e['text'] for e in mindmap['elements'] if str(e['elementId']) == str(decision.get('target_id'))), ""),
                        "url": page.url,
                        "page_name": page_name,
                        "outcome": action_result.get('outcome'),
                        "success": action_result.get('success'),
                    })
                    
                    # Update trace for Refiner
                    self.trace.append({
                        "step": step,
                        "thought": decision['thought'],
                        "action": decision['action'],
                        "page_name": page_name,
                        "locator_used": action_result.get('refined_locator') or action_result.get('locator'),
                        "value": decision.get('value'),
                        "url": page.url,
                        "screenshot": img_name,
                        # Capturing rich context for composite locators
                        "element_context":  {
                            "tag": next((e['tagName'] for e in mindmap['elements'] if str(e['elementId']) == str(decision.get('target_id'))), ""),
                            "text": next((e['text'] for e in mindmap['elements'] if str(e['elementId']) == str(decision.get('target_id'))), ""),
                            "role": next((e.get('role', '') for e in mindmap['elements'] if str(e['elementId']) == str(decision.get('target_id'))), ""),
                        }
                    })
                    self._save_trace()
                    
                    # Passive Collection: Save ALL elements
                    self._save_all_elements(page.url, step, mindmap['elements'])
                    
                    step += 1
                    if not action_result.get('success'):
                        print(colored(f"⚠️ Action failed. Retrying...", "yellow"))

                # Save Trace & Documentation
                self._save_trace()
                self._generate_documentation()
                try:
                    await browser.close()
                except Exception as e:
                    print(colored(f"⚠️ Error closing browser: {e}", "yellow"))
        except Exception as e:
            print(colored(f"❌ Explorer Crashed: {e}", "red"))
            traceback.print_exc()
            raise e

    async def _make_decision(self, mindmap, page_url):
        # Retrieve RAG context from Knowledge Bank
        rag_context = self.kb.get_rag_context(page_url, self.workflow)
        self.last_rag_context = rag_context # Store for logging in main loop
        
        context = {
            "goal": self.workflow,
            "page_context": mindmap['summary'],
            "elements": [{"id": e['elementId'], "text": e['text'], "tag": e['tagName']} for e in mindmap['elements'][:500]],
            "history": self.history[-20:], # Expanded history for long-tail workflows
            "test_data": self.test_data,
            "knowledge_bank": rag_context, # INJECTED: Lessons learned from previous runs
            "last_action_error": self.last_error # INJECTED: Immediate feedback from last attempt
        }
        
        prompt = f"Current Mindmap Context:\n{json.dumps(context, indent=2)}"
        
        try:
            resp = await llm.ainvoke([("system", SYSTEM_PROMPT_PLANNER), ("human", prompt)])
            return try_parse_json(resp.content)
        except Exception as e:
            print(f"Error in decision: {e}")
            return None
    
    def is_duplicate_state(self, page_url, mindmap):
        """
        Check if we are stuck on the same state after an action.
        Repeated visits to the same page (e.g. returning from a modal) are ALLOWED.
        Consecutive identical states are only a problem if the action taken also produced no change.
        """
        element_count = len(mindmap.get('elements', []))
        page_title = mindmap.get('summary', {}).get('title', '')
        
        # Base fingerprint: URL + Structure
        state_fingerprint = f"{page_url}:{element_count}:{page_title}"
        
        # Action fingerprint: What we just did
        last_action = self.history[-1]['action'] if self.history else 'none'
        last_target = self.history[-1].get('target_text', '') if self.history else 'none'
        last_value = str(self.history[-1].get('value', '')) if self.history else 'none'
        action_fingerprint = f"{last_action}:{last_target}"

        # Initialize tracking on first call
        if not hasattr(self, 'last_action_fingerprint'):
            self.last_state_fingerprint = None
            self.last_action_fingerprint = None
            self.consecutive_duplicate_count = 0

        # It's a "bad" duplicate only if BOTH the state AND the action we took are the same as before,
        # OR if we've taken 3+ different actions and the state hasn't changed at all (stuck)
        if state_fingerprint == self.last_state_fingerprint:
            if action_fingerprint == self.last_action_fingerprint:
                # Slow repeats: allow up to 5 identical actions on identical states
                self.consecutive_duplicate_count += 1
                return self.consecutive_duplicate_count >= 5
            
            # Different action on same state (e.g. filling next field)
            self.consecutive_duplicate_count += 1
            if self.consecutive_duplicate_count >= 20: 
                return True
            return False
        else:
            # Progress made! Reset counters.
            self.last_state_fingerprint = state_fingerprint
            self.last_action_fingerprint = action_fingerprint
            self.consecutive_duplicate_count = 0
            return False
            
        return False
    
    def _get_page_name(self, url, title):
        """
        Heuristically determines a valid class name for the current page.
        """
        path = urlparse(url).path.strip('/')
        
        # Priority 1: Known URL segments
        if not path or path == 'index.php':
            return "HomePage"
        if 'login' in path: return "LoginPage"
        if 'product' in path: return "ProductsPage"
        if 'cart' in path: return "CartPage"
        if 'checkout' in path: return "CheckoutPage"
        if 'signup' in path: return "SignupPage"
        if 'contact' in path: return "ContactPage"
        
        # Priority 2: Sanitize Title
        if title:
            # Remove special chars and capitalize
            clean_title = re.sub(r'[^a-zA-Z0-9]', ' ', title).title().replace(' ', '')
            if clean_title:
                return f"{clean_title}Page"
                
        # Priority 3: Path segment
        if path:
            return f"{path.split('/')[-1].title()}Page"
            
        return "GenericPage"

    async def _validate_locator(self, page, locator_str):
        """
        Checks if the locator is actually visible on the page before we try to use it.
        """
        if not locator_str: return False
        
        try:
            # We use a short timeout for validation to keep explorer fast
            is_visible = await page.locator(locator_str).is_visible(timeout=2000)
            return is_visible
        except:
            return False

    def detect_stuck_loop(self):
        """Detect if Explorer is stuck in a repetitive pattern."""
        if len(self.history) < self.loop_detection_window:
            return False
        
        # Get last N actions with URLs
        recent_steps = self.history[-self.loop_detection_window:]
        action_signatures = [f"{h['action']}:{h['url']}" for h in recent_steps]
        
        # Pattern 1: All identical actions = stuck
        if len(set(action_signatures)) == 1:
            print(colored("🔁 Detected stuck loop: identical actions", "yellow"))
            return True
        
        # Pattern 2: Circular A->B->A pattern
        if len(action_signatures) >= 3:
            if action_signatures[0] == action_signatures[2]:
                print(colored("🔁 Detected circular navigation pattern", "yellow"))
        return False

    async def _dismiss_overlays(self, page):
        """Aggressively dismisses modals, overlays, cookie banners, popups, and consent dialogs, including shadow DOMs."""
        try:
            # 1. Structural Removal (Shadow-Piercing "Nuke" Option) with broader selectors
            await page.evaluate("""
                () => {
                    const dismiss = (root) => {
                        const selectors = '[class*="overlay"], [class*="modal"], [id*="cookie"], [class*="banner"], [role="dialog"], [aria-modal="true"], [class*="popup"], [class*="consent"], #hs-eu-cookie-confirmation';
                        const overlays = root.querySelectorAll(selectors);
                        overlays.forEach(el => {
                            const style = window.getComputedStyle(el);
                            if (style.position === 'fixed' || style.position === 'absolute') {
                                if (parseInt(style.zIndex) > 100 || el.innerText.toLowerCase().includes('cookie') || el.innerText.toLowerCase().includes('accept')) {
                                    el.remove();
                                }
                            }
                        });
                        // Recurse into shadows
                        const all = root.querySelectorAll('*');
                        all.forEach(el => {
                            if (el.shadowRoot) dismiss(el.shadowRoot);
                        });
                    };
                    dismiss(document);
                    
                    // 3. Specific Google Vignette Handling
                    const adFrame = document.querySelector('iframe[id*="google_ads_iframe"]');
                    if (adFrame) {
                        try {
                            const innerDoc = adFrame.contentDocument || adFrame.contentWindow.document;
                            const dismissBtn = innerDoc.querySelector('#dismiss-button') || innerDoc.querySelector('.dismiss-button');
                            if (dismissBtn) dismissBtn.click();
                        } catch (e) {}
                        adFrame.remove();
                    }
                    
                    // Clear vignette hash if present
                    if (window.location.hash.includes('google_vignette')) {
                        window.location.hash = '';
                    }
                }
            """)
            # 2. Escape Key (Removed: Too broad, closes legitimate modals)
            # await page.keyboard.press("Escape")
        except Exception as e:
            print(colored(f"   ⚠️ Overlay dismissal warning: {e}", "yellow"))

    async def _execute_with_retry(self, page, func, *args, retries=3, **kwargs):
        """Utility to retry an async action up to `retries` times with a short pause."""
        for attempt in range(1, retries + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                print(colored(f"   ⚠️ Attempt {attempt} failed: {e}", "red"))
                if attempt < retries:
                    # Healing: Try dismissing blocking overlays before retrying
                    print(colored("   🚑 Attempting to clear blocking overlays...", "magenta"))
                    await self._dismiss_overlays(page)
                    await asyncio.sleep(1)
        return {"success": False, "outcome": f"All {retries} attempts failed."}

    async def _execute_action(self, page, decision, elements):
        action = decision['action']
        target_id = decision.get('target_id')
        target_el = next((e for e in elements if str(e['elementId']) == str(target_id)), None)

        if not target_el and action in ['click', 'fill']:
            return {"success": False, "outcome": "Target element ID not found in current DOM"}

        # We no longer dismiss overlays UNCONDITIONALLY before every action.
        # Instead, we will do it as a "healing" step inside _execute_with_retry if needed.

        locator_str = f"[data-agent-id='{target_id}']"
        
        # PRE-EXECUTION VALIDATION
        is_valid = await self._validate_locator(page, locator_str)
        if not is_valid:
            print(colored(f"⚠️ Validation Failed: ID={target_id} not visible. Attempting overlay dismissal...", "yellow"))
            await self._dismiss_overlays(page)
            # Second check
            is_valid = await self._validate_locator(page, locator_str)
            if not is_valid:
                return {"success": False, "outcome": "Locator validation failed (element not visible or blocked)"}

        refined_locator = await self._refine_locator(page, target_el) if target_el else locator_str

        async def perform():
            if action == 'click':
                print(colored(f"🖱️ Clicking ID={target_id} ({target_el['text']})", "yellow"))
                try:
                    await page.locator(locator_str).click(timeout=15000)
                    # Add wait for potential modal triggers
                    if "cart" in target_el.get('text', '').lower() or "add" in target_el.get('text', '').lower():
                        print(colored("   ⌛ Waiting for potential modal/animation...", "grey"))
                        await asyncio.sleep(1.5)
                except Exception as e:
                    # Fix for "intercepts pointer events" (overlays/ads)
                    if "intercepts pointer events" in str(e):
                        print(colored("   🛡️ Click intercepted! Retrying with force=True...", "yellow"))
                        try:
                            await page.locator(locator_str).click(timeout=15000, force=True)
                        except Exception as e2:
                            print(colored(f"   ❌ Force click also failed: {e2}", "red"))
                            # Fallback to coordinate click below...
                    else:
                        print(colored(f"   👉 Locator failed ({e}). Using coordinate fallback.", "magenta"))
                    
                    if target_el.get('center') and target_el['center'].get('x') is not None:
                        await page.mouse.click(target_el['center']['x'], target_el['center']['y'])
                    else:
                        print(colored("   ❌ Coordinate fallback failed: No center coordinates.", "red"))
                
            elif action == 'fill':
                val = decision.get('value', '')
                print(colored(f"⌨️ Filling ID={target_id} with '{val}'", "yellow"))
                try:
                    await page.locator(locator_str).fill(val, timeout=15000)
                except Exception as e:
                    print(colored(f"   👉 Locator failed ({e}). Using coordinate fallback.", "magenta"))
                    if target_el.get('center') and target_el['center'].get('x') is not None:
                        await page.mouse.click(target_el['center']['x'], target_el['center']['y'])
                        await page.keyboard.type(val)
                    else:
                        print(colored("   ❌ Coordinate fallback failed: No center coordinates.", "red"))
            
            elif action == 'navigate':
                url = decision.get('value')
                print(colored(f"🌐 Navigating to {url}", "yellow"))
                # Robust navigate with timeout and wait state
                await page.goto(url, wait_until="load", timeout=60000)
                await asyncio.sleep(1) # Extra settlement time
                
            elif action == 'scroll':
                print(colored("📜 Scrolling down...", "yellow"))
                await page.keyboard.press("PageDown")
                await asyncio.sleep(0.5)
                
            elif action == 'long_press':
                print(colored(f"👆 Long-pressing ID={target_id} (10s)...", "yellow"))
                # Use coordinates for maximum reliability on custom widgets
                center = target_el.get('center', {})
                if center.get('x') is not None and center.get('y') is not None:
                    x, y = center['x'], center['y']
                    await page.mouse.move(x, y)
                    await page.mouse.down()
                    await asyncio.sleep(10)
                    await page.mouse.up()
                else:
                    print(colored("   ❌ Long-press failed: No center coordinates.", "red"))

            return {
                "success": True,
                "outcome": "Action executed",
                "locator": locator_str,
                "refined_locator": refined_locator
            }

        result = await self._execute_with_retry(page, perform)
        if not result.get("success"):
            self.last_error = f"Action '{action}' on ID {target_id} failed: {result.get('outcome')}"
        else:
            self.last_error = None # Reset on success
            
        return result

    async def _refine_locator(self, page: Page, el: dict):
        """
        Converts a transient data-agent-id locator into a stable Playwright locator.
        This is the "Self-Healing" heart of the agent.
        """
        agent_id = el['elementId']
        locator = page.locator(f"[data-agent-id='{agent_id}']")
        
        # We use a JS snippet to extract the best possible Playwright selector from the live element
        # This is more accurate than just guessing from the JSON.
        try:
            refined = await locator.evaluate("""
                (el) => {
                    // --- Tier 1: Attributes (Golden Standard) ---
                    if (el.getAttribute('data-testid')) return `page.get_by_test_id("${el.getAttribute('data-testid')}")`;
                    if (el.getAttribute('data-test')) return `page.locator("[data-test='${el.getAttribute('data-test')}']")`;
                    
                    // ID is good IF it looks stable (not a long random hash)
                    if (el.id && el.id.length < 50 && !/\\d{10,}/.test(el.id)) {
                        return `page.locator("#${el.id}")`;
                    }

                    // --- Tier 2: Semantics (User-Facing) ---
                    const role = el.getAttribute('role') || (el.tagName === 'BUTTON' ? 'button' : el.tagName === 'A' ? 'link' : '');
                    const text = el.innerText || el.textContent || "";
                    const cleanText = text.trim().replace(/\\n/g, ' ').slice(0, 60);
                    
                    // Name/Label/Placeholder
                    if (el.getAttribute('name')) return `page.locator("[name='${el.getAttribute('name')}']")`;
                    if (el.getAttribute('placeholder')) return `page.get_by_placeholder("${el.getAttribute('placeholder')}")`;
                    if (el.getAttribute('aria-label')) return `page.get_by_label("${el.getAttribute('aria-label')}")`;
                    
                    if (el.id) {
                         const label = document.querySelector(`label[for="${el.id}"]`);
                         if (label) return `page.get_by_label("${label.innerText.trim()}")`;
                    }

                    // Role + Name (Accessibility Standard)
                    if (role && cleanText.length > 0) {
                        return `page.get_by_role("${role}", name="${cleanText}")`;
                    }
                    
                    if (cleanText.length > 0 && cleanText.length < 30) {
                        return `page.get_by_text("${cleanText}")`;
                    }

                    // --- Tier 3: Structural/CSS (Hierarchy) ---
                    // Try to find a unique class combination
                    if (el.className && typeof el.className === 'string') {
                        const unstablePrefixes = ['p-', 'm-', 'bg-', 'text-', 'hover:', 'active:', 'focus:', 'static', 'relative', 'absolute', 'flex', 'grid', 'items-', 'justify-'];
                        const classes = el.className.split(' ').filter(c => {
                            const trimmed = c.trim();
                            return trimmed.length > 0 && !unstablePrefixes.some(p => trimmed.startsWith(p));
                        });
                        if (classes.length > 0) {
                             return `page.locator(".${classes.join('.')}")`; 
                        }
                    }

                    // --- Tier 4: XPath / Fallback ---
                    // Simple recursive XPath generator
                    function getXPath(node) {
                        if (node.id && node.id.length < 50 && !/\\d{10,}/.test(node.id)) return `//*[@id="${node.id}"]`;
                        if (node === document.body) return '/html/body';
                        if (!node.parentNode) return '';
                        
                        let ix = 0;
                        const siblings = node.parentNode.childNodes;
                        for (let i = 0; i < siblings.length; i++) {
                            const sibling = siblings[i];
                            if (sibling === node) return getXPath(node.parentNode) + '/' + node.tagName.toLowerCase() + '[' + (ix + 1) + ']';
                            if (sibling.nodeType === 1 && sibling.tagName === node.tagName) ix++;
                        }
                        return '';
                    }
                    
                    const xpath = getXPath(el);
                    if (xpath) return `page.locator("xpath=${xpath}")`;

                    return null;
                }
            """, timeout=5000)
        except Exception as e:
            print(colored(f"   ⚠️ Refinement timeout/error: {str(e)[:50]}...", "magenta"))
            refined = None

        if not refined:
            if el.get('text'):
                refined = f"page.get_by_text('{el['text']}')"
            else:
                refined = f"page.mouse.click({el['center']['x']}, {el['center']['y']})"
            
        print(colored(f"   ✨ Refined: {refined}", "cyan"))
        return refined

    def _save_trace(self):
        # Ensure trace path is absolute and directory exists
        path_from_config = self.config.get("paths", {}).get("trace")
        if path_from_config:
            trace_path = os.path.join(self.project_root, path_from_config)
        else:
            trace_path = os.path.join(self.output_dir, "trace.json")
            
        dirname = os.path.dirname(trace_path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
            
        with open(trace_path, "w", encoding='utf-8') as f:
            json.dump({
                "workflow": self.workflow, 
                "target_url": self.config["target_url"],
                "trace": self.trace
            }, f, indent=2)
        print(colored(f"💾 Trace saved to {trace_path}", "green"))

    def _generate_documentation(self):
        """Generates human-readable Navigate.md and workflow.md"""
        nav_path = os.path.join(self.output_dir, "Navigate.md")
        workflow_path = os.path.join(self.output_dir, "workflow.md")
        
        # 1. Generate Navigate.md
        with open(nav_path, "w", encoding="utf-8") as f:
            f.write(f"# Navigation Log: {self.workflow}\n\n")
            f.write("| Step | Page | Action | Target | Outcome | Screenshot |\n")
            f.write("|------|------|--------|--------|---------|------------|\n")
            
            for item in self.trace:
                step = item["step"]
                page = item.get("page_name", "Unknown")
                action = item.get("action", "Unknown")
                target = item.get("element_context", {}).get("text") or item.get("locator_used", "N/A")
                outcome = "✅" # Assuming success if recorded, or check specific outcome field
                img = item.get("screenshot", "")
                
                # Relative link to snapshot
                img_link = f"[View](../snapshots/{img})" if img else "-"
                
                # Sanitize table content
                target = str(target).replace("|", "/")[:30]
                
                f.write(f"| {step} | {page} | {action} | {target} | {outcome} | {img_link} |\n")
        
        print(colored(f"📝 Generated {nav_path}", "cyan"))
        
        # 2. Generate workflow.md
        with open(workflow_path, "w", encoding="utf-8") as f:
            f.write(f"# Workflow Summary: {self.workflow}\n\n")
            f.write(f"**Goal**: {self.workflow}\n")
            f.write(f"**Total Steps**: {len(self.trace)}\n")
            f.write(f"**Final URL**: {self.trace[-1]['url'] if self.trace else 'N/A'}\n\n")
            
            f.write("## Journey Highlight\n")
            seen_pages = []
            for item in self.trace:
                p = item.get("page_name")
                if p and p not in seen_pages:
                    seen_pages.append(p)
                    f.write(f"- Visited **{p}**\n")
                    
        print(colored(f"📝 Generated {workflow_path}", "cyan"))

    def _save_all_elements(self, url, step, elements):
        """Passive Collection: Save all discovered elements for future reference with rotation logic."""
        path = self.config.get("paths", {}).get("outputs", "outputs")
        file_path = os.path.join(path, "discovered_elements.json")
        
        data = {}
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                try: data = json.load(f)
                except: data = {}
        
        key = f"{url}::step_{step}"
        data[key] = elements
        
        # ROTATION LOGIC: Keep only last 50 steps to prevent massive file growth
        if len(data) > 50:
             # Keep the latest 50 keys
             sorted_keys = sorted(data.keys())[-50:] 
             data = {k: data[k] for k in sorted_keys}
             print(colored(f"🔄 Rotated discovered_elements.json (Trimmed to 50 entries)", "yellow"))

        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        print(colored(f"💾 Passive Collection: {len(elements)} elements saved.", "blue"))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python explorer.py <config_path> [--headed]")
        sys.exit(1)
    
    config_path = sys.argv[1]
    headed = "--headed" in sys.argv
    agent = ExplorerAgent(config_path, headed=headed)
    asyncio.run(agent.run())
