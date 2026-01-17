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
from core.lib.visual_verifier import VisualVerifier
from core.lib.tool_executor import ToolExecutor
from core.lib.visual_locator import VisualLocator
from core.lib.visual_watcher import VisualWatcher
from core.lib.vision_interactor import VisionInteractor
import cv2
import numpy as np

load_dotenv()

# Initialize 2026-ready LLM
# Initialize 2026-ready LLM
llm = SafeLLM(
    model="gemini-2.0-flash",
    temperature=0.0,
    model_kwargs={"response_mime_type": "application/json"}
)

SYSTEM_PROMPT_PLANNER = """
You are a Senior Automation Strategist working with a Tool Registry system.
Your goal is to complete the user's workflow by deciding the next best TOOL to use.

**AVAILABLE TOOLS (World-Class, High-Resilience):**
1. **perform_search**: Search for a query.
   - Args: {"query": "text to search"}
   - *Strategy*: High-level abstraction. Use this first for any search task.
   
2. **smart_click**: Click an element with multi-stage fallback.
   - Args: {"element_id": int (MANDATORY), "text": "optional", "selector": "optional"}
   - *Strategic Note*: High reliability. It uses the `element_id` to retrieve vision coordinates (x,y) if Playwright fails. ALWAYS include the `element_id` from the list.
   
3. **smart_fill**: Fill an input field with verification.
   - Args: {"element_id": int (MANDATORY), "value": "text", "placeholder": "optional"}
   - *Strategic Note*: Tries Native Type -> Force Fill -> JS Value Injection. ALWAYS include `element_id`.
   
4. **navigate_to**: Direct URL navigation.
5. **verify_text**: Check if text is present on the page (Validation).
   - Args: {"text": "exact text to look for"}
   - *Strategy*: Use this for "Verify X appears" or "Confirm X is in cart" steps. NOT for searching.

6. **get_css_hierarchy**: Generate a robust, unique CSS selector.
   - Args: {"text": "visible text of element"}
   - *Strategy*: **PRIORITY TOOL**. Use this BEFORE clicking to get a guaranteed unique selector, especially for products or lists.

**THINKING PROCESS (WORLD CLASS):**
1. **Selector First**: Can I get a unique selector for my target? Use `get_css_hierarchy`.
2. **Action-Result Cycle**: I just used tool X. Did the page change? If NO, why?
3. **Vision-First Trust**: If you see an element in the list, use its `id`.
4. **State Awareness**: If the goal says "Enter credentials" and the modal is open, focus on those inputs.
4. **Crisis Recovery**: If trapped in a loop, propose a DIFFERENT target or a DIFFERENT tool. Don't be afraid to click neighboring elements to trigger UI updates.

**INPUTS:**
1. `goal`: The user's workflow goal.
2. `page_context`: A summary of the current page.
3. `elements`: A list of interactive elements found.
4. `history`: Past tool executions and their outcomes.
5. `test_data`: Available credentials or input data.
6. `knowledge_bank`: Strategic insights from previous runs.

**THINKING PROCESS:**
1. Observe: What page am I on?
2. **ERROR CHECK**: If `last_tool_error` exists, learn from it and try a different approach.
3. History Check: What tools have I ALREADY executed? Don't repeat unless stuck.
4. **KNOWLEDGE CHECK**: If `knowledge_bank` has proven strategies, follow them.
5. Validate: Did my LAST tool call work? (Check if elements changed or new content appeared)
6. Multi-Goal Check: Does the goal have multiple phases? Track which are complete.
7. **Login Check**: If login page appears and NO credentials in `test_data` or `goal`, skip login.
8. Select: Which TOOL and ARGUMENTS achieve the next unfulfilled part of the goal?

**CRITICAL RULES:**
- **Tool Selection**: Choose the right tool for the task (search vs click vs fill)
- **Argument Quality**: Provide exact, specific arguments (e.g., text="Submit" not text="button")
- **Sequential Progress**: Complete Phase 1 before Phase 2
- **Error Recovery**: If a tool fails, try a different approach (different text, selector strategy)

**OUTPUT SCHEMA (JSON only)**:
{
  "thought": "Explicitly state which Phase/Step you are currently on and why this tool is the correct choice",
  "tool": "perform_search | smart_click | smart_fill | navigate_to | verify_text | get_css_hierarchy",
  "arguments": {
    // Tool-specific arguments (see AVAILABLE TOOLS above)
  },
  "expected_outcome": "Description of expected UI change (e.g., 'Search results page loads')",
  "completed_step": 1,  // The number of the PHASE you just finished
  "is_goal_achieved": false
}

**EXAMPLES:**

// Search scenario
{
  "thought": "Phase 2 requires searching for 'AAPL'. I will use perform_search which auto-handles the search submission.",
  "tool": "perform_search",
  "arguments": {"query": "AAPL"},
  "expected_outcome": "Search results page appears with Apple Inc. information",
  "completed_step": 2,
  "is_goal_achieved": false
}

// Click scenario  
{
  "thought": "I need to click the 'News' link to proceed to Phase 1b.",
  "tool": "smart_click",
  "arguments": {"text": "News"},
  "expected_outcome": "News section loads",
  "completed_step": 1,
  "is_goal_achieved": false
}

**GOAL COMPLETION**:
Set `is_goal_achieved: true` ONLY when EVERY phase is complete and you see confirmation (success message, target page loaded, etc.).
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
        self.total_cost = {"input": 0, "output": 0}
        self.output_dir = os.path.join(os.path.dirname(config_path), "outputs")
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.history = []
        self.vision_first_mode = os.environ.get("VISION_FIRST", "false").lower() == "true"
        self.visual_watcher = None
        self.vision_interactor = None
        
        # Initialize Vision components if mode enabled
        if self.vision_first_mode:
            print(colored("👁️ Vision-First mode enabled (with OCR support)", "cyan", attrs=["bold"]))
            self.visual_watcher = VisualWatcher(None) # Page set during execute
            self.vision_interactor = VisionInteractor(None)
        self.visited_states = set()
        self.loop_detection_window = 5
        self.scrolled_urls = set()
        self.snapshot_dir = self.output_dir
        self.last_error = None
        
        # Initialize Robust Action Handler
        self.robust_handler = get_robust_handler()
        self.robust_handler.set_domain(self.config.get("target_url", ""))
        self.robust_handler.reset()  # Fresh start for this session
        
        # Initialize Tool Executor
        self.tool_executor = ToolExecutor()
        print(colored("🔧 Tool Executor initialized", "cyan"))
        
        # Goal Parsing
        self.parsed_goal = self._parse_goal_with_metadata(self.workflow)
        self.completed_goal_steps = []
        self.skipped_goal_steps = []
        self.step_learnings = {}
        
        print(colored(f"📋 Parsed {len(self.parsed_goal)} goal steps", "cyan"))
        for step in self.parsed_goal:
            print(colored(f"  Step {step['step_num']}: {step['description'][:60]}", "grey"))

    async def wait_for_page_stability(self, page, timeout=5000, interval=500):
        """World-Class Stability Check: Waits until the DOM stops changing."""
        try:
            print(colored(f"⏳ Waiting for page stability...", "grey"))
            last_count = -1
            start_time = time.time()
            while time.time() - start_time < timeout / 1000:
                current_count = await page.evaluate("document.querySelectorAll('*').length")
                if current_count == last_count:
                    await asyncio.sleep(0.3)
                    return True
                last_count = current_count
                await asyncio.sleep(interval / 1000)
        except: pass
        return False

    def _get_page_name(self, url, title):
        """Determines a valid class name for the current page."""
        from urllib.parse import urlparse
        path = urlparse(url).path.strip('/')
        if not path or path == 'index.php': return "HomePage"
        if 'login' in path: return "LoginPage"
        if 'product' in path: return "ProductsPage"
        if 'cart' in path: return "CartPage"
        if title:
            clean_title = re.sub(r'[^a-zA-Z0-9]', ' ', title).title().replace(' ', '')
            if clean_title: return f"{clean_title}Page"
        return "GenericPage"

        
    async def run(self):
        print(colored(f"Explorer: Starting Strategy 2026. Goal: {self.workflow}", "blue", attrs=["bold"]))
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=not self.headed,
                    channel="chrome", 
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
                    ignore_https_errors=False,
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
                
                # Override navigator properties to hide automation (Super-Stealth Mode)
                await context.add_init_script("""
                    // Hide WebDriver
                    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                    
                    // Add realistic plugins
                    Object.defineProperty(navigator, 'plugins', {get: () => [
                        {name: 'Chrome PDF Viewer', filename: 'internal-pdf-viewer', description: 'Portable Document Format'},
                        {name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer', description: 'Portable Document Format'},
                        {name: 'Native Client', filename: 'internal-nacl-plugin', description: ''}
                    ]});
                    
                    // Add realistic languages and platform
                    Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                    Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});
                    
                    // Hardware signals
                    Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});
                    Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});
                    
                    // WebGL Spoofing (often used for fingerprinting)
                    const getParameter = WebGLRenderingContext.prototype.getParameter;
                    WebGLRenderingContext.prototype.getParameter = function(parameter) {
                        if (parameter === 37445) return 'Intel Open Source Technology Center';
                        if (parameter === 37446) return 'Mesa DRI Intel(R) HD Graphics 520 (Skylake GT2)';
                        return getParameter(parameter);
                    };

                    window.chrome = {runtime: {}, loadTimes: () => ({}), csi: () => ({}), app: {}};
                    
                    // Fake Battery API
                    if (navigator.getBattery) {
                        const originalGetBattery = navigator.getBattery;
                        navigator.getBattery = () => Promise.resolve({
                            charging: true,
                            chargingTime: 0,
                            dischargingTime: Infinity,
                            level: 1,
                            onchargingchange: null,
                            onchargingtimechange: null,
                            ondischargingtimechange: null,
                            onlevelchange: null
                        });
                    }
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
                    # Random human-like delay before first navigation
                    delay = 1.0 + (float(int(hashlib.md5(self.config['target_url'].encode()).hexdigest(), 16)) % 2000) / 1000
                    print(colored(f"⏳ Humanizing: Waiting {delay:.1f}s before navigation...", "grey"))
                    await asyncio.sleep(delay)

                    print(colored(f"🌐 Initial Navigation: {self.config['target_url']}", "cyan"))
                    response = await page.goto(self.config["target_url"], wait_until="domcontentloaded", timeout=90000)


                    
                    # --- HUMAN SIGNALS ---
                    # Akamai often unblocks after mouse move/scroll
                    print(colored("🖱️ Sending human signals (Mouse move + Scroll)...", "grey"))
                    await page.mouse.move(100, 100)
                    await asyncio.sleep(0.5)
                    await page.mouse.move(400, 300)
                    await page.mouse.wheel(0, 300) # Scroll down
                    await asyncio.sleep(0.8)
                    await page.mouse.wheel(0, -300) # Scroll back up
                    
                    # Check if blocked (status code or skeleton)
                    if response and response.status >= 400:
                         print(colored(f"⚠️ Page blocked (Status {response.status}). Retrying with fresh context...", "yellow"))
                         await asyncio.sleep(5)
                         await page.goto(self.config["target_url"], wait_until="networkidle", timeout=60000)

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
                trace_file = os.path.join(self.output_dir, 'trace.json')
                if os.path.exists(trace_file):
                    try:
                        print(colored("\n⚡ FAST LANE ACTIVATED: Replaying saved workflow!", "green", attrs=["bold"]))
                        print(colored(f"📋 Loading trace from: {trace_file}", "cyan"))
                        
                        with open(trace_file, 'r', encoding='utf-8') as f:
                            saved_trace = json.load(f)
                        
                        workflow_steps = saved_trace.get('trace', [])
                        print(colored(f"🎯 Found {len(workflow_steps)} steps to replay", "cyan"))
                        
                        # Initialize ToolExecutor with trace path for self-healing
                        self.tool_executor = ToolExecutor(trace_path=trace_file)
                        
                        # Execute workflow with multi-locator fallback
                        success_count = 0
                        for idx, step_data in enumerate(workflow_steps, 1):
                            print(colored(f"\n--- Step {idx}/{len(workflow_steps)} ---", "blue"))
                            
                            # Get current page screenshot for visual matching
                            try:
                                screenshot_path = os.path.join(self.output_dir, f'replay_step_{idx}.png')
                                await page.screenshot(path=screenshot_path)
                            except:
                                screenshot_path = None
                            
                            # Execute with multi-locator fallback
                            result = await self.tool_executor.execute_with_fallback(
                                page, 
                                step_data,
                                screenshot_path
                            )
                            
                            if result.get('status') == 'success':
                                success_count += 1
                                if result.get('fallback_used'):
                                    print(colored(f"  🔄 Used fallback locator (self-healed)", "cyan"))
                            else:
                                print(colored(f"  ❌ Step {idx} failed: {result.get('error')}", "red"))
                                print(colored(f"\\n⚠️ Fast Lane failed at step {idx}, falling back to exploration...", "yellow"))
                                break
                        
                        if success_count == len(workflow_steps):
                            print(colored(f"\\n✅ Fast Lane replay of {success_count} steps finished.", "green", attrs=["bold"]))
                            # Pick up from where we left off to ensure goal is reached
                            step = success_count
                        else:
                            print(colored(f"\\n⚠️ Fast Lane partial completion ({success_count}/{len(workflow_steps)})", "yellow"))
                            step = success_count
                    
                    except Exception as e:
                        print(colored(f"⚠️ Fast Lane error: {e}", "yellow"))
                        print(colored("🔄 Falling back to normal exploration...", "yellow"))
                        # Continue to slow lane below
                else:
                    print(colored("\n🐢 SLOW LANE: No saved workflow found - exploring from scratch...", "cyan"))
                
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
                    
                    prio_keywords = ['search', 'product', 'category', 'collection', 'find', 'vacuum', 'hair', 'shop', 'store']
                    if page.url not in self.scrolled_urls and any(k in page.url.lower() for k in prio_keywords):
                        print(colored("📜 Triggering one-time infinite scroll for new relevant page...", "cyan"))
                        await self.handle_infinite_scroll(page, max_scrolls=3)
                        self.scrolled_urls.add(page.url)

                    # Initialize mindmap for this step
                    mindmap = None

                    # --- TURBO: Stability & State-Aware Caching ---
                    await self.wait_for_page_stability(page)
                    current_dom_hash = await self.get_dom_hash(page)
                    state_key = f"{page.url}:{current_dom_hash}"
                    
                    # Force mining if the last action was a 'fill' (to see suggestions)
                    force_mining = self.history and self.history[-1]['action'] == 'fill'
                    
                    # --- VISION-FIRST: Instant Fallback for Modals ---
                    if self.vision_first_mode and self.visual_watcher:
                        # Update VisualWatcher with the current page
                        self.visual_watcher.page = page
                        if await self.visual_watcher.wait_for_visual_stability(timeout_ms=5000):
                            if self.visual_watcher.is_overlay_present():
                                print(colored("🚀 [Instant Vision Fallback] Modal detected - providing skeletal mindmap for Vision assistance", "green", attrs=["bold"]))
                                goal_lower = self.workflow.get('goal', '').lower()
                                skeletal_elements = []
                                if 'login' in goal_lower:
                                    skeletal_elements = [
                                        {"elementId": 9991, "text": "Username", "type": "input", "hint": "Visible via OCR"},
                                        {"elementId": 9992, "text": "Password", "type": "input", "hint": "Visible via OCR"},
                                        {"elementId": 9993, "text": "Log in", "type": "button", "hint": "Visible via OCR"}
                                    ]
                                elif 'signup' in goal_lower or 'sign up' in goal_lower:
                                    skeletal_elements = [
                                        {"elementId": 9991, "text": "Username", "type": "input", "hint": "Visible via OCR"},
                                        {"elementId": 9992, "text": "Password", "type": "input", "hint": "Visible via OCR"},
                                        {"elementId": 9993, "text": "Sign up", "type": "button", "hint": "Visible via OCR"}
                                    ]
                                elif 'order' in goal_lower or 'purchase' in goal_lower:
                                    # Support for Place Order modal
                                    skeletal_elements = [
                                        {"elementId": 9991, "text": "Name", "type": "input", "hint": "Visible via OCR"},
                                        {"elementId": 9992, "text": "Credit card", "type": "input", "hint": "Visible via OCR"},
                                        {"elementId": 9993, "text": "Purchase", "type": "button", "hint": "Visible via OCR"}
                                    ]
                                mindmap = {
                                    "summary": {"title": await page.title(), "mission_status": "Vision-assisted modal detected", "state": "action_required"},
                                    "elements": skeletal_elements,
                                    "blocking_elements": [{"type": "overlay", "reason": "Modal backdrop blocking DOM mining"}]
                                }
                                self.last_mindmap = mindmap
                                self.last_state_key = state_key # Use the same state key
                    
                    if not mindmap:
                        if not force_mining and hasattr(self, 'last_state_key') and self.last_state_key == state_key:
                            print(colored(f"⚡ Turbo Mode: State unchanged. Skipping mining (Reusing cache)...", "green", attrs=["bold"]))
                            mindmap = self.last_mindmap
                        else:
                            # 1. ANALYZE (Miner) with Timeout Protection
                            try:
                                mindmap = await asyncio.wait_for(
                                    analyze_page(page, page.url, self.workflow),
                                    timeout=120
                                )
                            except asyncio.TimeoutError:
                                print(colored("⚠️ Vision analysis timed out. Falling back to simple extraction.", "yellow"))
                                mindmap = {
                                    "summary": {"title": await page.title(), "mission_status": "Vision timed out.", "state": "error"},
                                    "elements": [],
                                    "blocking_elements": []
                                }
                            
                            # PROACTIVE BLOCKER HANDLING: If Miner detects a modal, dismiss it immediately
                            if mindmap and (mindmap.get('summary', {}).get('state') == 'blocked_by_modal' or mindmap.get('blocking_elements')):
                                print(colored("🚨 Proactive Blocker Detected! Triggering dismissal shield...", "magenta", attrs=["bold"]))
                                await self._dismiss_overlays(page)
                                await asyncio.sleep(1)
                                # Re-mine after dismissal
                                mindmap = await analyze_page(page, page.url, self.workflow)
                            
                            self.last_state_key = state_key
                            self.last_mindmap = mindmap
                    # ----------------------------------
                    
                    # Save screenshot for trace
                    page_title = mindmap['summary'].get('title')
                    if not page_title or page_title == "Unknown":
                        page_title = await page.title() or "Unknown"
                    
                    page_name = self._get_page_name(page.url, page_title)
                    img_name = f"step_{step:02d}_{page_name}.png"
                    img_path = os.path.join(self.snapshot_dir, img_name)
                    
                    # Capture screenshot with error handling for connection issues
                    try:
                        await page.screenshot(path=img_path)
                    except Exception as screenshot_error:
                        print(colored(f"⚠️ Screenshot failed: {screenshot_error}", "yellow"))
                        # Create a placeholder to avoid breaking trace
                        img_name = f"step_{step:02d}_error.png"
                    
                    print(colored(f"📍 PAGE: {page_title}", "white", attrs=["bold"]), flush=True)
                    print(colored(f"🔍 URL: {page.url}", "grey"), flush=True)
                    
                    # Check for duplicate states (infinite loop prevention)
                    is_dup_state = await self.is_duplicate_state(page.url, mindmap, page=page)
                    
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
                                 action_result = await self._execute_tool_intent(page, enhanced_decision, mindmap['elements'])
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
                        if await self.is_duplicate_state(page.url, mindmap, page=page) and self.consecutive_duplicate_count >= 12:
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
                                    action_result = await self._execute_tool_intent(page, enhanced_decision, mindmap['elements'])
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

                    # --- GOAL COMPLETION CHECK (Pre-Action 'done' only) ---
                    if decision.get('action') == 'done' or decision.get('is_goal_achieved'):
                        # Log final state before exiting
                        # AUTO-COMPLETE: If we are done, mark all remaining steps as passed
                        for gs in self.parsed_goal:
                            if gs['step_num'] not in self.completed_goal_steps:
                                self.completed_goal_steps.append(gs['step_num'])
                                print(colored(f"✅ STEP {gs['step_num']} PASSED!", "green", attrs=["bold"]))

                        self.trace.append({
                            "step": step,
                            "thought": thought or 'Goal already achieved.',
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
                    
                    # 📸 PRE-ACTION CAPTURE (For Visual Verification)
                    try:
                        pre_action_screenshot = await page.screenshot(type="jpeg", quality=50)
                    except:
                        pre_action_screenshot = None

                    action_result = await self._execute_tool_intent(page, decision, mindmap['elements'])
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
                        
                        # 📸 VISUAL VERIFICATION (Local Diff)
                        visual_diff = {"score": 0, "changed": False}
                        if pre_action_screenshot:
                            try:
                                post_action_screenshot = await page.screenshot(type="jpeg", quality=50)
                                visual_diff = VisualVerifier.get_visual_diff(pre_action_screenshot, post_action_screenshot)
                                
                                if visual_diff['changed']:
                                    print(colored(f"   👀 VISUAL CONFIRMATION: UI Changed by {visual_diff['score']}%", "green"))
                                else:
                                    print(colored(f"   ⚠️ VISUAL WARNING: No significant visual change detected ({visual_diff['score']}%)", "yellow"))
                            except Exception as e:
                                print(colored(f"   ⚠️ Visual verify failed: {e}", "yellow"))

                        mindmap = await analyze_page(page, page.url, self.workflow)
                        # Inject visual feedback into mindmap for next turn
                        mindmap['last_visual_diff'] = visual_diff
                        
                        print(colored(f"   ✅ Refreshed: Now see {len(mindmap['elements'])} elements", "grey"))

                    
                    # 4. VALIDATE & LOG
                    page_title = mindmap['summary'].get('title', 'Unknown')
                    page_name = self._get_page_name(page.url, page_title)
                    
                    self.history.append({
                        "step": step,
                        "action": decision.get('tool') or decision.get('action', 'unknown'),
                        "target_text": next((e['text'] for e in mindmap['elements'] if str(e['elementId']) == str(decision.get('target_id'))), ""),
                        "target_id": decision.get('target_id'),
                        "url": page.url,
                        "page_name": page_name,
                        "outcome": action_result.get('outcome'),
                        "success": action_result.get('success'),
                    })
                    action_key = decision.get('tool') or decision.get('action', '')
                    if action_result.get('success') or action_key in ['navigate', 'navigate_to', 'done']:
                        # Build multi-locator array
                        locators_array = self._build_locators_array(
                            decision, 
                            action_result, 
                            mindmap['elements'], 
                            step,
                            page,
                            current_screenshot_path=img_path
                        )
                        
                        self.trace.append({
                            "step": step,
                            "thought": decision['thought'],
                            "action": decision.get('tool') or decision.get('action', 'unknown'),
                            "page_name": page_name,
                            "locators": locators_array,  # NEW: Multi-locator array
                            # Keep old fields for backward compatibility
                            "locator_used": action_result.get('refined_locator') or action_result.get('locator') or decision.get('arguments', {}).get('selector') or decision.get('arguments', {}).get('text'),
                            "value": decision.get('value') or decision.get('arguments', {}).get('value') or decision.get('arguments', {}).get('query'),
                            "url": page.url,
                            "screenshot": img_name,
                            "element_context":  {
                                "tag": next((e['tagName'] for e in mindmap['elements'] if str(e['elementId']) == str(decision.get('target_id'))), ""),
                                "text": next((e['text'] for e in mindmap['elements'] if str(e['elementId']) == str(decision.get('target_id'))), ""),
                                "role": next((e.get('role', '') for e in mindmap['elements'] if str(e['elementId']) == str(decision.get('target_id'))), ""),
                            }
                        })
                        self._save_trace()
                        
                        # NEW: Check if this action completed the goal
                        if decision.get('completed_step'):
                            step_num = int(decision.get('completed_step'))
                            if step_num not in self.completed_goal_steps:
                                self.completed_goal_steps.append(step_num)
                                print(colored(f"✅ STEP {step_num} PASSED!", "green", attrs=["bold"]))

                        if decision.get('is_goal_achieved'):
                             print(colored("🎯 MISSION ACCOMPLISHED: Final action executed. Goal Achieved!", "green", attrs=["bold"]), flush=True)
                             break
                             
                        step += 1
                    else:
                        # Determine current goal step
                        current_step_meta = self._get_current_step_metadata(mindmap, page.url)
                        
                        # Optional Step Handling
                        if current_step_meta and current_step_meta['is_optional']:
                            print(colored(f"⏭️ Optional step '{current_step_meta['description'][:40]}...' failed. Skipping.", "yellow"))
                            self.skipped_goal_steps.append(current_step_meta['step_num'])
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
                                    retry_result = await self._execute_tool_intent(page, enhanced_decision, mindmap['elements'])
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
        self.last_rag_context = rag_context
        
        # Determine if we are in a loop to warn the Planner
        loop_warning = None
        if hasattr(self, 'consecutive_duplicate_count') and self.consecutive_duplicate_count > 1:
            loop_warning = f"⚠️ CRITICAL LOOP WARNING: You have been on this EXACT page state for {self.consecutive_duplicate_count} steps. Your last action '{self.history[-1]['action']}' on target '{self.history[-1].get('target_text')}' CHANGED NOTHING. Do NOT repeat this. Try a different element, scroll, or assume the goal might be partially blocked. If you just clicked a search icon and the input is still 'disabled', try clicking it again OR look for a hidden input that might have appeared."

        # TOKEN OPTIMIZATION: Truncate element text and filter out junk
        formatted_elements = []
        for e in mindmap['elements'][:300]: # Reduced from 500
            text = (e.get('text') or '').strip()
            if len(text) > 60: # Reduced from 100
                text = text[:57] + "..."
            
            # Skip elements that are purely decorative or empty unless they are inputs/buttons/links
            if not text and e['tagName'] not in ['button', 'input', 'select', 'a', 'area', 'textarea']:
                continue
                
            formatted_elements.append({
                "id": e['elementId'],
                "text": text,
                "tag": e['tagName'],
                "type": e.get('type', ''),
                "placeholder": e.get('attributes', {}).get('placeholder', ''),
                "name": e.get('attributes', {}).get('name', ''),
                "role": e.get('role', ''),
                "disabled": e.get('is_disabled', False)
            })

        # Truncate RAG context if it's too large
        str_rag = str(rag_context)
        if len(str_rag) > 5000:
            rag_context = str_rag[:5000] + "... [TRUNCATED]"

        # GOAL PROGRESS TRACKING
        goal_status = []
        current_step_id = None
        for step in self.parsed_goal:
            status = "⏳ PENDING"
            if step['step_num'] in self.completed_goal_steps:
                status = "✅ PASSED"
            elif step['step_num'] in self.skipped_goal_steps:
                status = "⏭️ SKIPPED"
            elif current_step_id is None:
                status = "🏃 IN PROGRESS"
                current_step_id = step['step_num']
            goal_status.append(f"Step {step['step_num']}: {step['description']} [{status}]")

        # COGNITIVE UNSTUCK MECHANISM
        # Detect potentially stuck state based on history
        failed_attempts = [h for h in self.history[-5:] if not h.get('success', True)]
        last_3_actions = [h['action'] for h in self.history[-3:]]
        
        # Condition 1: Repeated Failures (3+ failures in last 5 steps)
        if len(failed_attempts) >= 3:
            loop_warning = f"⚠️ COGNITIVE STOP: You have failed {len(failed_attempts)} times recently. STOP. Do NOT retry the same action. Look for a different way. Is there a popup? Is the element disabled? Try 'perform_search' instead of clicking. Try scrolling."
            
        # Condition 2: Action Loop (Last 3 actions are identical)
        elif len(last_3_actions) == 3 and len(set(last_3_actions)) == 1:
            loop_warning = f"⚠️ COGNITIVE STOP: You are looping on action '{last_3_actions[0]}'. STOP. You already tried this 3 times. It is NOT working. Propose a DIFFERENT tool or a DIFFERENT target."
            
        # Condition 3: Existing State Loop (Duplicate state count)
        elif hasattr(self, 'consecutive_duplicate_count') and self.consecutive_duplicate_count > 1:
            loop_warning = f"⚠️ CRITICAL LOOP WARNING: You have been on this EXACT page state for {self.consecutive_duplicate_count} steps. Your last action '{self.history[-1]['action']}' on target '{self.history[-1].get('target_text')}' CHANGED NOTHING. Do NOT repeat this. Try a different element, scroll, or assume the goal might be partially blocked. If you just clicked a search icon and the input is still 'disabled', try clicking it again OR look for a hidden input that might have appeared."
            
        # Condition 4: Stuck on same Goal Step for too long
        # (This logic requires tracking step start times/counts, skipping for now to keep it simple)

        context = {
            "goal": self.workflow,
            "goal_progress": goal_status, 
            "current_step": current_step_id,
            "page_context": mindmap['summary'],
            "elements": formatted_elements,
            "history": self.history[-10:], 
            "test_data": self.test_data,
            "knowledge_bank": rag_context,
            "last_action_error": self.last_error,
            "loop_warning": loop_warning 
        }
        
        
        prompt = f"Current Mindmap Context:\n{json.dumps(context, indent=2)}"
        
        if loop_warning:
            print(colored(f"\n🧠 COGNITIVE UNSTUCK TRIGGERED: {loop_warning}\n", "magenta", attrs=['bold']))
            prompt = f"!!! CRISIS MODE - READ THIS FIRST !!!\n{loop_warning}\n\n" + prompt
        
        try:
            resp = await llm.ainvoke([("system", SYSTEM_PROMPT_PLANNER), ("human", prompt)])
            return try_parse_json(resp.content)
        except Exception as e:
            print(f"Error in decision: {e}")
            return None
    
    async def get_dom_hash(self, page):
        """
        Hash the *semantic* content, including Shadow DOM and input values.
        This provides a robust 'state fingerprint' that catches form changes.
        """
        try:
            content = await page.evaluate("""
                () => {
                    const getSemantic = (root) => {
                        let text = "";
                        // 1. Collect direct text if possible
                        if (root.innerText) text += root.innerText;
                        
                        // 2. Iterate all children to find Shadow Roots and Inputs
                        const walker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT);
                        let node = walker.nextNode();
                        while (node) {
                            // Catch Shadow DOM
                            if (node.shadowRoot) {
                                text += getSemantic(node.shadowRoot);
                            }
                            // Catch Input Values (Very important for detecting fill success!)
                            if (node.tagName === 'INPUT' || node.tagName === 'TEXTAREA' || node.tagName === 'SELECT') {
                                text += `[val:${node.value}]`;
                            }
                            node = walker.nextNode();
                        }
                        return text;
                    };
                    
                    const raw = getSemantic(document.body);
                    // Standardize: remove timestamps, long numbers (IDs), and collapse whitespace
                    return raw
                        .replace(/\\d{10,}/g, '') 
                        .replace(/\\d{2}:\\d{2}(:\\d{2})?/g, '') // Time
                        .replace(/\\s+/g, ' ')
                        .substring(0, 10000);
                }
            """)
            if not content: return None
            return hashlib.md5(content.encode('utf-8')).hexdigest()
        except Exception as e:
            print(f"⚠️ DOM Hash failed: {e}")
            return None
    
    async def is_duplicate_state(self, page_url, mindmap, page=None):
        """
        Check if we are stuck on the same state after an action.
        Now uses robust DOM Hashing + Action Fingerprinting.
        """
        try:
            # Enhanced fingerprint: URL + DOM Hash
            dom_hash = await self.get_dom_hash(page) if page else None
            
            # Fallback to metadata if DOM hash fails or page not provided
            if not dom_hash:
                element_count = len(mindmap.get('elements', []))
                page_title = mindmap.get('summary', {}).get('title', '')
                state_fingerprint = f"{page_url}:{element_count}:{page_title}"
            else:
                state_fingerprint = f"{page_url}:{dom_hash}"
            
            # Action fingerprint: What we just did
            last_action = self.history[-1]['action'] if self.history else 'none'
            last_target = self.history[-1].get('target_text', '') if self.history else 'none'
            # last_value = str(self.history[-1].get('value', '')) if self.history else 'none'
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
                    return self.consecutive_duplicate_count >= 3
                
                # Different action on same state
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
                
        except Exception as e:
            print(colored(f"⚠️ Error in is_duplicate_state: {e}", "yellow"))
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
        Verify if the element is interactable.
        """
        if not locator_str: return False
        
        try:
            loc = page.locator(locator_str)
            if await loc.count() == 0:
                return False
                
            # If it's visible, great!
            if await loc.is_visible(timeout=1500):
                return True
                
            # SPECIAL CASE: If not visible but attached, it might be clickable via coordinates
            # if it's just considered 'hidden' by Playwright due to some CSS quirk (like z-index)
            if await loc.is_attached(timeout=500):
                 # We still return false here BUT _execute_action will check for coordinates
                 # Actually, let's return True if it's attached and it's a click action?
                 # No, better to keep this clean and handle the 'invisible click' in _execute_action.
                 pass

            return False
        except:
            return False


    async def _dismiss_overlays(self, page):
        """World-Class Overlay Handler: Unlocks scroll and hunts for close buttons."""
        try:
            print(colored("🛡️ [World-Class] Handling potential interrupters (Popups/Overlays)...", "magenta"))
            await page.evaluate("""
                () => {
                    // 1. SCROLL UNLOCKER: Force body to be scrollable
                    document.body.style.overflow = 'auto';
                    document.body.style.setProperty('overflow', 'auto', 'important');
                    document.documentElement.style.overflow = 'auto';
                    document.documentElement.style.setProperty('overflow', 'auto', 'important');
                    
                    // 2. SEMANTIC CLOSE HUNTER: Find and click 'X', 'Close', 'Accept', 'Got it'
                    const closeSelectors = [
                        '[aria-label*="Close"]', '[aria-label*="dismiss"]', '[aria-label*="Close" i]',
                        '[class*="close"]', '[id*="close"]',
                        '.close-icon', '.modal-close', '.popup-close',
                        'button:has-text("Accept")', 'button:has-text("Got it")', 'button:has-text("Dismiss")'
                    ];
                    
                    const huntAndClick = (root) => {
                        closeSelectors.forEach(sel => {
                            try {
                                const btns = root.querySelectorAll(sel);
                                btns.forEach(btn => {
                                    const style = window.getComputedStyle(btn);
                                    if (style.display !== 'none' && style.visibility !== 'hidden') {
                                        btn.click();
                                    }
                                });
                            } catch(e) {}
                        });
                        
                        // Recurse into Shadow DOM
                        root.querySelectorAll('*').forEach(el => {
                            if (el.shadowRoot) huntAndClick(el.shadowRoot);
                        });
                    };
                    huntAndClick(document);

                    // 3. NUCLEAR BACKDROP NUKE: Remove blockers
                    const blockers = document.querySelectorAll('[class*="backdrop"], [class*="overlay"], [class*="modal-bg"], [class*="cookie"]');
                    blockers.forEach(b => {
                        const style = window.getComputedStyle(b);
                        const zIndex = parseInt(style.zIndex);
                        if (zIndex > 50 || style.position === 'fixed') {
                            b.remove();
                        }
                    });

                    // 4. PREVENTATIVE: Hide any high z-index element that covers most of the screen
                    document.querySelectorAll('*').forEach(el => {
                        const style = window.getComputedStyle(el);
                        if (parseInt(style.zIndex) > 1000) {
                            const rect = el.getBoundingClientRect();
                            if (rect.width > window.innerWidth * 0.8 && rect.height > window.innerHeight * 0.8) {
                                el.style.display = 'none';
                            }
                        }
                    });
                }
            """)
            # 5. Escape Key (The universal close signal)
            await page.keyboard.press("Escape")
        except Exception as e:
            print(colored(f"   ⚠️ Overlay handler warning: {e}", "yellow"))
    async def handle_infinite_scroll(self, page, max_scrolls=5):
        """
        Smart Infinite Scroll Handler (Crawlee-inspired).
        Scrolls down until no new content is loaded or max_scrolls reached.
        """
        try:
            previous_height = await page.evaluate('document.body.scrollHeight')
            scroll_count = 0
            
            print(colored("📜 Checking for infinite scroll...", "cyan"))
            
            while scroll_count < max_scrolls:
                # Scroll to bottom
                await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                
                # Wait for potential network activity
                try:
                    await page.wait_for_load_state('networkidle', timeout=2000)
                except: 
                    await asyncio.sleep(1) # Fallback wait
                
                # Check height
                current_height = await page.evaluate('document.body.scrollHeight')
                
                if current_height <= previous_height:
                    # No growth? Try one more aggressive scroll to be sure
                    # Sometimes removing 'scroll-behavior: smooth' helps
                    await page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
                    await page.evaluate('window.scrollTo(0, document.body.scrollHeight + 500)')
                    await asyncio.sleep(1)
                    current_height = await page.evaluate('document.body.scrollHeight')
                    if current_height <= previous_height:
                         break # Truly stuck
                
                previous_height = current_height
                scroll_count += 1
                print(colored(f"   ⬇️ Scrolled {scroll_count}/{max_scrolls} (Height: {current_height}px)", "cyan"))
                
            if scroll_count > 0:
                print(colored(f"✅ Infinite scroll complete. Expanded page by {scroll_count} screens.", "green"))
                return True
        except Exception as e:
            print(colored(f"⚠️ Infinite scroll warning: {e}", "yellow"))
        return False

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
            # COORDINATE FALLBACK: If we have coordinates, try them even if 'is_visible' is false
            # This handles elements that are visible to a human/miner but hidden to Playwright's strict check
            if action == 'click' and target_el.get('center'):
                 cx, cy = target_el['center'].get('x'), target_el['center'].get('y')
                 print(colored(f"⚠️ Validation Failed: ID={target_id} not strictly visible. Attempting Coordinate Click at ({cx}, {cy})...", "yellow"))
                 try:
                     if self.headed:
                         await page.evaluate(f"window.showAgentCursor && window.showAgentCursor({cx}, {cy}, 'click')")
                     await page.mouse.click(cx, cy)
                     return {"success": True, "outcome": "Coordinate click executed on ostensibly hidden element", "locator": locator_str}
                 except Exception as e:
                     print(colored(f"   ❌ Coordinate click failed: {e}", "red"))

            print(colored(f"⚠️ Validation Failed: ID={target_id} not visible and no fallback. Attempting overlay dismissal...", "yellow"))
            await self._dismiss_overlays(page)
            is_valid = await self._validate_locator(page, locator_str)
            if not is_valid:
                return {"success": False, "outcome": "Locator validation failed (element not visible or blocked)"}

        refined_locator = await self._refine_locator(page, target_el) if target_el else locator_str
    
    async def _execute_tool_intent(self, page, decision, elements):
        """
        Execute a tool intent from the Planner (NEW PATTERN - replaces _execute_action).
        
        Args:
            page: Playwright Page object
            decision: JSON from Planner with {"tool": "...", "arguments": {...}}
            elements: Current DOM elements
            
        Returns:
            Dict with success status and outcome
        """
        tool_name = decision.get('tool')
        arguments = decision.get('arguments', {})
        
        if not tool_name:
            # Fallback to old pattern if Planner hasn't adapted yet
            if decision.get('action'):
                print(colored("⚠️ Planner used old 'action' format, falling back to legacy executor", "yellow"))
                return await self._execute_action(page, decision, elements)
            return {"success": False, "outcome": "No tool or action specified in decision"}
        
        # ENHANCEMENT: Inject target_el into arguments for precision fallbacks (e.g. coordinates)
        target_id = decision.get('arguments', {}).get('element_id')
        target_el = next((e for e in elements if str(e['elementId']) == str(target_id)), None)
        if target_el:
            decision['arguments']['target_el'] = target_el
            
        # --- VISION-FIRST: Placeholder ID handling ---
        if str(target_id) in ['9991', '9992', '9993']:
            print(colored(f"🎯 [Vision-First] Handling skeletal ID {target_id} via OCR...", "magenta", attrs=["bold"]))
            
            # Special case for "Log in"/"Sign up" button (ID 9993) to use button detection, not label detection
            if str(target_id) == '9993':
                 btn_text = target_el.get('text', 'Log in')
                 success = await self.vision_interactor.click_button_by_text(btn_text)
                 if success:
                     return {"success": True, "outcome": f"Skeletal '{btn_text}' button clicked via OCR"}
                 else:
                     return {"success": False, "outcome": f"Vision failed to find '{btn_text}' button"}

            label = target_el.get('text', 'Username')
            coords = await self.vision_interactor.find_input_by_label(label)
            if coords:
                if tool_name == 'smart_fill':
                    val = decision.get('arguments', {}).get('value', '')
                    await page.mouse.click(coords[0], coords[1])
                    await asyncio.sleep(0.5)
                    await page.keyboard.type(val, delay=50)
                    return {"success": True, "outcome": "Skeletal ID filled via Vision"}
                elif tool_name == 'smart_click':
                    await page.mouse.click(coords[0], coords[1])
                    return {"success": True, "outcome": "Skeletal ID clicked via Vision"}
            return {"success": False, "outcome": f"Vision failed to locate skeletal label '{label}'"}

        print(colored(f"\n🔧 EXECUTING TOOL: {tool_name}", "cyan"))
        
        # Adjust timeout for Vision-First mode (fail faster to DOM so we can use Vision)
        if self.vision_first_mode:
            print(colored("⏳ [Vision-First] Using 5s DOM interaction timeout", "grey"))
            if 'arguments' not in decision: decision['arguments'] = {}
            decision['arguments']['interaction_timeout'] = 5000

        # Execute the tool through ToolExecutor
        result = await self.tool_executor.execute_intent(page, decision)
        
        # --- VISION RECOVERY ---
        if result.get("status") == "failure" and self.vision_first_mode and self.vision_interactor:
            err = result.get("error", "").lower()
            if any(k in err for k in ["visible", "timeout", "intercepts", "hidden", "attached"]):
                print(colored("🔄 [Vision Recovery] DOM interaction failed. Attempting OCR fallback...", "magenta", attrs=["bold"]))
                label = target_el.get('text', '') if target_el else ""
                if label and tool_name in ['smart_click', 'smart_fill']:
                    coords = await self.vision_interactor.find_input_by_label(label)
                    if coords:
                        await page.mouse.click(coords[0], coords[1])
                        if tool_name == 'smart_fill':
                            await asyncio.sleep(0.5)
                            await page.keyboard.type(decision.get('arguments', {}).get('value', ''), delay=50)
                        return {"success": True, "outcome": "Recovered via Vision OCR"}

        # Convert ToolExecutor result to legacy format for compatibility
        return {
            "success": result.get("status") == "success",
            "outcome": result.get("error") if result.get("status") == "failure" else f"Tool '{tool_name}' executed successfully"
        }

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
            # COORDINATE FALLBACK: If we have coordinates, try them even if 'is_visible' is false
            # This handles elements that are visible to a human/miner but hidden to Playwright's strict check
            if action == 'click' and target_el.get('center'):
                 cx, cy = target_el['center'].get('x'), target_el['center'].get('y')
                 print(colored(f"⚠️ Validation Failed: ID={target_id} not strictly visible. Attempting Coordinate Click at ({cx}, {cy})...", "yellow"))
                 try:
                     if self.headed:
                         await page.evaluate(f"window.showAgentCursor && window.showAgentCursor({cx}, {cy}, 'click')")
                     await page.mouse.click(cx, cy)
                     return {"success": True, "outcome": "Coordinate click executed on ostensibly hidden element", "locator": locator_str}
                 except Exception as e:
                     print(colored(f"   ❌ Coordinate click failed: {e}", "red"))

            print(colored(f"⚠️ Validation Failed: ID={target_id} not visible and no fallback. Attempting overlay dismissal...", "yellow"))
            await self._dismiss_overlays(page)
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
                print(colored(f"⌨️  Interacting with ID={target_id}...", "yellow"))
                try:
                    # 1. Click to focus and CLEAR existing content
                    await page.locator(locator_str).click(timeout=5000)
                    
                    # Select all and delete (Robust clear for SPAs)
                    await page.keyboard.down('Control')
                    await page.keyboard.press('a')
                    await page.keyboard.up('Control')
                    await page.keyboard.press('Backspace')
                    
                    # 2. Use natural typing
                    await page.locator(locator_str).type(val, delay=40) 
                    
                    # 3. Enter key if requested OR if the element is clearly a search input 
                    # OR if the goal looks like a search and we are filling a text-like input
                    is_search_context = any(kw in self.workflow.lower() for kw in ['search', 'find', 'lookup', 'query', 'check price'])
                    is_input_element = target_el.get('tagName') in ['input', 'textarea'] or target_el.get('role') == 'searchbox'
                    text_lower = target_el.get('text', '').lower()
                    attr_lower = str(target_el.get('attributes', {})).lower()
                    looks_like_search = 'search' in text_lower or 'search' in attr_lower or 'query' in attr_lower
                    
                    if val.endswith('\n') or (is_input_element and (looks_like_search or is_search_context)):
                         print(colored("   ⌨️ Search pattern detected. Pressing Enter...", "cyan"))
                         await page.keyboard.press("Enter")
                         await asyncio.sleep(3) # Heavy wait for search results
                         
                    print(colored(f"   ✅ Entered: '{val}'", "green"))
                except Exception as e:
                    print(colored(f"   ⚠️ Interaction failed: {e}. Trying simple fill...", "yellow"))
                    await page.locator(locator_str).fill(val, timeout=5000)
            
            elif action == 'navigate':
                url = decision.get('value')
                print(colored(f"🌐 Navigating to {url}", "yellow"))
                # Robust navigate with timeout and wait state
                await page.goto(url, wait_until="load", timeout=60000)
                await asyncio.sleep(1) # Extra settlement time
                
            elif action == 'scroll_down':
                print(colored(f"📜 Scrolling down...", "yellow"))
                await page.mouse.wheel(0, 600)
                await asyncio.sleep(1)

            elif action == 'scroll_up':
                print(colored(f"📜 Scrolling up...", "yellow"))
                await page.mouse.wheel(0, -600)
                await asyncio.sleep(1)

            elif action == 'press_enter':
                print(colored(f"⌨️ Pressing Enter...", "yellow"))
                await page.keyboard.press("Enter")
                await asyncio.sleep(2)

            elif action == 'hover':
                print(colored(f"🖱️ Hovering over ID={target_id}", "yellow"))
                # Coordinate hover fallback if visibility fails
                if target_el.get('center') and target_el['center'].get('x') is not None and target_el['center'].get('y') is not None:
                     cx, cy = target_el['center'].get('x'), target_el['center'].get('y')
                     await page.mouse.move(cx, cy)
                else:
                     await page.locator(locator_str).hover(timeout=5000)
                await asyncio.sleep(1)
                
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

    def _build_locators_array(self, decision, action_result, elements, step, page, current_screenshot_path=None):
        """
        Build multi-locator array for robust replay with visual fallback.
        Returns array of locator dictionaries with different strategies.
        """
        locators = []
        action = decision.get('tool') or decision.get('action', '')
        arguments = decision.get('arguments', {})
        
        # Extract what we clicked/filled from tool arguments
        selector = arguments.get('selector')
        text = arguments.get('text') or arguments.get('query')
        
        # 1. CSS Locator (from action_result or arguments)
        css_locator = (
            action_result.get('refined_locator') or 
            action_result.get('locator') or 
            selector
        )
        if css_locator and css_locator != text:  # Don't add if it's just text
            locators.append({
                "type": "css",
                "value": css_locator,
                "priority": 1,
                "success_count": 0
            })
        
        # 2. Text Locator (from arguments or action result)
        if text and len(text) < 100:
            locators.append({
                "type": "text",
                "value": text,
                "priority": 2,
                "success_count": 0
            })
            
            # 2b. Add synthetic CSS/XPath selectors as fallbacks
            if action == "smart_click":
                # CSS: Anchor with exact text
                locators.append({
                    "type": "css",
                    "value": f"a:has-text('{text}')",
                    "priority": 3,
                    "success_count": 0
                })
                
                # XPath: Link or button containing text
                locators.append({
                    "type": "xpath",
                    "value": f"//a[contains(text(), '{text}')] | //button[contains(text(), '{text}')]",
                    "priority": 4,
                    "success_count": 0
                })
                
                # CSS: Aria-label match
                locators.append({
                    "type": "css",
                    "value": f"[aria-label*='{text}' i]",  # Case-insensitive
                    "priority": 5,
                    "success_count": 0
                })
        
        # 3. Try to find element in mindmap for additional context (bbox, role)
        target_id = decision.get('target_id')
        target_element = None
        
        if target_id:
            target_element = next((e for e in elements if str(e['elementId']) == str(target_id)), None)
        elif text:
            # Fallback: Robust element finding strategy when target_id is missing
            
            # 1. Try Exact Match (stripped)
            target_element = next((e for e in elements if e.get('text', '').strip() == text), None)
            
            # 2. Try Case-Insensitive Match
            if not target_element:
                target_element = next((e for e in elements if e.get('text', '').strip().lower() == text.lower()), None)
                
            # 3. Try Partial Match (text in element_text)
            if not target_element:
                candidates = [e for e in elements if text.lower() in e.get('text', '').strip().lower()]
                
                # Filter candidates by role if possible
                interactive_candidates = [e for e in candidates if e.get('role') in ['link', 'button', 'menuitem']]
                
                if interactive_candidates:
                    # Pick the shortest text match (most specific)
                    target_element = min(interactive_candidates, key=lambda e: len(e.get('text', '')))
                elif candidates:
                    target_element = min(candidates, key=lambda e: len(e.get('text', '')))
            
        # 4. Role Locator (if we have element context OR can infer from action)
        if target_element:
            role = target_element.get('role', '')
            elem_text = target_element.get('text', '').strip()
            if role and elem_text:
                locators.append({
                    "type": "role",
                    "value": f"{role}[name='{elem_text[:50]}']",
                    "priority": 4,
                    "success_count": 0
                })
        elif text and action == "smart_click":
            # Infer likely role (link for clicks)
            locators.append({
                "type": "role",
                "value": f"link[name='{text[:50]}']",
                "priority": 4,
                "success_count": 0
            })
        
        # 5. Visual Template (if we have bbox and screenshot)
        if target_element and target_element.get('bbox') and current_screenshot_path and os.path.exists(current_screenshot_path):
            try:
                template_dir = os.path.join(self.output_dir, 'element_templates')
                os.makedirs(template_dir, exist_ok=True)
                
                bbox = target_element['bbox']
                template_filename = f"step_{step:02d}_element_{target_id or 'text'}_{step}.png"
                template_path = os.path.join('element_templates', template_filename)
                full_template_path = os.path.join(self.output_dir, template_path)
                
                # Crop and save template using OpenCV
                img = cv2.imread(current_screenshot_path)
                if img is not None:
                    x, y, w, h = bbox
                    # Ensure coordinates are within bounds
                    h_img, w_img, _ = img.shape
                    x = max(0, min(x, w_img-1))
                    y = max(0, min(y, h_img-1))
                    w = max(1, min(w, w_img-x))
                    h = max(1, min(h, h_img-y))
                    
                    crop = img[y:y+h, x:x+w]
                    cv2.imwrite(full_template_path, crop)
                    
                    locators.append({
                        "type": "visual",
                        "template": template_path.replace('\\', '/'),  # Normalize for cross-platform check
                        "priority": 5,
                        "success_count": 0,
                        "bbox": bbox
                    })
                    print(colored(f"      📸 Captured visual template: {template_filename}", "cyan"))
                
            except Exception as e:
                print(colored(f"⚠️ Failed to setup visual template: {e}", "yellow"))
        
        return locators

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
        # Support multiple formats: "1.", "1:", "Step 1:", "1) "
        step_pattern = r'(?:Step\s+)?(\d+)[.:)]\s*(.*?)(?=\s*(?:Step\s+)?\d+[.:)]\s*|$)'
        matches = re.findall(step_pattern, goal_text, re.DOTALL | re.IGNORECASE)
        
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
            if step_meta['step_num'] in self.skipped_goal_steps:
                continue  # Skip already completed steps
            
            step_keywords = [w.lower() for w in step_meta['description'].split() if len(w) > 3]
            recent_actions = ' '.join([h.get('target_text', '') for h in self.history[-5:]]).lower()
            page_content = mindmap['summary'].get('title', '').lower()
            
            # If recent actions or page content match this step's keywords
            if any(keyword in recent_actions or keyword in page_content for keyword in step_keywords[:3]):
                return step_meta
        
        # Default: Return first incomplete step
        for step_meta in self.parsed_goal:
            if step_meta['step_num'] not in self.skipped_goal_steps:
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
