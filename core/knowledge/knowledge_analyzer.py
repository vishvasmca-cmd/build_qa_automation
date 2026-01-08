import os
import json
import glob

def analyze_knowledge_bank():
    """Analyzes the knowledge bank to extract learning insights"""
    insights = {
        "total_sites": 0,
        "total_locators": 0,
        "proven_locators": 0,  # stability > 0
        "total_rules": 0,
        "domains": []
    }
    
    KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "..", "knowledge")
    
    # Analyze Sites
    sites_dir = os.path.join(KNOWLEDGE_DIR, "sites")
    if os.path.exists(sites_dir):
        for site in os.listdir(sites_dir):
            site_path = os.path.join(sites_dir, site)
            if not os.path.isdir(site_path):
                continue
            
            insights["total_sites"] += 1
            
            # Check locators.json
            loc_file = os.path.join(site_path, "locators.json")
            if os.path.exists(loc_file):
                try:
                    with open(loc_file, "r", encoding="utf-8") as f:
                        locs = json.load(f)
                        for page, locators in locs.items():
                            for loc in locators:
                                insights["total_locators"] += 1
                                if loc.get("stability", 0) > 0:
                                    insights["proven_locators"] += 1
                except:
                    pass
    
    # Analyze Domains
    domains_dir = os.path.join(KNOWLEDGE_DIR, "domains")
    if os.path.exists(domains_dir):
        for domain_file in glob.glob(os.path.join(domains_dir, "*.yaml")):
            try:
                import yaml
                with open(domain_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                    rules = data.get("learned_rules", [])
                    insights["total_rules"] += len(rules)
                    
                    domain_name = os.path.basename(domain_file).replace(".yaml", "")
                    if rules:
                        insights["domains"].append({
                            "name": domain_name,
                            "rules_count": len(rules)
                        })
            except:
                pass
    
    return insights
