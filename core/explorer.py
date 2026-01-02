import asyncio
import json
import os
from playwright.async_api import async_playwright
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Reuse miner logic
import sys
sys.path.append(os.path.dirname(__file__))
from miner import analyze_page

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.0,
    model_kwargs={"response_mime_type": "application/json"}
)

SYSTEM_PROMPT_DECIDER = """
You are an Autonomous Browser Agent.
Your goal is to complete the User's Workflow by interacting with the page.

**INPUTS:**
1. `user_workflow`: The high-level goal.
2. `current_page_summary`: What page we are on.
3. `available_elements`: List of clickable/fillable items with LOators.
4. `history`: List of actions taken so far.
5. `test_data`: Data available to use (username, password, zip, etc).

**OUTPUT:**
A JSON object deciding the NEXT action:
{
  "thought": "No login credentials found. I will look for a Register or Sign Up link to create a new user account.",
  "action": "fill" | "click" | "navigate" | "scroll" | "done",
  "target_element_id": "el_0" (from available_elements) OR null,
  "expected_outcome": "Description of what should happen (e.g., 'Page redirects to /dashboard')",
  "value_to_fill": "standard_user" (if fill),
  "scroll_direction": "down" | "up" | "to_element",
  "is_goal_achieved": false
}

**RULES:**
1. **CHECK STATE & GOAL**:
   - If you see "Welcome [User]", "Log Out", or "Overview", you are **LOGGED IN**.
   - If goal is "Login": You are DONE. Set `is_goal_achieved: true`.
   - If goal is "Register" and you are logged in: **SKIP** registration and assume success, OR logout ONLY if strictly necessary.
   - **DO NOT LOGOUT** proactively. Assume current session is valid for next steps (Transfer, etc).

2. **CREDENTIALS**: Check `test_data` FIRST.
   - If `test_data` has 'username' and 'password', USE THEM to login.
   - Do NOT Register if you have valid credentials, unless goal explicitly says "Create New User".

3. **REGISTRATION FORMS**: If you see multiple empty input fields (firstName, lastName, address, etc):
   - NEVER click "Register" or "Submit" until ALL required fields are filled
   - Fill fields ONE AT A TIME in sequence: First Name → Last Name → Address → City → State → Zip → Phone → SSN → Username → Password → Confirm
   - Generate realistic data: 
     * Names: "John Doe", "Jane Smith"
     * Address: "123 Main Street" 
     * City: "New York", State: "NY", Zip: "10001"
     * Phone: "555-1234", SSN: "123-45-6789"
     * Username: "user_" + random, Password: "Test@1234"
   - ONLY click submit after seeing all fields have values

4. **PRIORITIZATION**: If you have no credentials in `test_data` and aren't logged in, PRIORITIZE finding a "Register" link.

5. **SCROLLING**: If you can't find a target element, use "scroll".

6. Look at `history` to avoid repeating loops.

7. **VERIFY SUCCESS**: After submitting a form, LOOK for success messages (e.g., "created successfully", "Welcome"). If found, set `is_goal_achieved: true`.

8. **STAY FOCUSED**:
   - **DO NOT** click "Forum", "Products", "Locations", "About Us", or external links.
   - **STAY ON** the main banking application.
   - If you end up on `forums.parasoft.com` or `parasoft.com`, usually you made a mistake. Navigate BACK immediately.

9. **CHECK VALUES**: If an input already has the correct value, DO NOT fill it again.

10. **TOGGLE STATES**: If goal is "Add X" and the button says "Remove", it means X is ALREADY added.

11. **NEXT STEP**: If X is added, find "shopping_cart_link" or "checkout" and CLICK IT.
"""

# Knowledge Management
from knowledge_bank import KnowledgeBank

