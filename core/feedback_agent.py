import os
import json
import yaml
from urllib.parse import urlparse
from dotenv import load_dotenv
from knowledge_bank import KnowledgeBank

# Import robust LLM wrapper
try:
    from .llm_utils import SafeLLM
except (ImportError, ValueError):
    from llm_utils import SafeLLM

class FeedbackAgent:
    """
    Post-Mortem Analysis Agent.
    Reviews test execution logs, diagnoses failures, and updates the Knowledge Bank
    to ensure the NEXT run doesn't make the same mistakes.
    """
    def __init__(self):
        load_dotenv()
        self.llm = SafeLLM(model="gemini-2.0-flash", temperature=0.1)
        self.kb = KnowledgeBank()

    def analyze_run(self, config_path, test_output_log, success):
        """
        Analyzes the result of a test run and reinforces memory.
        """
        with open(config_path, "r") as f:
            config = json.load(f)
            
        project = config["project_name"]
        url = config["target_url"]
        domain = urlparse(url).netloc
        
        print(f"🧠 Feedback Agent: Analyzing run for {project}...")

        if success:
            print(f"   ✅ Run was successful. Reinforcing patterns.")
            # We could optionally ask LLM to identify *why* it was successful, 
            # but for now, we just trust the existing stability score updates.
            return

        # FAILURE ANALYSIS
        print(f"   ❌ Run failed. Diagnosing root cause...")
        
        # specific failure analysis prompt
        system_prompt = """You are a Senior QA Automation Architect.
Your goal is to analyze a FAILED test execution log and extract actionable "Lessons Learned" for the Knowledge Base.

**INPUT**:
- Test Execution Log (Pytest output)
- Target URL

**OUTPUT**:
A JSON object containing:
1. "root_cause": Brief explanation of why it failed (e.g., "Locator not found", "Timeout on Modal", "Logic Error").
2. "bad_locators": List of specific locator strings that failed and should be blacklisted/downgraded.
3. "new_rule": A behavioral rule to add to the domain knowledge (e.g., "Always close modal #advert before clicking login").
4. "suggested_fix": A customized strategy for the next attempt.
"""

        user_msg = f"""
        Target: {url}
        
        FAILURE LOG:
        {test_output_log[-2000:]}  # Last 2000 chars usually contain the traceback
        """

        try:
            resp = self.llm.invoke([
                ("system", system_prompt),
                ("human", user_msg)
            ])
            
            clean = resp.content.replace("```json", "").replace("```", "").strip()
            analysis = json.loads(clean)
            
            print(f"   🔍 Diagnosis: {analysis['root_cause']}")
            
            # Action 1: Update Locator Stability (Explicit Downgrade)
            if analysis.get("bad_locators"):
                print(f"   📉 Downgrading stability for: {analysis['bad_locators']}")
                # We need a method in KnowledgeBank to explicitly kill a locator
                self._penalize_locators(domain, analysis['bad_locators'])
            
            # Action 2: Add Learned Rule to Domain Knowledge
            if analysis.get("new_rule"):
                print(f"   📝 learning new rule: {analysis['new_rule']}")
                self._add_domain_rule(config.get("domain", "general"), analysis['new_rule'])

        except Exception as e:
            print(f"   ⚠️ Feedback analysis failed: {e}")

    def _penalize_locators(self, site_domain, bad_locators):
        """Directly modifies locators.json to mark these as bad."""
        site_path = os.path.join(self.kb.root, "sites", site_domain)
        loc_file = os.path.join(site_path, "locators.json")
        
        if os.path.exists(loc_file):
            try:
                with open(loc_file, "r") as f:
                    data = json.load(f)
                
                changed = False
                for page, locs in data.items():
                    for l in locs:
                        if l['playwright'] in bad_locators:
                            l['stability'] = -10  # Nuked
                            changed = True
                
                if changed:
                    with open(loc_file, "w") as f:
                        json.dump(data, f, indent=2)
            except: pass

    def log_failure(self, context, error_details):
        """
        Logs a failure event to a consolidated failures.json file.
        context: dict with site, stage, etc.
        error_details: string or dict with error info
        """
        import datetime
        
        failures_path = os.path.join(self.kb.root, "failures.json")
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "context": context,
            "error": str(error_details)
        }
        
        current_data = []
        if os.path.exists(failures_path):
            try:
                with open(failures_path, "r") as f:
                    current_data = json.load(f)
                    if not isinstance(current_data, list): current_data = []
            except: 
                current_data = []
        
        current_data.append(entry)
        
        try:
           with open(failures_path, "w") as f:
               json.dump(current_data, f, indent=2)
           print(f"📝 Failure logged to {failures_path}")
        except Exception as e:
           print(f"⚠️ Failed to log failure: {e}")

    def _add_domain_rule(self, domain, rule):
        """Adds a high-level rule to the domain YAML."""
        # Clean domain name
        if isinstance(domain, dict): domain = "general"
        
        domain_file = os.path.join(self.kb.root, "domains", f"{domain}.yaml")
        data = {}
        if os.path.exists(domain_file):
            try:
                with open(domain_file, "r") as f:
                    data = yaml.safe_load(f) or {}
            except: data = {}
            
        rules = data.get("learned_rules", [])
        if rule not in rules:
            rules.append(rule)
            data["learned_rules"] = rules
            
            with open(domain_file, "w") as f:
                yaml.dump(data, f)

