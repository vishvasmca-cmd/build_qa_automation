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
            model="gemini-2.0-flash",
            temperature=0.0,
            model_kwargs={"response_mime_type": "application/json"}
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

    async def plan_goal(self, goal: str, base_url: str = None, deep_mode: bool = False):
        print(colored(f"\n[PLAN] PLANNER: Planning goal -> '{goal}' (Deep Mode: {deep_mode})", "cyan", attrs=["bold"]))
        url = base_url or self.workflow.get("base_url") or "https://www.google.com"
        landmarks = self.workflow.get("landmarks", [])
        landmarks_text = json.dumps(landmarks, indent=2) if landmarks else "None discovered yet."
        
        # Load Sitemap if available
        sitemap_text = "No sitemap available."
        if os.path.exists(self.sitemap_path):
            with open(self.sitemap_path, 'r', encoding='utf-8') as f:
                sitemap = json.load(f)
                sitemap_text = json.dumps(sitemap, indent=2)
            print(colored(f"🗺️ [PLAN] Loaded Sitemap with {len(sitemap)} pages.", "cyan"))

        # Detect Domain and get Persona
        domain = DomainExpert.detect_domain(url, landmarks_text, goal)
        persona = DomainExpert.get_persona_prompt(domain)
        print(colored(f"🎭 [EXPERT] Detected Domain: {domain.upper()}. Persona: {persona.split('.')[0]}", "yellow"))

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
        
        **DISCOVERED LANDMARKS (Use these real names/IDs if possible):**
        {landmarks_text}
        
        **VALIDATED SITE MAP (Use these EXACT URLs for navigation steps):**
        {sitemap_text}
        
        **YOUR TASK:**
        1. Break this goal into sequential automation steps using valid Keywords.
        2. **Automatic Validation**: Add `assert_visible` or `assert_url` steps after major actions (like clicking a link or filling a search) to verify the process.
        3. Prefer items from the DISCOVERED LANDMARKS if they match the intent.
        
        **VALID KEYWORDS:**
        - navigate(url)
        - click(description)
        - fill(value, description)
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
                 print(colored("❌ Failed to parse valid JSON from LLM.", "red"))
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
                print(colored("❌ No scenarios found in response.", "red"))
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
                
            print(colored(f"✅ Planner generated {count} scenarios. Workflow updated.", "green"))
            return True
            
        except Exception as e:
            print(colored(f"❌ Planner Error: {e}", "red"))
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
