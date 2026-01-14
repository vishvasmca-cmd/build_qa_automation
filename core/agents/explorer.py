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
from core.agents.miner import analyze_page
from core.knowledge.knowledge_bank import KnowledgeBank

# Import Metrics Logger
# Import Metrics Logger
from core.lib.metrics_logger import logger

# Import Robust Action Handler
from core.lib.robust_handler import get_handler as get_robust_handler

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
2. **ERROR CHECK (PRIORITY)**: Check `last_action_error`. If it contains a hint like "Try clicking element X first", you MUST follow that hint immediately.
3. History Check: Review `history` carefully. What have I ALREADY DONE? Use element text and URLs to verify.
4. **KNOWLEDGE CHECK (CRITICAL)**: Analyze `knowledge_bank`. If it contains "Proven Locators" for specific elements, PRIORITIZE them. If it contains "Learned Rules" or "Strategic Insights", you **MUST** follow them to avoid repeating past failures (e.g., "Always close popup X before Y").
5. Validate: Did my LAST action work? Note: On SPAs, the URL might not change even if the content does.
6. Multi-Goal Check: Look at the `goal`. Does it have multiple steps (e.g., '1. Home, 2. Price')? Check off completed steps based on history.
7. **Login Check**: If I encounter a login page and NO credentials are in `test_data` AND NO credentials are in the `goal`, SKIP login entirely. Instead, explore publicly accessible areas. However, if credentials are provided in either `test_data` or the `goal` description, proceed with login.
8. **Validation Check**: Check the `disabled` field in the element list. YOU MUST NOT 'click' or 'fill' an element if `disabled` is true. If the element you want is disabled, LOOK for a nearby button/icon that might enable it (e.g., a "Search" icon to open a search bar, or an "Edit" button to enable a form).
9. Select: Which element ID from the list corresponds to the NEXT unfulfilled part of the goal? 
10. **STEP TRACKING (CRITICAL)**: You MUST complete the workflow steps IN ORDER. If you land on a page that belongs to a LATER step (e.g., login page but you haven't added to cart yet), you MUST attempt to navigate BACK to the correct page for the EARLIEST unfulfilled step. DO NOT skip ahead just because you are on a convenient page.

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
        self.loop_detection_window = 5  # Check last N steps for patterns
        
        self.project_root = os.path.dirname(config_path)
        self.snapshot_dir = os.path.join(self.project_root, "snapshots")
        os.makedirs(self.snapshot_dir, exist_ok=True)
        self.last_error = None  # Track the last action failure
        
        # Initialize Robust Action Handler
        self.robust_handler = get_robust_handler()
        self.robust_handler.set_domain(self.config.get("target_url", ""))
        self.robust_handler.reset()  # Fresh start for this session
        
        # Self-Learning & Optional Steps Enhancement
        self.parsed_goal = self._parse_goal_with_metadata(self.workflow)
        self.step_learnings = {}  # Store learnings per step number
        self.skipped_steps = []  # Track which optional steps were skipped
        
        # Extract search query from goal if present
        import re
        search_match = re.search(r"[Ss]earch[^'\"]*['\"]([^'\"]+)['\"]", self.workflow)
        if search_match:
            self.test_data['search_query'] = search_match.group(1)
            print(colored(f"🔍 Extracted search query: '{self.test_data['search_query']}'", "cyan"))
        
        print(colored(f"📋 Parsed {len(self.parsed_goal)} goal steps", "cyan"))
        for step in self.parsed_goal:
            flags = []
            if step['is_optional']: flags.append("Optional")
            if step['self_learning_enabled']: flags.append("Self-Learning")
            flag_str = f" [{', '.join(flags)}]" if flags else ""
            print(colored(f"  Step {step['step_num']}: {step['description'][:60]}{flag_str}", "grey"))

        
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
                        "--disable-infobars",
                        "--start-maximized"
                    ]
                )
                
                # Enhanced stealth configuration for headless mode
                # Use no_viewport for maximized window, or large viewport
                context = await browser.new_context(
                    no_viewport=True if self.headed else False,
                    viewport=None if self.headed else {"width": 1920, "height": 1080},
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
                
                # Handle JS Alerts/Dialogs automatically
                page.on("dialog", lambda dialog: asyncio.create_task(dialog.accept()))
                
                # 🎯 VISUAL CURSOR: Add a visible cursor indicator for headed mode
                if self.headed:
                    await page.add_init_script("""
                        window.showAgentCursor = (x, y, action = 'click') => {
                            // Remove existing cursor
                            const existing = document.getElementById('agent-cursor');
                            if (existing) existing.remove();
                            
                            // Create cursor element
                            const cursor = document.createElement('div');
                            cursor.id = 'agent-cursor';
                            cursor.style.cssText = `
                                position: fixed;
                                left: ${x - 15}px;
                                top: ${y - 15}px;
                                width: 30px;
                                height: 30px;
                                border: 3px solid #FF4444;
                                border-radius: 50%;
                                background: rgba(255, 68, 68, 0.3);
                                pointer-events: none;
                                z-index: 999999;
                                transition: all 0.3s ease;
                                animation: pulse 0.5s ease-out;
                            `;
                            
                            // Add pulse animation
                            const style = document.createElement('style');
                            style.textContent = `
                                @keyframes pulse {
                                    0% { transform: scale(1); opacity: 1; }
                                    50% { transform: scale(1.5); opacity: 0.7; }
                                    100% { transform: scale(1); opacity: 1; }
                                }
                            `;
                            document.head.appendChild(style);
                            document.body.appendChild(cursor);
                            
                            // Remove after animation
                            setTimeout(() => cursor.remove(), 1000);
                        };
                    """)
                
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
                        print(colored("⚠️ Vision analysis timed out. Falling back to simple extraction.", "yellow"))
                        # Basic fallback: dummy mindmap with just title and empty elements
                        # (Miner already has internal fallbacks, but this keeps explorer moving)
                        mindmap = {
                            "summary": {"title": await page.title(), "mission_status": "Vision timed out."},
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
                    is_dup_state = self.is_duplicate_state(page.url, mindmap)
                    
                    # Trigger Self-Learning on recurrent duplicates (Check counter directly)
                    if self.consecutive_duplicate_count == 5:
                         current_step_meta = self._get_current_step_metadata(mindmap, page.url)
                         if current_step_meta and current_step_meta['self_learning_enabled']:
                             step_num = current_step_meta['step_num']
                             if step_num not in self.step_learnings: self.step_learnings[step_num] = []
                             
                             print(colored(f"🧠 DUP STATE DETECTED: Triggering Self-Learning for Step {step_num}", "magenta", attrs=["bold"]))
                             
                             # Analyze failure
                             analysis = await self._analyze_failure_with_llm(
                                 current_step_meta,
                                 self.history[-5:],
                                 mindmap,
                                 self.step_learnings[step_num]
                             )
                             
                             self.step_learnings[step_num].append({
                                 "attempt": len(self.step_learnings[step_num]) + 1,
                                 "diagnosis": "Stuck in Duplicate State: " + analysis.get('diagnosis', 'State not changing'),
                                 "suggestion": analysis.get('suggestion'),
                                 "timestamp": time.time()
                             })
                             
                             # Enhanced Decision
                             await asyncio.sleep(2)
                             mindmap = await analyze_page(page, page.url, self.workflow)
                             enhanced_decision = await self._make_decision_with_learning(
                                 mindmap, page.url, current_step_meta, self.step_learnings[step_num]
                             )
                             
                             if enhanced_decision:
                                 print(colored(f"🚑 Breaking duplicate state with enhanced decision: {enhanced_decision['action']}", "green"))
                                 action_result = await self._execute_action(page, enhanced_decision, mindmap['elements'])
                                 self.history.append({
                                     "step": step,
                                     "thought": enhanced_decision['thought'] + " [Dup Break]",
                                     "action": enhanced_decision['action'],
                                     "target_text": enhanced_decision.get('target_id'),
                                     "success": action_result.get('success')
                                     
                                 })
                                 step += 1
                                 continue

                    if is_dup_state:
                        print(colored(f"⚠️ Duplicate state detected (count: {self.consecutive_duplicate_count})", "yellow"))
                        
                        # LEVEL 1: Overlay Dismissal (Standard)
                        if self.consecutive_duplicate_count >= 2:
                            print(colored("   🛡️ Attempting overlay dismissal...", "magenta"))
                            await self._dismiss_overlays(page)
                            await asyncio.sleep(2)
                        
                        # LEVEL 2: Page Refresh (Aggressive) - Triggered much earlier per user request
                        if self.consecutive_duplicate_count >= 5: 
                             print(colored("🔄 STUCK LOOP PERSISTS: Refreshing page...", "magenta", attrs=["bold"]))
                             try:
                                await page.reload(wait_until="domcontentloaded", timeout=60000)
                                await asyncio.sleep(3)
                             except Exception as e:
                                print(colored(f"   ⚠️ Refresh failed: {e}", "yellow"))

                        # LEVEL 3: Hard Navigation (Nuclear)
                        if self.consecutive_duplicate_count >= 8:
                             print(colored("☢️ CRITICAL STUCK: Hard navigation to target URL...", "red", attrs=["bold"]))
                             try:
                                await page.goto(self.config["target_url"], wait_until="domcontentloaded", timeout=60000)
                                await asyncio.sleep(3)
                             except: pass
                        
                        # Re-mine after rescue
                        mindmap = await analyze_page(page, page.url, self.workflow)
                        if self.is_duplicate_state(page.url, mindmap) and self.consecutive_duplicate_count >= 12:
                            print(colored(f"❌ Rescue failed: Duplicate limit reached ({self.consecutive_duplicate_count}). Breaking loop.", "red"), flush=True)
                            break
                        print(colored("🚑 Rescue successful! State changed.", "green"))
                    
                    # Check for stuck loops (circular navigation)
                    # Check for stuck loops (circular navigation)
                    if self.detect_stuck_loop():
                        print(colored("⚠️ Stuck in repetitive pattern.", "yellow"))
                        
                        # Try Self-Learning Reuse
                        current_step_meta = self._get_current_step_metadata(mindmap, page.url)
                        if current_step_meta and current_step_meta['self_learning_enabled']:
                            step_num = current_step_meta['step_num']
                            if step_num not in self.step_learnings: self.step_learnings[step_num] = []
                            
                            if len(self.step_learnings[step_num]) < 5:
                                print(colored(f"🧠 LOOP DETECTED: Triggering Self-Learning for Step {step_num}", "magenta", attrs=["bold"]))
                                
                                # Analyze failure (Loop is a failure)
                                analysis = await self._analyze_failure_with_llm(
                                    current_step_meta,
                                    self.history[-10:],
                                    mindmap,
                                    self.step_learnings[step_num]
                                )
                                
                                self.step_learnings[step_num].append({
                                    "attempt": len(self.step_learnings[step_num]) + 1,
                                    "diagnosis": "Stuck in Loop: " + analysis.get('diagnosis', 'Repetitive Actions'),
                                    "suggestion": analysis.get('suggestion'),
                                    "timestamp": time.time()
                                })
                                
                                # Enhanced Decision
                                enhanced_decision = await self._make_decision_with_learning(
                                    mindmap, page.url, current_step_meta, self.step_learnings[step_num]
                                )
                                
                                if enhanced_decision:
                                    print(colored(f"🚑 Breaking loop with enhanced decision: {enhanced_decision['action']}", "green"))
                                    # Execute immediately
                                    action_result = await self._execute_action(page, enhanced_decision, mindmap['elements'])
                                    self.history.append({
                                        "step": step,
                                        "thought": enhanced_decision['thought'] + " [Loop Break]",
                                        "action": enhanced_decision['action'],
                                        "target_text": enhanced_decision.get('target_id'),
                                        "success": action_result.get('success')
                                    })
                                    step += 1
                                    continue
                        
                        print(colored("❌ Loop break failed or limit reached. Exiting.", "red"))
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
                    
                    # POST-ACTION DOM REFRESH: If we clicked something, wait and re-mine to catch newly enabled elements
                    if action_result.get('success') and decision.get('action') == 'click':
                        print(colored("   ⏳ Post-click refresh: Checking for newly enabled elements...", "grey"))
                        await asyncio.sleep(1)  # Brief wait for any animations/state changes
                        mindmap = await analyze_page(page, page.url, self.workflow)
                        print(colored(f"   ✅ Refreshed: Now see {len(mindmap['elements'])} elements", "grey"))

                    
                    # 4. VALIDATE & LOG
                    page_title = mindmap['summary'].get('title', 'Unknown')
                    page_name = self._get_page_name(page.url, page_title)
                    
                    self.history.append({
                        "step": step,
                        "action": decision['action'],
                        "target_text": next((e['text'] for e in mindmap['elements'] if str(e['elementId']) == str(decision.get('target_id'))), ""),
                        "target_id": decision.get('target_id'),
                        "url": page.url,
                        "page_name": page_name,
                        "outcome": action_result.get('outcome'),
                        "success": action_result.get('success'),
                    })
                    
                    # Update trace for Refiner
                    if action_result.get('success') or decision['action'] in ['navigate', 'done']:
                        self.trace.append({
                            "step": step,
                            "thought": decision['thought'],
                            "action": decision['action'],
                            "page_name": page_name,
                            "locator_used": action_result.get('refined_locator') or action_result.get('locator'),
                            "value": decision.get('value'),
                            "url": page.url,
                            "screenshot": img_name,
                            "element_context":  {
                                "tag": next((e['tagName'] for e in mindmap['elements'] if str(e['elementId']) == str(decision.get('target_id'))), ""),
                                "text": next((e['text'] for e in mindmap['elements'] if str(e['elementId']) == str(decision.get('target_id'))), ""),
                                "role": next((e.get('role', '') for e in mindmap['elements'] if str(e['elementId']) == str(decision.get('target_id'))), ""),
                            }
                        })
                        self._save_trace()
                        step += 1
                    else:
                        # Determine current goal step
                        current_step_meta = self._get_current_step_metadata(mindmap, page.url)
                        
                        # Optional Step Handling
                        if current_step_meta and current_step_meta['is_optional']:
                            print(colored(f"⏭️ Optional step '{current_step_meta['description'][:40]}...' failed. Skipping.", "yellow"))
                            self.skipped_steps.append(current_step_meta['step_num'])
                            # Clear error and continue
                            self.last_error = None
                            continue
                        
                        # Self-Learning Retry
                        if current_step_meta and current_step_meta['self_learning_enabled']:
                            step_num = current_step_meta['step_num']
                            if step_num not in self.step_learnings:
                                self.step_learnings[step_num] = []
                            
                            # Trigger self-learning after 3 consecutive failures on same step
                            failures_on_step = sum(1 for h in self.history[-5:] if not h.get('success', True))
                            if failures_on_step >= 3 and len(self.step_learnings[step_num]) < 5:
                                print(colored(f"\n🧠 SELF-LEARNING ACTIVATED for step {step_num}", "magenta", attrs=["bold"]))
                                
                                # Analyze failure
                                analysis = await self._analyze_failure_with_llm(
                                    current_step_meta,
                                    self.history[-10:],
                                    mindmap,
                                    self.step_learnings[step_num]
                                )
                                
                                print(colored(f"📊 Diagnosis: {analysis.get('diagnosis', 'N/A')}", "cyan"))
                                print(colored(f"💡 Suggestion: {analysis.get('suggestion', 'N/A')}", "yellow"))
                                
                                # Store learning
                                self.step_learnings[step_num].append({
                                    "attempt": len(self.step_learnings[step_num]) + 1,
                                    "diagnosis": analysis.get('diagnosis'),
                                    "suggestion": analysis.get('suggestion'),
                                    "timestamp": time.time()
                                })
                                
                                # Make enhanced decision
                                await asyncio.sleep(2)  # Brief pause
                                mindmap = await analyze_page(page, page.url, self.workflow)
                                enhanced_decision = await self._make_decision_with_learning(
                                    mindmap,
                                    page.url,
                                    current_step_meta,
                                    self.step_learnings[step_num]
                                )
                                
                                if enhanced_decision:
                                    # Execute retry with learning
                                    retry_result = await self._execute_action(page, enhanced_decision, mindmap['elements'])
                                    if retry_result.get('success'):
                                        print(colored("✅ Self-learning retry succeeded!", "green"))
                                        # Record successful trace
                                        self.trace.append({
                                            "step": step,
                                            "thought": enhanced_decision['thought'] + " [Self-Learning Applied]",
                                            "action": enhanced_decision['action'],
                                            "page_name": page_name,
                                            "locator_used": retry_result.get('refined_locator'),
                                            "value": enhanced_decision.get('value'),
                                            "url": page.url,
                                            "screenshot": img_name,
                                            "element_context": {
                                                "tag": next((e['tagName'] for e in mindmap['elements'] if str(e['elementId']) == str(enhanced_decision.get('target_id'))), ""),
                                                "text": next((e['text'] for e in mindmap['elements'] if str(e['elementId']) == str(enhanced_decision.get('target_id'))), ""),
                                                "role": next((e.get('role', '') for e in mindmap['elements'] if str(e['elementId']) == str(enhanced_decision.get('target_id'))), ""),
                                            }
                                        })
                                        step += 1
                                        continue
                        
                        print(colored(f"⚠️ Action failed. Retrying in next step...", "yellow"))


                    # Passive Collection: Save ALL elements (always, for future RAG)
                    self._save_all_elements(page.url, step, mindmap['elements'])

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
        
        # Determine if we are in a loop to warn the Planner
        loop_warning = None
        if hasattr(self, 'consecutive_duplicate_count') and self.consecutive_duplicate_count > 1:
            loop_warning = f"⚠️ SYSTEM WARNING: You have been on this EXACT page state for {self.consecutive_duplicate_count} steps. Your previous actions are NOT changing the page. Do NOT repeat the same click. Try a different element or a different approach (e.g. scroll or wait)."

        context = {
            "goal": self.workflow,
            "page_context": mindmap['summary'],
            "elements": [{"id": e['elementId'], "text": e['text'], "tag": e['tagName'], "disabled": e.get('is_disabled', False)} for e in mindmap['elements'][:500]],
            "history": self.history[-20:], # Expanded history
            "test_data": self.test_data,
            "knowledge_bank": rag_context,
            "last_action_error": self.last_error,
            "loop_warning": loop_warning # NEW: Critical feedback to break loops
        }
        
        # If we are hitting 429s, we should explicitly try to reduce the prompt size here if needed
        # but the main fix is preventing the loop in the first place.
        
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
        
        # Enhanced: Track enabled vs disabled element counts
        enabled_count = sum(1 for e in mindmap.get('elements', []) if not e.get('is_disabled'))
        disabled_count = element_count - enabled_count
        
        # Enhanced fingerprint: URL + Enabled/Disabled counts + Title
        # This catches state changes like "search icon clicked → input becomes enabled"
        state_fingerprint = f"{page_url}:{enabled_count}:{disabled_count}:{page_title}"
        
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
        # OR if we've taken many different actions and the state hasn't changed at all (stuck)
        if state_fingerprint == self.last_state_fingerprint:
            if action_fingerprint == self.last_action_fingerprint:
                # Same action on same state - very likely stuck.
                self.consecutive_duplicate_count += 1
                return self.consecutive_duplicate_count >= 4
            
            # Different action on same state (e.g. filling next field)
            self.consecutive_duplicate_count += 1
            # Lowered threshold to trigger rescue faster (was 20)
            if self.consecutive_duplicate_count >= 8: 
                return True
            return False
        else:
            # Progress made! Reset counters.
            self.last_state_fingerprint = state_fingerprint
            self.last_action_fingerprint = action_fingerprint
            self.consecutive_duplicate_count = 0
            return False
            
        return False
    
    def detect_stuck_loop(self):
        """
        Detects if the agent is performing the exact same action sequence repeatedly.
        """
        if len(self.history) < self.loop_detection_window * 2:
            return False
            
        # Get last N actions
        recent = [f"{h['action']}:{h.get('target_text','')}[:10]" for h in self.history[-self.loop_detection_window:]]
        previous = [f"{h['action']}:{h.get('target_text','')}[:10]" for h in self.history[-self.loop_detection_window*2:-self.loop_detection_window]]
        
        # If the sequence of last N actions identifies with the previous N actions
        if recent == previous:
            # Allow some repetition if we are in a self-learning loop (check if diagnosisfound)
            if any("Self-Learning" in str(h.get('thought', '')) for h in self.history[-self.loop_detection_window:]):
                return False
            return True
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
            
        # Smart Guard: Provide helpful feedback for disabled elements
        if target_el and target_el.get('is_disabled'):
            # Look for nearby elements that might enable this one
            target_text = target_el.get('text', '')[:50]
            
            # Check if there's a button with similar text that might open/enable this field
            potential_enablers = [
                e for e in elements 
                if not e.get('is_disabled') 
                and e.get('tagName') == 'button'
                and any(keyword in e.get('text', '').lower() for keyword in ['search', 'open', 'show', 'expand'])
            ]
            
            if potential_enablers:
                enabler = potential_enablers[0]
                hint = f"Element {target_id} ('{target_text}') is disabled. Try clicking element {enabler['elementId']} ('{enabler['text'][:30]}') first to enable it."
                print(colored(f"💡 Smart Guard: {hint}", "yellow"))
                return {"success": False, "outcome": hint}
            else:
                print(colored(f"🛡️ Guard: Element {target_id} is disabled and no enabler found.", "red"))
                return {"success": False, "outcome": f"Element {target_id} is disabled. Look for a button or icon that might enable it (e.g., 'Search', 'Edit', 'Open')."}

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
                    # 🎯 Show visual cursor before clicking (headed mode only)
                    if self.headed and target_el.get('center'):
                        cx, cy = target_el['center'].get('x'), target_el['center'].get('y')
                        if cx and cy:
                            try:
                                await page.evaluate(f"window.showAgentCursor && window.showAgentCursor({cx}, {cy}, 'click')")
                                await asyncio.sleep(0.3)  # Brief pause to see cursor
                            except: pass
                    
                    await page.locator(locator_str).click(timeout=15000)
                    
                    # 🔍 SEARCH ICON HANDLER: Wait for popover to open, let Planner fill naturally
                    target_text_lower = target_el.get('text', '').lower()
                    if 'search' in target_text_lower and ('product' in target_text_lower or 'part' in target_text_lower):
                        print(colored("   🔍 Search icon clicked. Waiting for search popover...", "cyan"))
                        await asyncio.sleep(2)  # Wait for search panel to open
                        # Let the Planner handle filling the input in the next step
                    
                    # Add wait for potential modal triggers
                    elif "cart" in target_text_lower or "add" in target_text_lower:
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
        
        # Record action for sequence learning
        self.robust_handler.record_action(
            action=action,
            target_id=str(target_id),
            target_text=target_el.get('text', '')[:50] if target_el else '',
            success=result.get("success", False)
        )
            
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
            # If the path is already relative to the root (starts with 'projects/'), use it directly
            if path_from_config.startswith("projects/") or path_from_config.startswith("projects\\"):
                trace_path = path_from_config
            else:
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
        
        # Save successful action sequence for future replay
        if len(self.trace) > 0:
            # Create flow name from workflow
            flow_name = self.workflow[:50].replace(" ", "_").replace(":", "").lower()
            self.robust_handler.save_successful_flow(flow_name)

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
        # Use the same output directory as other artifacts
        file_path = os.path.join(self.output_dir, "discovered_elements.json")
        
        data = {}
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                try: data = json.load(f)
                except: data = {}
        
        key = f"{url}::step_{step}"
        data[key] = elements
        
        # ROTATION LOGIC
        if len(data) > 50:
             sorted_keys = sorted(data.keys())[-50:] 
             data = {k: data[k] for k in sorted_keys}

        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        print(colored(f"💾 Passive Collection: {len(elements)} elements saved to {file_path}", "blue"))
    
    def _parse_goal_with_metadata(self, goal_text):
        """Parse goal string and extract metadata for each step."""
        import re
        
        steps = []
        # Split by numbered steps: "1.", "2.", etc.
        step_pattern = r'(\d+)\.\s*([^0-9]+?)(?=\d+\.|$)'
        matches = re.findall(step_pattern, goal_text, re.DOTALL)
        
        for step_num, step_text in matches:
            step_text = step_text.strip()
            # Extract annotations
            is_optional = bool(re.search(r'\[optional\s*step\]', step_text, re.IGNORECASE))
            self_learning = bool(re.search(r'\[keep\s+trying|self[\s-]?learning\]', step_text, re.IGNORECASE))
            
            # Clean text (remove annotations)
            clean_text = re.sub(r'\[optional.*?\]|\[keep.*?\]|\[self.*?\]', '', step_text, flags=re.IGNORECASE).strip()
            # Remove trailing periods/colons
            clean_text = re.sub(r'[.,:]+$', '', clean_text).strip()
            
            steps.append({
                "step_num": int(step_num),
                "description": clean_text,
                "is_optional": is_optional,
                "self_learning_enabled": self_learning
            })
        
        return steps if steps else [{"step_num": 1, "description": goal_text, "is_optional": False, "self_learning_enabled": False}]
    
    def _get_current_step_metadata(self, mindmap, url):
        """Determine which goal step we're currently working on."""
        # Match keywords from step descriptions to recent actions
        for step_meta in self.parsed_goal:
            if step_meta['step_num'] in self.skipped_steps:
                continue  # Skip already completed steps
            
            step_keywords = [w.lower() for w in step_meta['description'].split() if len(w) > 3]
            recent_actions = ' '.join([h.get('target_text', '') for h in self.history[-5:]]).lower()
            page_content = mindmap['summary'].get('title', '').lower()
            
            # If recent actions or page content match this step's keywords
            if any(keyword in recent_actions or keyword in page_content for keyword in step_keywords[:3]):
                return step_meta
        
        # Default: Return first incomplete step
        for step_meta in self.parsed_goal:
            if step_meta['step_num'] not in self.skipped_steps:
                return step_meta
        
        return self.parsed_goal[0] if self.parsed_goal else None
    
    async def _analyze_failure_with_llm(self, step_metadata, recent_history, mindmap, past_learnings):
        """Use LLM to analyze why the step failed."""
        analysis_prompt = f"""You are a Test Automation Failure Analyst. Analyze why this step failed.

**GOAL STEP**: {step_metadata['description']}

**RECENT ACTIONS** (last 10):
{json.dumps(recent_history, indent=2)}

**CURRENT PAGE**:
- URL: {mindmap.get('url', 'N/A')}
- Title: {mindmap['summary'].get('title', 'N/A')}
- Elements: {len(mindmap['elements'])}

**PAST LEARNINGS**:
{json.dumps(past_learnings, indent=2) if past_learnings else "None (first attempt)"}

Diagnose WHY it failed and suggest a fix. Don't repeat failed strategies.

OUTPUT JSON:
{{
  "diagnosis": "Root cause",
  "suggestion": "Specific fix to try",
  "confidence": "high|medium|low"
}}
"""
        
        try:
            resp = await llm.ainvoke([("system", "You are a test automation expert."), ("human", analysis_prompt)])
            return try_parse_json(resp.content) or {"diagnosis": "Unknown", "suggestion": "Try alternative approach", "confidence": "low"}
        except Exception as e:
            print(f"LLM analysis error: {e}")
            return {"diagnosis": "LLM error", "suggestion": "Retry", "confidence": "low"}
    
    async def _make_decision_with_learning(self, mindmap, page_url, step_metadata, learnings):
        """Enhanced decision making with accumulated learnings."""
        learning_summary = "\n".join([
            f"Attempt {l['attempt']}: {l['diagnosis']} → Try: {l['suggestion']}"
            for l in learnings
        ])
        
        enhanced_context = {
            "goal": step_metadata['description'],
            "page_context": mindmap['summary'],
            "elements": [{"id": e['elementId'], "text": e['text'], "tag": e['tagName'], "disabled": e.get('is_disabled', False)} for e in mindmap['elements'][:500]],
            "history": self.history[-20:],
            "test_data": self.test_data,
            "knowledge_bank": self.kb.get_rag_context(page_url, self.workflow),
            "self_learning_insights": learning_summary,
            "last_action_error": self.last_error
        }
        
        enhanced_prompt = SYSTEM_PROMPT_PLANNER + f"""

**🧠 SELF-LEARNING MODE ACTIVE**:
Previous attempts on this step:
{learning_summary}

You MUST try a DIFFERENT approach than what failed before.
"""
        
        prompt = f"Context:\n{json.dumps(enhanced_context, indent=2)}"
        
        try:
            resp = await llm.ainvoke([("system", enhanced_prompt), ("human", prompt)])
            return try_parse_json(resp.content)
        except Exception as e:
            print(f"Enhanced decision error: {e}")
            return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python explorer.py <config_path> [--headed]")
        sys.exit(1)
    
    config_path = sys.argv[1]
    headed = "--headed" in sys.argv
    agent = ExplorerAgent(config_path, headed=headed)
    asyncio.run(agent.run())