class ExplorerAgent:
    def __init__(self, config_path):
        with open(config_path, "r") as f:
            self.config = json.load(f)
        self.workflow = self.config["workflow_description"]
        self.test_data = self.config.get("test_data", {})
        self.trace = []
        self.domain_knowledge = {}
        self.kb = KnowledgeBank()
        self.knowledge_context = self.kb.get_rag_context(self.config["target_url"], self.workflow)
        self.total_cost = {"input": 0, "output": 0}

    async def explore(self):
        print(f"🚀 Explorer Starting. Goal: {self.workflow}")
        
        step_count = 0
        consecutive_failures = 0
        loop_blacklist = set()
        repetition_count = 0
        last_target = None
        last_action = None
        
        # Path for cache
        cache_path = self.config.get("paths", {}).get("cache", "locator_cache.json")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context() 
            page = await context.new_page()
            
            # Start - with longer timeout for production sites
            await page.goto(self.config["target_url"], timeout=60000)  # 60 seconds
            active_page = page
            step_count = 0
            max_steps = 60 # Safety limit increased for full flows
            consecutive_failures = 0
            
            while step_count < max_steps:
                print(f"\n--- Step {step_count + 1} ---")
                
                # 1. Analyze
                try:
                    await active_page.wait_for_load_state("networkidle", timeout=60000)  # 60s for production
                except:
                    # If networkidle times out, continue anyway (some sites never reach it)
                    print("   ⏭️ Skipping networkidle wait (site may use lazy loading)")
                
                # Force refresh if we had a failure last time
                force_refresh = (consecutive_failures > 0)
                
                page_data = await analyze_page(active_page, active_page.url, 
                                               knowledge_context=self.knowledge_context,
                                               cache_path=cache_path,
                                               force_refresh=force_refresh)
                
                # Check for empty locators
                if not page_data['locators']:
                    print("⚠️ No locators found. Retrying with force refresh...")
                    consecutive_failures += 1
                    if consecutive_failures > 3:
                        print("❌ Too many failures. Ending exploration.")
                        break
                    await asyncio.sleep(2)
                    continue

                # Update Domain Knowledge
                self.domain_knowledge[active_page.url] = page_data["summary"]
                print(f"📍 On Page: {page_data['summary']['page_name']}")
                
                # Discovered Test Data
                extracted = page_data["summary"].get("extracted_test_data", {})
                if extracted:
                    print(f"💎 Discovered Test Data: {json.dumps(extracted)}")
                    self.test_data.update(extracted)
                    self._save_test_data()
                
                # 2. Decide
                # Loop Warning Logic
                feedback_msg = None
                if repetition_count == 1:
                    feedback_msg = f"⚠️ SYSTEM ALERT: You performed '{last_action}' on '{last_target}' in the previous step. It seems you are stuck. Please try a DIFFERENT method or element."

                # 2. Decide
                decision = await self._make_decision(page_data, loop_blacklist, feedback_msg)
                print(f"🤔 AI Thought: {decision['thought']}")
                
                # LOOP DETECTION
                target_id = decision.get('target_element_id')
                action = decision.get('action')
                
                if last_target and target_id == last_target and action == last_action:
                    repetition_count += 1
                else:
                    repetition_count = 0
                
                last_target = target_id
                last_action = action
                
                if repetition_count >= 2:
                    print(f"🛑 Loop Detected on {target_id}. Blacklisting and skipping.")
                    loop_blacklist.add(target_id)
                    # Record failure to help training
                    self.trace.append({
                        "step": step_count,
                        "url": active_page.url,
                        "page_name": page_data['summary']['page_name'],
                        "action": action,
                        "target": target_id,
                        "success": False,
                        "decision_reason": "Loop Detected - Skipped",
                        "expected_outcome": "Break Loop"
                    })
                    step_count += 1
                    continue
                
                if decision['is_goal_achieved'] or decision['action'] == 'done':
                    print("🎉 Goal Achieved (according to AI)!")
                    break
                    
                # 3. Act
                result = await self._execute_action(active_page, decision, page_data['locators'])
                loc_str = result.get('locator')
                
                if not loc_str:
                    print("⚠️ Action failed or target not found.")
                    consecutive_failures += 1
                    await asyncio.sleep(2)
                    continue
                
                # TAB SWITCHING: If a new page was opened, switch to it!
                if result.get('new_page'):
                    active_page = result['new_page']
                    print(f"🔄 Switched to new tab: {active_page.url}")
                
                # Reset failure count on success
                consecutive_failures = 0
                
                # 4. Record
                # Capture credentials if generated/filled
                if decision['action'] == 'fill' and decision.get('value_to_fill'):
                    val = decision['value_to_fill']
                    target_id = decision['target_element_id']
                    
                    # Find element name/type to identify credential fields
                    target_el = next((e for e in page_data['locators'] if e.get('elementId') == target_id), None)
                    if target_el:
                        # Heuristic: Check name/id/type
                        # Check various attributes for keywords
                        el_name = (target_el.get('name') or '').lower()
                        el_id = (target_el.get('id') or '').lower()
                        el_type = (target_el.get('type') or '').lower()
                        
                        key = None
                        if 'user' in el_name or 'login' in el_name or 'email' in el_name or 'user' in el_id:
                            key = 'username'
                        elif 'pass' in el_name or 'pass' in el_id or el_type == 'password':
                            key = 'password'
                        elif 'ssn' in el_name or 'ssn' in el_id:
                            key = 'ssn'
                        
                        if key:
                            print(f"🔐 Captured Credential: {key} = {val}")
                            self.test_data[key] = val
                            self._save_test_data()

                self.trace.append({
                    "step": step_count,
                    "url": active_page.url,
                    "page_name": page_data['summary']['page_name'],
                    "action": decision['action'],
                    "target": decision.get('target_element_id'),
                    "locator_used": loc_str,
                    "success": result.get("success", False),
                    "value": decision.get('value_to_fill'),
                    "decision_reason": decision['thought'],
                    "expected_outcome": decision.get('expected_outcome')
                })
                
                step_count += 1
                await asyncio.sleep(2) # Slow down for visibility
                
            # Done
            await self._save_trace()
            await browser.close()
            
    async def _make_decision(self, page_data, blacklist=None, feedback=None):
        if blacklist is None: blacklist = set()
        
        # Simplify elements for LLM context
        simple_elements = []
        for el in page_data['locators']:
            # Skip blacklisted elements (Loop Breaking)
            if el.get('elementId') in blacklist:
                continue
                
            # Find best locator string for context
            candidates = el.get("locatorCandidates", [])
            best_loc = candidates[0]['playwrightLocator'] if candidates else "unknown"
            
            simple_elements.append({
                "id": el.get('elementId'),
                "text": el.get('visibleText', ''),
                "current_value": el.get('value', ''), # Pass value to AI
                "role": el.get('role', ''),
                "testId": el.get('dataTestId', ''),
                "customTestId": el.get("xpath") or el.get("dataTestId"), # Fallback
                "locator_hint": best_loc
            })
            
        user_msg = f"""
        Workflow: {self.workflow}
        Current Page: {page_data['summary']}
        RAG Knowledge Context: {self.knowledge_context}
        Test Data: {json.dumps(self.test_data)}
        History: {[f"{t['action']} on {t['page_name']}" for t in self.trace]}
        
        Available Elements:
        {json.dumps(simple_elements[:60])}
        """
        
        if feedback:
            user_msg += f"\n\n{feedback}\n"
        
        resp = llm.invoke([("system", SYSTEM_PROMPT_DECIDER), ("human", user_msg)])
    
    # Capture AI Cost
    if hasattr(resp, 'response_metadata'):
        usage = resp.response_metadata.get('token_usage', {}) or resp.response_metadata.get('usage_metadata', {})
        self.total_cost["input"] += usage.get('prompt_tokens', 0)
        self.total_cost["output"] += usage.get('completion_tokens', 0)
        # print(f"💰 Decision Cost: {usage.get('prompt_tokens', 0)} in, {usage.get('completion_tokens', 0)} out")
        try:
            decision = json.loads(resp.content.replace("```json", "").replace("```", "").strip())
        except:
            print(f"⚠️ Failed to parse LLM response: {resp.content}")
            return {"action": "wait", "thought": "Error parsing response", "is_goal_achieved": False}
            
        if "is_goal_achieved" not in decision:
            decision["is_goal_achieved"] = False
        return decision
        
    async def _execute_action(self, page, decision, locators):
        if decision['action'] == 'navigate':
            # Not really used if we click links, but supported
            return {"locator": None, "new_page": None}
        
        elif decision['action'] == 'scroll':
            # Handle scroll before trying to find element
            direction = decision.get('scroll_direction', 'down')
            print(f"📜 Scrolling {direction} to discover elements...")
            
            if direction == 'down':
                await page.keyboard.press("PageDown")
                await asyncio.sleep(0.5)
                await page.mouse.wheel(0, 600)
            elif direction == 'up':
                await page.keyboard.press("PageUp")
                await page.mouse.wheel(0, -600)
            
            await asyncio.sleep(1)
            return {"locator": "scroll", "new_page": None}
            
        elif decision['action'] in ['click', 'fill']:
            target_id = decision['target_element_id']
            # Find full element data
            target_el = next((e for e in locators if e.get('elementId') == target_id), None)
            
            if not target_el:
                print("❌ Target element not found in mined data!")
                return {"locator": None, "new_page": None}
                
            # Pick best locator
            candidates = target_el.get('locatorCandidates', [])
            # Prioritize GOOD strength
            best_cand = next((c for c in candidates if c['strength'] == 'GOOD'), candidates[0] if candidates else None)
            
            if not best_cand:
                print("❌ No valid candidate locator found.")
                return 

            loc_str = best_cand['playwrightLocator']
            
            # Clean locator string for eval (simple hack for now, better to use proper parser later)
            # Remove "page." prefix if it exists to genericize
            # Actually, since we are in python, we might need to eval it or parse it.
            # For robustness, let's try to extract the selector
            
            # Quick hack: If it's `page.locator('...')`, extract inside.
            # If `page.getBy...(...)`, use that.
            
            print(f"⚡ Executing {decision['action']} on {loc_str}")
            
            # We will use the LOCATOR STRING directly via eval in a lambda or simple parsing
            # But `loc_str` is a string like "page.getByTestId('user-name')". 
            # We need to map this to the actual page object.
            
            # Dynamic execution helper
            try:
                # remove 'page.' prefix
                method_call = loc_str.replace("page.", "", 1)
                
                # Safe approach: Using specific methods
                locator = None
                if "getByTestId" in loc_str:
                    val = loc_str.split("'")[1]
                    locator = page.get_by_test_id(val)
                elif "getByRole" in loc_str:
                    import re
                    pythonic_loc = loc_str.replace("getByRole", "get_by_role")
                    pythonic_loc = re.sub(r'\{\s*name:\s*[\'"](.*?)[\'"]\s*\}', r'name="\1"', pythonic_loc)
                    locator = eval(pythonic_loc, {"page": page, "re": re})
                elif "locator" in loc_str:
                     import re
                     match = re.search(r"locator\(['\"](.*)['\"]\)", loc_str)
                     if match:
                         locator = page.locator(match.group(1))
                
                if not locator:
                     # Last resort eval with snake_case mapping
                     import re # inject re for regex
                     # Map JS-style methods to Python snake_case
                     pythonic_loc = loc_str
                     # Convert { name: '...' } to name='...'
                     pythonic_loc = re.sub(r'\{\s*name:\s*[\'"](.*?)[\'"]\s*\}', r'name="\1"', pythonic_loc)
                     
                     for js, py in [
                         ("getByTestId", "get_by_test_id"), ("getByRole", "get_by_role"),
                         ("getByText", "get_by_text"), ("getByPlaceholder", "get_by_placeholder"),
                         ("getByLabel", "get_by_label"), ("getByTitle", "get_by_title"),
                         ("getByAltText", "get_by_alt_text")
                     ]:
                         pythonic_loc = pythonic_loc.replace(js, py)
                     
                     locator = eval(pythonic_loc, {"page": page, "re": re})

                     # ---------------------------------------------------------
                     # SELF-HEALING: Ambiguity Handler
                     # If locator matches multiple elements, prioritize the VISIBLE one.
                     # This solves "Strict Mode" errors and prevents interacting with hidden/overlay elements.
                     # ---------------------------------------------------------
                     try:
                         count = await locator.count()
                         if count > 1:
                             print(f"   ⚠️ Ambiguous Locator: Found {count} matches for {loc_str}. Filtering for visibility...")
                             found_visible = False
                             for i in range(count):
                                 try:
                                     # Check visibility with short timeout
                                     if await locator.nth(i).is_visible(timeout=500):
                                         locator = locator.nth(i)
                                         print(f"   ✅ Self-Healed: Selected match #{i+1} (Visible)")
                                         found_visible = True
                                         break
                                 except: pass
                             
                             if not found_visible:
                                 print("   ⚠️ No visible matches found. Defaulting to first match.")
                                 locator = locator.first
                     except Exception as e:
                         # Some dynamic locators might fail count check, ignore
                         pass
                     # ---------------------------------------------------------

                result = {"locator": loc_str, "new_page": None, "success": True}

                if decision['action'] == 'click':
                    # Listen for new page
                    try:
                        async with page.context.expect_page(timeout=2000) as new_page_info:
                            try:
                                await locator.click(timeout=4000)
                            except Exception as e:
                                if "strict mode" in str(e):
                                    print("   ⚠️ Strict mode violation. Clicking first match.")
                                    await locator.first.click(timeout=4000)
                                else:
                                    raise e
                        
                        # MULTI-TAB STRATEGY
                        new_page = await new_page_info.value
                        await new_page.wait_for_load_state()
                        # Simple domain check: valid if it contains part of original target
                        # Extract domain from target_url
                        from urllib.parse import urlparse
                        base_domain = urlparse(self.config["target_url"]).netloc
                        new_domain = urlparse(new_page.url).netloc
                        
                        if base_domain not in new_domain and "localhost" not in new_domain:
                            print(f"🛑 External Tab detected ({new_page.url}). Closing to stay on target.")
                            await new_page.close()
                            result["new_page"] = None
                        else:
                            result["new_page"] = new_page

                    except Exception as e:
                        # Normal click if no new page (or expect_page timed out)
                        try:
                            await locator.scroll_into_view_if_needed(timeout=2000)
                            try:
                                await locator.click(timeout=4000)
                            except Exception as click_e:
                                if "strict mode" in str(click_e):
                                    await locator.first.click(timeout=4000)
                                else:
                                    raise click_e
                        except Exception as inner_e:
                            print(f"   ⚠️ Normal click failed ({inner_e}). Trying force click...")
                            try:
                                await locator.first.click(timeout=3000, force=True)
                            except Exception as force_e:
                                # NUCLEAR OPTION: JS Click
                                print(f"   ☢️ Force click failed ({force_e}). Trying JS Click...")
                                await locator.first.evaluate("el => el.click()")
                                await asyncio.sleep(1) # Wait for JS execution

                elif decision['action'] == 'fill':
                    # Prevent filling non-inputs
                    if target_el and target_el.get('role') in ['link', 'button', 'img']:
                         print(f"⚠️ Skipping fill on non-input role: {target_el.get('role')}")
                         return {"locator": None, "new_page": None}

                    val = str(decision.get('value_to_fill', ''))
                    # Smart interaction for fields
                    is_password = "password" in loc_str.lower() or "pass" in loc_str.lower()
                    
                    
                    # 1. PASSWORD CHECK: If we just filled this password on this page, SKIP it.
                    # This prevents loops because password fields often read as empty/masked.
                    if is_password:
                        # Use self.trace, not self.history (which doesn't exist)
                        history = [h for h in self.trace if h.get('url') == page.url]
                        # Look at last 5 actions on this page
                        recent_fills = [h for h in history[-5:] if h['action'] == 'fill' and h.get('locator_used') == loc_str]
                        if recent_fills:
                             print(f"⏩ Skipping cached password fill: {loc_str}")
                             # Fake success to move to next thought
                             return {"locator": loc_str, "new_page": None}

                    try:
                        await locator.scroll_into_view_if_needed(timeout=2000)
                        await locator.click(timeout=2000) # Focus
                        if is_password:
                            await locator.fill("") # Clear
                            await locator.press_sequentially(val, delay=100) # Simulated typing
                        else:
                            await locator.fill(val)
                        
                        # Trigger validation/blur
                        await page.keyboard.press("Tab")
                        await asyncio.sleep(0.5) 
                    except Exception as e:
                        print(f"   ⚠️ Smart fill failed ({e}). Fallback to standard fill.")
                        try:
                            await locator.fill(val)
                        except Exception as fill_e:
                            if "strict mode" in str(fill_e):
                                await locator.first.fill(val)
                            else:
                                print(f"   ❌ Standard fill failed: {fill_e}")
                

                
                return result
                    
            except Exception as e:
                print(f"⚠️ Action Failed: {e}")
                return {"locator": loc_str if 'loc_str' in locals() else None, "new_page": None, "success": False}
                
        return {"locator": None, "new_page": None}
                # Fallback: Try visualization click?
                
    async def _save_trace(self):
        output = {
            "workflow": self.workflow,
            "domain_info": self.domain_knowledge,
            "trace": self.trace,
            "metadata": {
                "cost": self.total_cost
            }
        }
        trace_path = self.config.get("paths", {}).get("trace", "explorer_trace.json")
        # Ensure dir exists
        trace_dir = os.path.dirname(trace_path)
        if trace_dir and not os.path.exists(trace_dir):
            os.makedirs(trace_dir, exist_ok=True)
            
        with open(trace_path, "w") as f:
            json.dump(output, f, indent=2)
        print(f"💾 Trace saved to {trace_path}")

    def _save_test_data(self):
        """Saves discovered test data to a local file in projects folder."""
        trace_path = self.config.get("paths", {}).get("trace", "")
        if not trace_path:
            return

        project_root = os.path.dirname(os.path.dirname(trace_path))
        if not project_root:
            project_root = "."
            
        # Prefer config/test-data.json if config dir exists (Standard Structure)
        config_dir = os.path.join(project_root, "config")
        if os.path.exists(config_dir):
             data_path = os.path.join(config_dir, "test-data.json")
        else:
             data_path = os.path.join(project_root, "test_data.json")

        try:
            with open(data_path, "w") as f:
                json.dump(self.test_data, f, indent=2)
            print(f"💾 Test data persisted to {data_path}")
        except Exception as e:
            print(f"⚠️ Failed to save test data: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Config file")
    args = parser.parse_args()
    
    agent = ExplorerAgent(args.config)
    asyncio.run(agent.explore())
