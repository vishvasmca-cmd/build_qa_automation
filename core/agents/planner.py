import sys
import os
import json
import logging
import asyncio
import argparse
from termcolor import colored
from typing import Dict, Any, List

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


from core.lib.llm_utils import SafeLLM, try_parse_json
from core.lib.domain_expert import DomainExpert

class PlannerAgent:
    """
    Decomposes a high-level goal into test scenarios and keywords in workflow.json.
    """
    def __init__(self, project_dir: str):
        self.project_dir = os.path.abspath(project_dir)
        self.workflow_path = os.path.join(self.project_dir, "workflow.json")
        self.sitemap_path = os.path.join(self.project_dir, "sitemap.json")
        
        # Load existing workflow if it exists
        self.workflow = self._load_workflow()
        
        self.llm = SafeLLM(
            model=None,
            temperature=0.0,
            model_kwargs={
                "response_mime_type": "application/json",
                #   FIX: Limit output tokens to prevent parsing failures
                # Normal: 2000 tokens = ~1-2 scenarios
                # Deep mode will override to 4000 in plan_goal()
                "max_output_tokens": 2000
            }
        )

    def _load_workflow(self) -> Dict:
        if os.path.exists(self.workflow_path):
            with open(self.workflow_path, 'r') as f:
                return json.load(f)
        return {
            "project": os.path.basename(self.project_dir),
            "goal": "",
            "base_url": "",
            "scenarios": []
        }
    
    def _parse_sitemap(self, sitemap: List[Dict]) -> Dict:
        """Parse sitemap into structured knowledge."""
        knowledge = {"pages_by_type": {}, "user_flows": [], "form_endpoints": []}
        
        # Filter out unknown pages
        useful_pages = [page for page in sitemap if page.get("page_type") != "unknown"]
        
        for page in useful_pages:
            page_type = page.get("page_type", "other")
            if page_type not in knowledge["pages_by_type"]:
                knowledge["pages_by_type"][page_type] = []
            knowledge["pages_by_type"][page_type].append(page)
        if "product_detail" in knowledge["pages_by_type"]:
            knowledge["user_flows"].append({"name": "E-commerce Shopping Flow", "type": "ecommerce"})
        for page in useful_pages:
            if page.get("forms"):
                knowledge["form_endpoints"].append(page)
        return knowledge
    
    def _generate_test_data(self, field: Dict) -> str:
        """Generate test data for field types."""
        field_type = field.get("type", "text").lower()
        field_name = (field.get("name") or "").lower()
        if field_type == "email" or "email" in field_name:
            return "{random_email}"
        elif "phone" in field_name:
            return "{random_phone}"
        elif "name" in field_name:
            return "{random_name}"
        else:
            return f"Test {field.get('name', 'value')}"
    
    def _create_fallback_workflow(self, goal: str, base_url: str) -> dict:
        """Create a simple fallback workflow when LLM fails to parse."""
        print(colored(f"     Creating simple fallback scenario from goal: {goal[:50]}...", "yellow"))
        
        # Parse goal for basic keywords
        goal_lower = goal.lower()
        steps = [
            {
                "id": "step_1",
                "keyword": "navigate",
                "args": {"url": base_url}
            }
        ]
        
        # Add basic steps based on goal keywords
        step_id = 2
        if "search" in goal_lower:
            steps.append({
                "id": f"step_{step_id}",
                "keyword": "click",
                "description": "Search"
            })
            step_id += 1
            steps.append({
                "id": f"step_{step_id}",
                "keyword": "fill",
                "description": "Search input",
                "args": {"value": "test"}
            })
            step_id += 1
        
        if "click" in goal_lower or "navigate to" in goal_lower:
            # Extract what to click after "click" or "navigate to"
            import re
            match = re.search(r"(?:click|navigate to)\s+'([^']+)'", goal_lower)
            if match:
                target = match.group(1)
                steps.append({
                    "id": f"step_{step_id}",
                    "keyword": "click",
                    "description": target
                })
                step_id += 1
        
        # Add assertion at the end
        steps.append({
            "id": f"step_{step_id}",
            "keyword": "assert_url",
            "args": {"expected_url": base_url}
        })
        
        return {
            "scenarios": [{
                "id": "fallback_scenario",
                "name": f"Fallback: {goal[:40]}",
                "description": f"Auto-generated fallback scenario for: {goal}",
                "steps": steps
            }]
        }

    async def plan_goal(self, goal: str, base_url: str = None, deep_mode: bool = False):
        print(colored(f"\n[PLAN] PLANNER: Planning goal -> '{goal}' (Deep Mode: {deep_mode})", "cyan", attrs=["bold"]))
        
        # Fallback to a default goal if None provided (e.g. from CI or malformed config)
        goal = goal or "Explore the website and identify key user flows and interactive elements."
        
        url = base_url or self.workflow.get("base_url") or "https://www.google.com"
        landmarks = self.workflow.get("landmarks", [])
        landmarks_text = json.dumps(landmarks, indent=2) if landmarks else "None discovered yet."
        
        # Load Sitemap if available
        sitemap_text = "No sitemap available."
        knowledge = {"pages_by_type": {}, "user_flows": [], "form_endpoints": []}
        
        if os.path.exists(self.sitemap_path):
            with open(self.sitemap_path, 'r', encoding='utf-8') as f:
                sitemap = json.load(f)
                sitemap_text = json.dumps(sitemap, indent=2)
                # [OK] Parse structured sitemap
                knowledge = self._parse_sitemap(sitemap)
            print(colored(f"[PLAN] Loaded Sitemap with {len(sitemap)} pages.", "cyan"))
            print(colored(f"[PLAN] Page types: {list(knowledge['pages_by_type'].keys())}", "cyan"))
            print(colored(f"[PLAN] Flows: {len(knowledge['user_flows'])}, Forms: {len(knowledge['form_endpoints'])}", "cyan"))

        # Detect Domain and get Persona
        domain = DomainExpert.detect_domain(url, landmarks_text, goal)
        persona = DomainExpert.get_persona_prompt(domain)
        print(colored(f"[EXPERT] Detected Domain: {domain.upper()}. Persona: {persona.split('.')[0]}", "yellow"))

        # Deep Mode: Request comprehensive suite
        task_desc = f'Create a test scenario for the goal: "{goal}"'
        if deep_mode:
            task_desc = f"""
            Act as a Lead SDET. 
            Analyze the domain ({domain}) and generate a COMPREHENSIVE REGRESSION SUITE (3-5 distinct scenarios).
            Cover key flows such as:
            - Authentication (if applicable)
            - Main User Flow (e.g. Search -> Add to Cart -> Checkout)
            - Secondary Flows (e.g. Contact Us, Profile update)
            - Edge cases if relevant.
            
            The user goal provided is: "{goal}" (Ensure this is covered).
            """

        prompt = f"""
        {persona}
        
        **MISSION:**
        {task_desc}
        
        **TARGET APPLICATION:**
        Base URL: {url}
        
        **DISCOVERED LANDMARKS (Use these real names/IDs if possible):**
        {landmarks_text}
        
        **VALIDATED SITE MAP (Use these EXACT URLs for navigation steps):**
        {sitemap_text}
        
        **YOUR TASK:**
        1. **CRITICAL FIRST STEP:** The very FIRST step MUST be `navigate` to: {url}
        2. Break this goal into sequential automation steps using valid Keywords.
        3. **Automatic Validation**: Add `assert_visible` or `assert_url` steps after major actions (like clicking a link or filling a search) to verify the process.
        4. Prefer items from the DISCOVERED LANDMARKS if they match the intent.
        
        **VALID KEYWORDS:**
        - navigate(url)
        - click(description, index=0)  # Use index for ordinal items (0=first, 1=second)
        - fill(value, description, index=0)
        - type(value, description)
        - hover(description)
        - select(value, description)
        - check(description)
        - uncheck(description)
        - press(key, description)
        - scroll_to(description)
        - wait(seconds)
        - wait_for_element(description)
        - assert_visible(description)
        - assert_text(expected_text, description)
        - assert_url(expected_url)
        - screenshot(name)
        
        **DYNAMIC DATA:**
        Use placeholders like {{random_email}}, {{random_name}}, {{random_password}} for form data.
        
        **FLOW AWARENESS RULES:**
        1. **WAIT_FOR_ELEMENT Usage - Use ONLY for:**
           - Dynamic content that loads after initial page render (AJAX, lazy loading)
           - Elements that appear after animations or transitions
           - DO NOT use for elements that should be present on initial page load
           - DO NOT wait for elements from a different page than the current one
        
        2. **E-Commerce Flow Understanding:**
           - Product List Page -> has product tiles/cards
           - Product Detail Page -> has single product details, 'Add to Cart' button
           - Cart Page -> has cart items, quantities, 'Proceed to Checkout' button
           - Checkout Page -> has payment/shipping forms, 'Place Order' button
           - DO NOT expect product browsing elements on checkout/cart pages
        
        3. **Context Switching:**
           - After 'Checkout' or 'Place Order', you are done with that flow
           - To browse products again, navigate back to home or products page first
        
        **CRITICAL RULES:**
        - Step 1 MUST be: navigate("{url}")
        - DO NOT use placeholder URLs like "example.com", "banking application", or "application homepage"
        - ONLY use the actual base URL: {url}
        
        **DESCRIPTION QUALITY RULES:**
        - [OK] GOOD: Use user-facing text like "Cart", "Login", "Search", "Add to Cart"
        - [FAIL] BAD: Do NOT use technical IDs like "shopping_cart_container", "btn_login", "search_input"
        - [OK] GOOD: "Continue", "Checkout", "Submit"
        - [FAIL] BAD: "continue_button", "checkout-btn", "submit_form"
        - The "description" field should be what a user SEES, not what developers NAME elements
        
        **RESPONSE FORMAT (JSON):**
        Use "args" (not "arguments") for parameters.
        {{
          "scenarios": [
            {{
              "id": "TC001",
              "name": "Scenario Name",
              "description": "...",
              "steps": [ ... ]
            }}
          ]
        }}
        """
        
        try:
            response = await self.llm.ainvoke(prompt)
            parsed = try_parse_json(response)
            
            if not parsed:
                print(colored("[FAIL] Failed to parse valid JSON from LLM.", "red"))
                print(colored(f"   Response length: {len(response)} characters", "yellow"))
                print(colored(f"   Sitemap pages: {len(sitemap) if os.path.exists(self.sitemap_path) else 0}", "yellow"))
                
                #   FIX: Retry with reduced context (only 10 pages)
                if os.path.exists(self.sitemap_path) and len(sitemap) > 10:
                    print(colored("     Retry #1: Reducing sitemap to 10 most relevant pages...", "yellow"))
                    
                    # Keep only most relevant pages (homepage, login, forms)
                    reduced_sitemap = []
                    for page in sitemap[:10]:  # Take first 10 pages only
                        reduced_sitemap.append(page)
                    
                    reduced_sitemap_text = json.dumps(reduced_sitemap, indent=2)
                    
                    # Rebuild prompt with reduced context
                    reduced_prompt = prompt.replace(sitemap_text, reduced_sitemap_text)
                    
                    print(colored(f"   Retry with {len(reduced_sitemap)} pages instead of {len(sitemap)}", "yellow"))
                    
                    response = await self.llm.ainvoke(reduced_prompt)
                    parsed = try_parse_json(response)
                
                #   FIX: Create fallback workflow if still failing
                if not parsed:
                    print(colored("   [WARN]  Retry failed. Creating fallback workflow from goal...", "yellow"))
                    parsed = self._create_fallback_workflow(goal, url)
                    
                if not parsed:
                    print(colored("   [FAIL] Fallback creation failed. Cannot proceed.", "red"))
                    return False

            # Normalize to list of scenarios
            scenarios_list = []
            if isinstance(parsed, dict):
                if "scenarios" in parsed:
                    scenarios_list = parsed["scenarios"]
                else:
                    # Single object scenario
                    scenarios_list = [parsed]
            elif isinstance(parsed, list):
                scenarios_list = parsed
            
            if not scenarios_list:
                print(colored("[FAIL] No scenarios found in response.", "red"))
                return False
            
            # Update workflow
            self.workflow["base_url"] = url
            self.workflow["goal"] = goal
            
            count = 0
            for scenario in scenarios_list:
                # Basic validation
                if "steps" not in scenario:
                    continue
                
                # Ensure ID present
                if "id" not in scenario:
                    scenario["id"] = f"TC_GEN_{count}"
                
                # VALIDATION: Ensure first step navigates to base_url
                if scenario.get("steps") and len(scenario["steps"]) > 0:
                    first_step = scenario["steps"][0]
                    if first_step.get("keyword") == "navigate":
                        first_url = first_step.get("args", {}).get("url", "")
                        # Fix hallucinated URLs
                        invalid_urls = ["example.com", "banking application", "application homepage", 
                                        "http://example.com", "https://example.com"]
                        if any(invalid in first_url.lower() for invalid in invalid_urls) or not first_url.startswith("http"):
                            print(colored(f"      Fixing invalid first URL: '{first_url}' -> '{url}'", "yellow"))
                            first_step["args"]["url"] = url
                    else:
                        # Inject navigate step if missing
                        print(colored(f"      Injecting missing navigate step to: {url}", "yellow"))
                        scenario["steps"].insert(0, {
                            "id": "step_0",
                            "keyword": "navigate",
                            "args": {"url": url}
                        })
                    
                # Check if scenario ID exists, update or append
                exists = False
                for i, s in enumerate(self.workflow["scenarios"]):
                    if s.get("id") == scenario["id"]:
                        self.workflow["scenarios"][i] = scenario
                        exists = True
                        break
                
                if not exists:
                    self.workflow["scenarios"].append(scenario)
                count += 1
            
            # Save workflow.json
            with open(self.workflow_path, 'w') as f:
                json.dump(self.workflow, f, indent=2)
                
            print(colored(f"[OK] Planner generated {count} scenarios. Workflow updated.", "green"))
            return True
            
        except Exception as e:
            print(colored(f"[FAIL] Planner Error: {e}", "red"))
            import traceback
            traceback.print_exc()
            
            #   FIX: Create fallback workflow even on exception
            print(colored("     Creating fallback workflow due to exception...", "yellow"))
            fallback = self._create_fallback_workflow(goal, url)
            if fallback:
                parsed = fallback
                # Proceed with fallback workflow
                scenarios_list = []
                if isinstance(parsed, dict):
                    if "scenarios" in parsed:
                        scenarios_list = parsed["scenarios"]
                    else:
                        scenarios_list = [parsed]
                elif isinstance(parsed, list):
                    scenarios_list = parsed
                
                if scenarios_list:
                    self.workflow["base_url"] = url
                    self.workflow["goal"] = goal
                    self.workflow["scenarios"] = scenarios_list
                    
                    with open(self.workflow_path, 'w') as f:
                        json.dump(self.workflow, f, indent=2)
                    
                    print(colored(f"[OK] Created fallback workflow with {len(scenarios_list)} scenario(s).", "green"))
                    return True
            
            return False

async def main():
    parser = argparse.ArgumentParser(description="Planner Agent")
    parser.add_argument("--project", required=True, help="Project directory")
    parser.add_argument("--goal", help="Goal to plan")
    parser.add_argument("--url", help="Base URL for the project")
    parser.add_argument("--deep", action="store_true", help="Enable deep comprehensive planning")
    
    args = parser.parse_args()
    
    agent = PlannerAgent(args.project)
    await agent.plan_goal(args.goal, base_url=args.url, deep_mode=args.deep)

if __name__ == "__main__":
    asyncio.run(main())
