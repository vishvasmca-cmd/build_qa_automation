import os
import json
import yaml
from urllib.parse import urlparse

KB_ROOT = "knowledge"

class KnowledgeBank:
    """
    Advanced Knowledge Bank designed for RAG (Retrieval Augmented Generation).
    Stores patterns in LLM-friendly formats (YAML/Markdown) and locators in JSON.
    """
    def __init__(self):
        self.root = KB_ROOT
        os.makedirs(os.path.join(self.root, "domains"), exist_ok=True)
        os.makedirs(os.path.join(self.root, "sites"), exist_ok=True)
        os.makedirs(os.path.join(self.root, "library"), exist_ok=True)

    def get_rag_context(self, url, goal):
        """
        Retrieves a context string optimized for LLM prompts.
        Combines Site knowledge, Domain patterns, Few-shot examples, AND Predictive History.
        """
        domain_netloc = urlparse(url).netloc
        site_path = os.path.join(self.root, "sites", domain_netloc)
        
        context = []
        
        # 0. Predictive History (Vector-like Search)
        # Find similar past actions for this goal/page
        history_context = self.query_predictive_model(goal, url)
        if history_context:
            context.append(f"### ✨ Predictive Insights (Best Next Steps based on history):\n{history_context}")

        # 1. Site Specific Knowledge
        if os.path.exists(site_path):
            # Load Site Metadata
            meta_file = os.path.join(site_path, "meta.yaml")
            if os.path.exists(meta_file):
                with open(meta_file, "r") as f:
                    context.append(f"### Site Knowledge ({domain_netloc}):\n{f.read()}")
            
            # Load Verified Locators
            loc_file = os.path.join(site_path, "locators.json")
            if os.path.exists(loc_file):
                with open(loc_file, "r") as f:
                    all_locs = json.load(f)
                    # Filter out bad locators (stability <= -2 implies repeated failure)
                    good_locs = {p: [l for l in ls if l.get('stability', 0) > -2] for p, ls in all_locs.items()}
                    context.append(f"### Proven Locators (Self-Corrected):\n{json.dumps(good_locs, indent=2)}")

            # Load Learned Behavioral Rules
            rules_file = os.path.join(site_path, "rules.md")
            if os.path.exists(rules_file):
                with open(rules_file, "r", encoding="utf-8") as f:
                    context.append(f"### Learned Behavioral Rules (CRITICAL - DO NOT IGNORE):\n{f.read()}")

        # 2. Domain Knowledge (Generic patterns for E-commerce, etc)
        # We try to infer domain or use project config
        # For now, let's just grab 'ecommerce' as a default if it exists
        domain_file = os.path.join(self.root, "domains", "ecommerce.yaml")
        if os.path.exists(domain_file):
            with open(domain_file, "r") as f:
                context.append(f"### Common Domain Patterns:\n{f.read()}")

        # 3. Few-Shot Library (Similar flows)
        library_file = os.path.join(self.root, "library", "common_flows.md")
        if os.path.exists(library_file):
            with open(library_file, "r") as f:
                # We could filter for 'goal' similarity here
                context.append(f"### Similar Test Patterns:\n{f.read()}")

        return "\n\n".join(context)

    def query_predictive_model(self, current_goal, current_url):
        """
        Performs a similarity search against the aggregated 'next_action_prediction.jsonl' dataset.
        Mimics a Vector DB RAG retrieval.
        """
        dataset_path = os.path.join(self.root, "datasets", "next_action_prediction.jsonl")
        if not os.path.exists(dataset_path):
            return None
            
        matches = []
        try:
            import difflib
            
            with open(dataset_path, "r") as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        input_goal = entry["input"].get("goal", "")
                        input_url = entry["input"].get("url", "")
                        
                        # Similarity Score: Match Goal AND URL Domain
                        # 1. Domain Match (Boolean)
                        domain_match = urlparse(current_url).netloc in input_url
                        
                        # 2. Goal Similarity (0-1)
                        goal_sim = difflib.SequenceMatcher(None, current_goal.lower(), input_goal.lower()).ratio()
                        
                        score = (1.0 if domain_match else 0.0) + goal_sim
                        
                        matches.append((score, entry))
                    except: continue
            
            # Sort by score descending
            matches.sort(key=lambda x: x[0], reverse=True)
            
            # Take top 3 relevant examples
            top_matches = matches[:3]
            
            # Format as context string
            output = []
            for score, m in top_matches:
                if score > 0.4: # Threshold
                    action = m['output']['action']
                    reason = m['output']['reasoning']
                    output.append(f"- When goal was '{m['input']['goal']}' on '{m['input']['current_page']}': Action '{action}' ({reason})")
                    
            return "\n".join(output) if output else None
            
        except Exception as e:
            print(f"⚠️ Vector Search Failed: {e}")
            return None

    def update_from_run(self, trace, config):
        """Distills trace into permanent site-specific knowledge files."""
        url = config.get("target_url")
        netloc = urlparse(url).netloc
        site_path = os.path.join(self.root, "sites", netloc)
        os.makedirs(site_path, exist_ok=True)

        # 1. Update Locators
        loc_file = os.path.join(site_path, "locators.json")
        locs = {}
        if os.path.exists(loc_file):
            with open(loc_file, "r") as f:
                locs = json.load(f)
        
        for step in trace:
            page = step.get("page_name")
            target_desc = step.get("decision_reason", "")
            loc = step.get("locator_used")
            if page and loc:
                if page not in locs: locs[page] = []
                
                # Check for existing locator to update stability
                found = False
                # Update stability based on outcome
                adjustment = 1 if step.get("success", True) else -2  # Penalize failures harder?
                
                found = False
                for l in locs[page]:
                    if l['playwright'] == loc:
                        l['stability'] = l.get('stability', 1) + adjustment
                        found = True
                        break
                
                if not found:
                    locs[page].append({
                        "description": target_desc[:50], 
                        "playwright": loc,
                        "stability": adjustment
                    })

        with open(loc_file, "w") as f:
            json.dump(locs, f, indent=2)

        # 2. Update Site Metadata (YAML for LLM readability)
        meta_file = os.path.join(site_path, "meta.yaml")
        meta = {
            "site": netloc,
            "category": config.get("domain", "general"),
            "successful_runs": config.get("workflow_description", ""),
            "total_trace_steps": len(trace)
        }
        with open(meta_file, "w") as f:
            yaml.dump(meta, f)

        print(f"📖 Knowledge Bank updated for {netloc}")

    def export_knowledge(self, output_path="trained_kb.json"):
        """Aggregates all site and domain knowledge into a single portable JSON file."""
        data = {
            "sites": {},
            "domains": {},
            "library": []
        }

        # Collect sites
        site_root = os.path.join(self.root, "sites")
        if os.path.exists(site_root):
            for site in os.listdir(site_root):
                site_path = os.path.join(site_root, site)
                if os.path.isdir(site_path):
                    loc_file = os.path.join(site_path, "locators.json")
                    if os.path.exists(loc_file):
                        with open(loc_file, "r") as f:
                            data["sites"][site] = json.load(f)

        # Collect domains
        domain_root = os.path.join(self.root, "domains")
        if os.path.exists(domain_root):
            for domain in os.listdir(domain_root):
                if domain.endswith(".yaml"):
                    with open(os.path.join(domain_root, domain), "r") as f:
                        data["domains"][domain.replace(".yaml", "")] = yaml.safe_load(f)

        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"📦 Knowledge exported to: {output_path}")

    def add_manual_docs(self, domain, docs_text):
        """Allows manual injection of business logic/documentation."""
        path = os.path.join(self.root, "domains", f"{domain}.yaml")
        data = {"manual_documentation": docs_text}
        if os.path.exists(path):
            with open(path, "r") as f:
                try:
                    data = yaml.safe_load(f)
                    data["manual_documentation"] = docs_text
                except: pass
        
        with open(path, "w") as f:
            yaml.dump(data, f)
        print(f"✅ Documentation added to Knowledge Bank for domain: {domain}")

# Initialize some defaults
if __name__ == "__main__":
    kb = KnowledgeBank()
    # Create a default ecommerce pattern
    ecommerce_pattern = {
        "common_elements": {
            "cart": "[data-test='shopping-cart-link'], .shopping_cart_link, .fa-shopping-cart",
            "checkout": "[data-test='checkout'], button:contains('Checkout')",
            "login_button": "input[type='submit'], button:contains('Login')"
        },
        "workflow_rules": [
            "Always search for a cart icon after adding an item.",
            "If login fails, check for error-message-container."
        ]
    }
    with open(os.path.join(KB_ROOT, "domains", "ecommerce.yaml"), "w") as f:
        yaml.dump(ecommerce_pattern, f)
    
    # Create a few-shot library example
    with open(os.path.join(KB_ROOT, "library", "common_flows.md"), "w") as f:
        f.write("Example: To checkout, you usually follow: Cart -> Checkout Button -> Information Form -> Continue -> Finish.\n")
