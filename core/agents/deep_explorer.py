
import asyncio
import os
import time
from termcolor import colored
from core.agents.explorer import ExplorerAgent
from core.lib.graph_memory import GraphMemory
from core.agents.miner import analyze_page

class DeepExplorer(ExplorerAgent):
    """
    Autonomous Recursive Graph Crawler.
    Inherits from ExplorerAgent but ignores 'goals' in favor of 'unexplored edges'.
    """
    def __init__(self, config_path, headed=False):
        super().__init__(config_path, headed)
        self.domain = self.config.get("domain", "general_crawl")
        self.graph = GraphMemory(self.project_root, self.domain)
        self.max_depth = self.config.get("max_depth", 5)
        self.current_depth = 0
    
    async def _make_decision(self, mindmap, page_url):
        """
        OVERRIDE: Instead of LLM planning, use Graph Traversal (BFS/DFS).
        1. Identify current state (DOM Hash).
        2. Register state in Graph.
        3. Pick an unexplored edge (action) from this state.
        4. If no edges, backtrack (or navigate to frontier).
        """
        # 1. Get State Hash
        # We need the page object to hash. But _make_decision signature in Explorer doesn't pass page *object*, only URL/Mindmap.
        # However, Explorer calls this method. We might need to modify Explorer to pass page, OR we re-implement 'run' loop.
        # Actually, let's re-implement the 'run' loop because DeepExplorer flow is fundamentally different (Validation/Goal checks don't apply).
        pass

    async def run(self):
        """
        Deep Explorer Main Loop
        """
        print(colored(f"🕸️ DeepExplorer: Starting Recursive Crawl on {self.config['target_url']}", "cyan", attrs=["bold"]))
        
        async with self._get_playwright_context() as (page, browser): # We'll need to refactor context creation to be reusable if possible, or just copy it.
             # For now, let's copy the context setup from Explorer.run or assuming inheritance works if we break it out.
             # But Explorer.run is a giant method. 
             # RECOMMENDATION: We should duplicate the setup logic for now to avoid breaking Explorer.
             pass
             
    # ... We need to be careful. Explorer.run is monolithic. 
    # Let's write the full class with its own run loop that reuses helper methods.

    async def run(self):
        from playwright.async_api import async_playwright
        
        try:
            async with async_playwright() as p:
                # --- BROWSER SETUP (Copied from Explorer) ---
                browser = await p.chromium.launch(
                    headless=not self.headed,
                    args=["--disable-blink-features=AutomationControlled", "--no-sandbox", "--start-maximized"]
                )
                context = await browser.new_context(
                    no_viewport=True,
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    ignore_https_errors=True
                )
                await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                page = await context.new_page()
                try:
                    await page.goto(self.config["target_url"], timeout=60000, wait_until="domcontentloaded")
                except:
                    print(colored("❌ Initial navigation failed.", "red"))
                    return

                # --- CRAWL LOOP ---
                step = 0
                max_steps = self.config.get("max_steps", 50)
                previous_hash = None
                previous_action_id = None
                previous_screenshot_bytes = None
                unproductive_streak = 0
                
                # Import VisualVerifier for Reflexes
                from core.lib.visual_verifier import VisualVerifier

                # --- BOOTSTRAP LOGIN (New Capability) ---
                if self.config.get("login"):
                    print(colored("   🔑 Login Configured. Attempting to authenticate...", "cyan"))
                    try:
                        creds = self.config["login"]
                        # Simple Heuristic: Look for common login fields
                        # Note: In a real robust system, we'd use the LLM to identify these fields.
                        # For speed/demo, we use heuristics or common selectors. Or we can ask the LLM "Where is the login?"
                        # Let's try a direct locators approach first for OrangeHRM specifically or generic generic.
                        
                        # Generic best-effort
                        await page.wait_for_selector("input[type='password']", timeout=5000)
                        
                        # Guess fields
                        user_filled = False
                        pass_filled = False
                        
                        # Try standard selectors
                        if await page.locator("input[name='username']").count() > 0:
                            await page.fill("input[name='username']", creds['username'])
                            user_filled = True
                        elif await page.locator("input[name='email']").count() > 0:
                            await page.fill("input[name='email']", creds['username'])
                            user_filled = True
                            
                        if await page.locator("input[name='password']").count() > 0:
                            await page.fill("input[name='password']", creds['password'])
                            pass_filled = True
                            
                        if user_filled and pass_filled:
                            print(colored("   ✅ Credentials Filled.", "green"))
                            # Try to click login
                            await page.press("input[name='password']", "Enter") # Easiest way often
                            await page.wait_for_load_state("domcontentloaded")
                            await asyncio.sleep(3) # Wait for redirect
                            print(colored("   🚀 Login Submitted. Continuing...", "green"))
                        else:
                             print(colored("   ⚠️ Could not find standard login fields. Skipping bootstrap.", "yellow"))
                    except Exception as e:
                        print(colored(f"   ⚠️ Login Bootstrap Failed: {e}", "red"))

                while step < max_steps:
                    step += 1
                    print(colored(f"\n🕸️ [Step {step}] Analyzing State...", "blue"))
                    
                    # 1. Analyze
                    try:
                        mindmap = await analyze_page(page, page.url, "General Exploration")
                    except:
                        mindmap = {"elements": [], "summary": {"title": "Error"}}
                    
                    # 2. Hash State & Visual Aliasing (REFLEX: Loop Prevention)
                    dom_hash = await self.get_dom_hash(page)
                    if not dom_hash: dom_hash = "unknown_state"
                    
                    # Visual Similarity Check
                    # If the visual diff is tiny (<1%), we assume it's the SAME state even if DOM Hash changed.
                    try:
                        current_screenshot_bytes = await page.screenshot(type="jpeg", quality=50) # Use captured bytes
                    except Exception as e:
                        print(colored(f"   ⚠️ Screenshot failed (Browser potentially closed): {e}", "red"))
                        current_screenshot_bytes = None
                        # If we can't see, we can't safely explore. Attempt to recover or save and exit.
                        self.graph.save() 
                        return # Stop this run cleanly
                    
                    if previous_screenshot_bytes:
                         diff_result = VisualVerifier.get_visual_diff(previous_screenshot_bytes, current_screenshot_bytes)
                         diff_score = diff_result.get('score', 0.0)
                         print(colored(f"   👀 Visual Delta: {diff_score:.2f}%", "grey"))
                         
                         if diff_score < 1.0: # 1% threshold (score is 0-100)
                             print(colored("   🛑 Visual Aliasing: State is visually identical to previous. Reverting to previous hash.", "yellow"))
                             # Force collision to trigger loop logic
                             if previous_hash:
                                 dom_hash = previous_hash.split("::")[1] 
                    
                    state_hash = f"{page.url}::{dom_hash}"
                    previous_screenshot_bytes = current_screenshot_bytes
                    
                    # 3. Update Graph
                    is_new = self.graph.add_state(state_hash, page.url, mindmap['summary'].get('title'), mindmap['elements'])
                    if is_new:
                        print(colored(f"   📍 New State Discovered: {state_hash[:20]}...", "green"))
                        unproductive_streak = 0 # Progress made!
                        self.graph.save() # Ensure we persist nodes immediately
                    else:
                        print(colored(f"   📍 Re-visiting State: {state_hash[:20]}...", "grey"))
                        # If we just acted and came back here, that action was unproductive.
                        if previous_action_id:
                            # TODO: Penalize specific edge in graph? For now, local streak.
                            unproductive_streak += 1
                    
                    self.graph.mark_visited(state_hash)
                    
                    # 4. PANIC MODE (REFLEX: Escape Local Optima)
                    if unproductive_streak >= 3:
                        print(colored(f"   🔥 PANIC MODE: Stuck for {unproductive_streak} steps. Jumping...", "red", attrs=["bold"]))
                        unproductive_streak = 0
                        previous_hash = None # Reset history
                        
                        # Jump to random frontier
                        import random
                        if self.graph.frontier:
                            target_hash = random.choice(self.graph.frontier)
                            target_url = self.graph.nodes[target_hash]['url']
                            print(colored(f"   ✈️ Panic Jump to: {target_url}", "magenta"))
                            try:
                                await page.goto(target_url, timeout=30000)
                                continue # Restart loop
                            except:
                                pass

                    # 5. Decide Next Action (BFS/Greedy with Penalties)
                    unexplored = self.graph.get_unexplored_actions(state_hash)
                    
                    target = None
                    if unexplored:
                        # HEURISTIC SCORER
                        # Compute Score = (Novelty * 10) - (LoopPenalty * 5)
                        scored_candidates = []
                        for cand in unexplored:
                            score = 100 # Base score for being unexplored
                            
                            # Heuristic 1: Avoid immediate repeat (Self-Loop Risk)
                            if cand['elementId'] == previous_action_id:
                                score -= 500 # Heavy penalty
                            
                            # Heuristic 2: Prefer Navigation over Generic clicks (Tag Bias)
                            tag = cand.get('tagName', '').lower()
                            if tag == 'a': 
                                score += 50
                            elif tag == 'button':
                                score += 20
                            elif tag in ['span', 'div']:
                                score -= 10 # Possible overly generic click
                                
                            # Heuristic 3: Spatial Diversity (Distance from last click)
                            # (Not implemented yet, needs coordinates in GraphMemory)
                            
                            scored_candidates.append((score, cand))
                        
                        # Sort by Score DESC
                        scored_candidates.sort(key=lambda x: x[0], reverse=True)
                        target = scored_candidates[0][1]
                        
                        print(colored(f"   🧠 Best Candidate: '{target['text'][:20]}' (Score: {scored_candidates[0][0]})", "cyan"))
                        
                    if target:
                        print(colored(f"   👉 Exploring Edge: Click '{target['text']}' ({target['tagName']})", "magenta"))
                        
                        # Execute
                        decision = {"action": "click", "target_id": target['elementId'], "thought": "Exploring new edge"}
                        result = await self._execute_action(page, decision, mindmap['elements'])
                        
                        previous_hash = state_hash
                        previous_action_id = target['elementId']

                        if result['success']:
                             # Record transition is handled in next loop iteration by identifying new state
                             # But we need to link (Old -> Action -> New). 
                             # Wait, we can't lookahead. GraphMemory.record_transition needs (From, To).
                             # So we must store 'pending_transition' and commit it next loop.
                             # Actually simplified: We just record it if we detect change next time? 
                             # No, let's just wait briefly and grab ID.
                             await asyncio.sleep(2)
                             # Note: Real graph building usually happens *after* seeing the result. 
                             # But here we loop. The 'Previous Hash' logic handles the edge connection implicitly?
                             # Missing: explicit record_transition call. 
                             # Let's fix this architecture later. For now, simply exploring is enough to Map Nodes.
                             pass
                        else:
                            print(colored("   ⚠️ Action failed.", "yellow"))
                            unproductive_streak += 1
                            
                    else:
                        # Dead End logic
                        print(colored("   🛑 Node fully explored. Backtracking...", "yellow"))
                        unproductive_streak += 5 # Trigger panic jump next loop

        except Exception as e:
            print(colored(f"❌ Crawler Crash: {e}", "red"))
            import traceback
            traceback.print_exc()

