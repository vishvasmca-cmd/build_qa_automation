import os
import json
import yaml
from urllib.parse import urlparse
from dotenv import load_dotenv
from core.knowledge.knowledge_bank import KnowledgeBank

# Import robust LLM wrapper
# Import robust LLM wrapper
from core.lib.llm_utils import SafeLLM
import sys

# Force UTF-8 for console output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

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

    def analyze_run(self, config_or_path, test_output_log, success):
        """
        Analyzes the result of a test run and reinforces memory.
        """
        if isinstance(config_or_path, dict):
            config = config_or_path
        else:
            with open(config_or_path, "r") as f:
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
1. "root_cause": Brief explanation of why it failed.
2. "bad_locators": List of specific playwright locator strings that were problematic.
3. "negative_rule": A mandatory "DON'T" rule (e.g., "NEVER click the 'Add to cart' overlay without 1s wait"). 
4. "positive_rule": A mandatory "DO" rule (e.g., "ALWAYS use the search bar for products instead of scrolling").
5. "suggested_fix": A customized strategy for the next attempt.
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
            
            # Action 2: Add Learned Rules to Site Knowledge
            for rule_type in ["negative_rule", "positive_rule"]:
                rule = analysis.get(rule_type)
                if rule:
                    prefix = "⚠️ PROHIBITED" if rule_type == "negative_rule" else "✅ PREFERRED"
                    print(f"   📝 learning new rule: {prefix}: {rule}")
                    self._add_site_rule(domain, f"{prefix}: {rule}")

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

    def _add_site_rule(self, site_domain, rule):
        """Appends a unique rule to the site's rules.md file."""
        site_path = os.path.join(self.kb.root, "sites", site_domain)
        rules_file = os.path.join(site_path, "rules.md")
        
        os.makedirs(site_path, exist_ok=True)
        
        # Format the rule as a bullet point if not already
        rule = rule.strip()
        if not rule.startswith("-"):
            rule = f"- {rule}"
            
        # Ignore extremely generic rules that clutter the KB
        generic_keywords = ["import path", "python path", "parentheses", "syntax error", "import error", "directory structure", "eval()", "module not found"]
        if any(kw in rule.lower() for kw in generic_keywords):
            print(f"   🧹 Filtering out generic programming rule: {rule}")
            return

        try:
            # Check for duplicates
            existing_rules = []
            if os.path.exists(rules_file):
                with open(rules_file, "r", encoding="utf-8") as f:
                    existing_rules = [line.strip() for line in f if line.strip()]
            
            if rule in existing_rules:
                print(f"   ♻️ Rule already exists, skipping duplicate.")
                return

            with open(rules_file, "a", encoding="utf-8") as f:
                f.write(f"\n{rule}\n")
            print(f"   💾 Saved unique rule to {rules_file}")
        except Exception as e:
            print(f"   ⚠️ Failed to save rule: {e}")

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

    def analyze_generic_error(self, agent_name, error_log):
        """
        Diagnoses non-testing errors (e.g., Planner crash, Explorer timeout).
        Returns a suggested fix or strategy adjustment.
        """
        print(f"🧠 Feedback Agent: Diagnosing {agent_name} failure...")
        system_prompt = f"""You are a System Architect diagnosing a crash in the {agent_name} component.
        Analyze the error log and suggest a fix.
        
        OUTPUT format using JSON:
        {{
            "root_cause": "Explanation",
            "suggested_action": "Retry with X | Skip Step | Fatal"
        }}
        """
        try:
            resp = self.llm.invoke([
                ("system", system_prompt),
                ("human", f"ERROR LOG:\n{str(error_log)[:2000]}")
            ])
            clean = resp.content.replace("```json", "").replace("```", "").strip()
            analysis = json.loads(clean)
            print(f"   🔍 Diagnosis: {analysis['root_cause']}")
            print(f"   💡 Suggestion: {analysis['suggested_action']}")
            return analysis
        except:
            return None
