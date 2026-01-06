import os
import json
import time
import shutil
from datetime import datetime, timedelta
from termcolor import colored

class KnowledgeCurator:
    """
    Maintains the Knowledge Base by pruning old data and consolidating learnings.
    Functions:
    1. Prune old training runs (default > 7 days).
    2. Consolidate stable locators (remove failed ones).
    3. Aggregate cross-site patterns (Universal Selector Library).
    """
    
    def __init__(self, kb_root="knowledge"):
        self.root = kb_root
        self.sites_dir = os.path.join(self.root, "sites")
        self.runs_dir = os.path.join(self.root, "training_runs")
        
    def prune_history(self, days_to_keep=7, dry_run=False):
        """Removes training runs older than N days."""
        print(colored(f"\n🧹 Pruning History (> {days_to_keep} days)...", "cyan"))
        
        if not os.path.exists(self.runs_dir):
            print("No training runs found.")
            return

        cutoff_time = time.time() - (days_to_keep * 86400)
        deleted_count = 0
        preserved_count = 0
        
        for run_id in os.listdir(self.runs_dir):
            run_path = os.path.join(self.runs_dir, run_id)
            if not os.path.isdir(run_path):
                continue
                
            # Check for "golden" tag
            if os.path.exists(os.path.join(run_path, "golden.marker")):
                preserved_count += 1
                continue
                
            # Check age
            mtime = os.path.getmtime(run_path)
            if mtime < cutoff_time:
                if dry_run:
                    print(f"[Dry Run] would delete: {run_id}")
                else:
                    try:
                        shutil.rmtree(run_path)
                        deleted_count += 1
                    except Exception as e:
                        print(f"Failed to delete {run_id}: {e}")
            else:
                preserved_count += 1
                
        print(f"✅ Pruned {deleted_count} runs. Preserved {preserved_count} runs.")

    def consolidate_locators(self):
        """
        Scans all sites, removing locators with negative stability (meaning they failed repeatedly).
        """
        print(colored("\n🧬 Consolidating Locators...", "cyan"))
        
        if not os.path.exists(self.sites_dir):
            print("No sites knowledge found.")
            return
            
        total_removed = 0
        total_sites = 0
        
        for site in os.listdir(self.sites_dir):
            site_path = os.path.join(self.sites_dir, site)
            loc_file = os.path.join(site_path, "locators.json")
            
            if not os.path.exists(loc_file):
                continue
                
            total_sites += 1
            try:
                with open(loc_file, "r") as f:
                    locs = json.load(f)
                
                new_locs = {}
                site_removed = 0
                
                for page, items in locs.items():
                    # Keep items where stability >= 0
                    valid_items = [item for item in items if item.get("stability", 0) >= 0]
                    
                    if valid_items:
                        new_locs[page] = valid_items
                    
                    site_removed += len(items) - len(valid_items)
                
                if site_removed > 0:
                    with open(loc_file, "w") as f:
                        json.dump(new_locs, f, indent=2)
                    total_removed += site_removed
                    
            except Exception as e:
                print(f"⚠️ Error processing {site}: {e}")
                
        print(f"✅ Consolidated {total_sites} sites. Removed {total_removed} unstable selectors.")

    def extract_global_patterns(self, min_domains=2):
        """
        Identifies selectors that appear across multiple unique domains.
        Promotes them to a global pattern library.
        """
        print(colored(f"\n🌍 Extracting Global Patterns (Min Domains: {min_domains})...", "cyan"))
        
        if not os.path.exists(self.sites_dir):
            return

        selector_map = {} # selector -> set(domains)
        
        # 1. Scan all sites
        for domain_dir in os.listdir(self.sites_dir):
            loc_file = os.path.join(self.sites_dir, domain_dir, "locators.json")
            if not os.path.exists(loc_file):
                continue
                
            try:
                with open(loc_file, "r") as f:
                    data = json.load(f)
                    
                for page, items in data.items():
                    for item in items:
                        selector = item.get("playwright")
                        if selector and item.get("stability", 0) > 0:
                            if selector not in selector_map:
                                selector_map[selector] = set()
                            selector_map[selector].add(domain_dir)
            except: pass

        # 2. Filter for cross-domain patterns
        global_patterns = []
        for selector, domains in selector_map.items():
            if len(domains) >= min_domains:
                global_patterns.append({
                    "selector": selector,
                    "frequency": len(domains),
                    "example_domains": list(domains)[:3]
                })

        # 3. Save to Library
        global_patterns.sort(key=lambda x: x["frequency"], reverse=True)
        
        lib_dir = os.path.join(self.root, "library")
        os.makedirs(lib_dir, exist_ok=True)
        
        out_path = os.path.join(lib_dir, "global_patterns.json")
        with open(out_path, "w") as f:
            json.dump(global_patterns, f, indent=2)
            
        print(f"✅ Found {len(global_patterns)} global patterns. Saved to {out_path}")

    def run_all(self):
        self.prune_history()
        self.consolidate_locators()
        self.extract_global_patterns()

if __name__ == "__main__":
    curator = KnowledgeCurator()
    curator.run_all()
