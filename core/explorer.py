
import asyncio
import json
import os
import sys
from playwright.async_api import async_playwright, Page
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from termcolor import colored

# Import agents
import sys
os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
from miner import analyze_page
from knowledge_bank import KnowledgeBank

load_dotenv()

# Initialize 2026-ready LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.0,
    response_mime_type="application/json"
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

**THINKING PROCESS:**
1. Observe: What page am I on?
2. History Check: Review `history` carefully. What have I ALREADY DONE? Use element text and URLs to verify.
3. Validate: Did my LAST action work? Note: On SPAs, the URL might not change even if the content does.
4. Multi-Goal Check: Look at the `goal`. Does it have multiple steps (e.g., '1. Home, 2. Price')? Check off completed steps based on history.
5. **Login Check**: If I encounter a login page and NO credentials are in `test_data`, SKIP login entirely. Instead, explore publicly accessible areas like footer links, documentation, pricing pages, or the homepage navigation.
6. Select: Which element ID from the list corresponds to the NEXT unfulfilled part of the goal?

**OUTPUT SCHEMA (JSON only)**:
{
  "thought": "Direct explanation of which part of the goal is being addressed and why this action moves us closer.",
  "action": "click | fill | scroll | long_press | navigate | done",
  "target_id": 5, 
  "value": "...", 
  "expected_outcome": "Description of expected UI change",
  "is_goal_achieved": false 
}
**CRITICAL**: Set `is_goal_achieved` to `true` ONLY if EVERY part of the user's workflow description is completed.
}
"""

def try_parse_json(content):
    import re
    content = re.sub(r'```json\s*', '', content)
    content = re.sub(r'\s*```', '', content)
    content = content.strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r'(\{.*\})', content, re.DOTALL)
        if match:
            try: return json.loads(match.group(1))
            except: pass
    return None

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
        self.output_dir = self.config.get("paths", {}).get("outputs", "outputs")
        os.makedirs(self.output_dir, exist_ok=True)
        self.history = []
        
        # State deduplication and loop detection
        self.visited_states = set()  # Track unique page states
        self.loop_detection_window = 3  # Check last N steps for patterns

    async def run(self):
        print(colored(f"Explorer: Starting Strategy 2026. Goal: {self.workflow}", "blue", attrs=["bold"]))
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=not self.headed)
            context = await browser.new_context(viewport={"width": 1280, "height": 800})
            page = await context.new_page()
            
            try:
                await page.goto(self.config["target_url"], wait_until="networkidle", timeout=60000)
            except:
                await page.wait_for_load_state("domcontentloaded")

            step = 0
            max_steps = 20
            
            while step < max_steps:
                print(colored(f"\n--- Step {step + 1} ---", "white", attrs=["bold"]))
                
                # 1. ANALYZE (Miner)
                mindmap = await analyze_page(page, page.url, self.workflow)
                
                # Save screenshot for trace
                img_name = f"step_{step}_pre.png"
                img_path = os.path.join(self.output_dir, img_name)
                await page.screenshot(path=img_path)
                
                print(f"📍 On Page: {mindmap['summary'].get('title', 'Unknown')}")
                print(f"🤔 State: {mindmap['summary'].get('state', 'Unknown')}")
                
                # Check for duplicate states (infinite loop prevention)
                if self.is_duplicate_state(page.url, mindmap):
                    print(colored("⚠️ Duplicate state detected. Exiting to prevent infinite loop.", "yellow"))
                    break
                
                # Check for stuck loops (circular navigation)
                if self.detect_stuck_loop():
                    print(colored("⚠️ Stuck in repetitive pattern. Breaking out.", "yellow"))
                    break
                
                # 2. PLAN (Decider)
                print(f"📡 Sending {len(mindmap['elements'])} elements to the Planner...")
                decision = await self._make_decision(mindmap)
                if not decision: 
                    print(colored("❌ Failed to make a decision.", "red"))
                    break
                
                print(colored(f"💭 Thought: {decision.get('thought')}", "cyan"))
                
                if decision.get('is_goal_achieved') or decision.get('action') == 'done':
                    print(colored("✅ Goal Achieved!", "green", attrs=["bold"]))
                    break
                
                # 3. ACT
                action_result = await self._execute_action(page, decision, mindmap['elements'])
                
                # 4. VALIDATE & LOG
                self.history.append({
                    "step": step,
                    "action": decision['action'],
                    "target_text": next((e['text'] for e in mindmap['elements'] if str(e['elementId']) == str(decision.get('target_id'))), ""),
                    "url": page.url,
                    "outcome": action_result.get('outcome'),
                    "success": action_result.get('success'),
                })
                
                # Update trace for Refiner
                self.trace.append({
                    "step": step,
                    "thought": decision['thought'],
                    "action": decision['action'],
                    "locator_used": action_result.get('refined_locator') or action_result.get('locator'),
                    "value": decision.get('value'),
                    "url": page.url,
                    "screenshot": img_name,
                    # Capturing rich context for composite locators
                    "element_context":  {
                        "tag": next((e['tagName'] for e in mindmap['elements'] if str(e['elementId']) == str(decision.get('target_id'))), ""),
                        "text": next((e['text'] for e in mindmap['elements'] if str(e['elementId']) == str(decision.get('target_id'))), ""),
                        "role": next((e.get('role', '') for e in mindmap['elements'] if str(e['elementId']) == str(decision.get('target_id'))), ""),
                         # We can add more like class later if dom_driver sends it
                    }
                })
                self._save_trace()
                
                # Passive Collection: Save ALL elements
                self._save_all_elements(page.url, step, mindmap['elements'])
                
                step += 1
                if not action_result.get('success'):
                    print(colored(f"⚠️ Action failed. Retrying...", "yellow"))

            # Save Trace
            self._save_trace()
            await browser.close()

    async def _make_decision(self, mindmap):
        context = {
            "goal": self.workflow,
            "page_context": mindmap['summary'],
            "elements": [{"id": e['elementId'], "text": e['text'], "tag": e['tagName']} for e in mindmap['elements'][:100]],
            "history": self.history[-10:], # Expanded history for navigation memory
            "test_data": self.test_data
        }
        
        prompt = f"Current Mindmap Context:\n{json.dumps(context, indent=2)}"
        
        try:
            resp = llm.invoke([("system", SYSTEM_PROMPT_PLANNER), ("human", prompt)])
            return try_parse_json(resp.content)
        except Exception as e:
            print(f"Error in decision: {e}")
            return None
    
    def is_duplicate_state(self, page_url, mindmap):
        """Check if we've visited this exact page state before to prevent infinite loops."""
        # Create fingerprint: URL + element count + page title
        element_count = len(mindmap.get('elements', []))
        page_title = mindmap.get('summary', {}).get('title', '')
        fingerprint = f"{page_url}:{element_count}:{page_title}"
        
        if fingerprint in self.visited_states:
            return True
        
        self.visited_states.add(fingerprint)
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
                return True
        
        return False

    async def _execute_action(self, page, decision, elements):
        action = decision['action']
        target_id = decision.get('target_id')
        target_el = next((e for e in elements if str(e['elementId']) == str(target_id)), None)
        
        if not target_el and action in ['click', 'fill']:
            return {"success": False, "outcome": "Target element ID not found in current DOM"}
        
        locator_str = f"[data-agent-id='{target_id}']"
        
        # Refinement Step: Get a stable locator for the final test script BEFORE it potentially evaporates
        refined_locator = await self._refine_locator(page, target_el) if target_el else locator_str

        try:
            if action == 'click':
                print(colored(f"🖱️ Clicking ID={target_id} ({target_el['text']})", "yellow"))
                # 2026 Strategy: Try locator, fallback to coordinates
                try:
                    await page.locator(locator_str).click(timeout=5000)
                except:
                    print(colored("   👉 Locator failed. Using coordinate fallback.", "magenta"))
                    await page.mouse.click(target_el['center']['x'], target_el['center']['y'])
                
            elif action == 'fill':
                val = decision.get('value', '')
                print(colored(f"⌨️ Filling ID={target_id} with '{val}'", "yellow"))
                try:
                    await page.locator(locator_str).fill(val, timeout=5000)
                except:
                    print(colored("   👉 Locator failed. Using coordinate fallback.", "magenta"))
                    await page.mouse.click(target_el['center']['x'], target_el['center']['y'])
                    await page.keyboard.type(val)
            
            elif action == 'navigate':
                url = decision.get('value')
                print(colored(f"🌐 Navigating to {url}", "yellow"))
                await page.goto(url)
                
            elif action == 'scroll':
                print(colored("📜 Scrolling down...", "yellow"))
                await page.keyboard.press("PageDown")
                await asyncio.sleep(0.5)
                
            elif action == 'long_press':
                print(colored(f"👆 Long-pressing ID={target_id} (10s)...", "yellow"))
                # Use coordinates for maximum reliability on custom widgets
                x, y = target_el['center']['x'], target_el['center']['y']
                await page.mouse.move(x, y)
                await page.mouse.down()
                await asyncio.sleep(10)
                await page.mouse.up()

            return {
                "success": True, 
                "outcome": "Action executed", 
                "locator": locator_str,
                "refined_locator": refined_locator
            }
            
        except Exception as e:
            return {"success": False, "outcome": str(e)}

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
                        const classes = el.className.split(' ').filter(c => c.trim().length > 0 && !c.includes('hover') && !c.includes('active'));
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
        trace_path = self.config.get("paths", {}).get("trace", "trace.json")
        os.makedirs(os.path.dirname(trace_path), exist_ok=True)
        with open(trace_path, "w") as f:
            json.dump({
                "workflow": self.workflow, 
                "target_url": self.config["target_url"],
                "trace": self.trace
            }, f, indent=2)
        print(colored(f"💾 Trace saved to {trace_path}", "green"))

    def _save_all_elements(self, url, step, elements):
        """Passive Collection: Save all discovered elements for future reference"""
        path = self.config.get("paths", {}).get("outputs", "outputs")
        file_path = os.path.join(path, "discovered_elements.json")
        
        data = {}
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                try: data = json.load(f)
                except: data = {}
        
        key = f"{url}::step_{step}"
        data[key] = elements
        
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
