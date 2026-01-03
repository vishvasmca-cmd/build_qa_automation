import os
import subprocess
import time
import json
import random
from concurrent.futures import ThreadPoolExecutor

def load_training_sites():
    """Loads the list of training sites from the external JSON config."""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "training_targets.json")
    if not os.path.exists(config_path):
        print(f"⚠️ Config not found at {config_path}. Returning empty list.")
        return []
    with open(config_path, "r") as f:
        return json.load(f)

def process_site(site):
    print(f"🚀 [Started] Training on: {site['project']}")
    
    # Ensure logs dir exists
    log_dir = os.path.join("projects", site["project"])
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "training.log")
    
    cmd = [
        "python", "-u", "continuous_learning.py",
        "--project", site["project"],
        "--url", site["url"],
        "--goal", site["goal"],
        "--domain", site.get("domain", "auto"),
        "--docs", site.get("docs", ""),
        "--iterations", os.environ.get("CI_ITERATIONS", "10") # Default 10, override in CI
    ]
    
    try:
        start_time = time.time()
        # Redirect output to log file to avoid console chaos in parallel mode, UNLESS in CI
        is_ci = os.environ.get("CI") == "true"
        
        if is_ci:
            # In CI, we WANT to see logs in the console
            subprocess.run(cmd, check=True)
        else:
             # Enable UTF-8 for emojis in local file logs
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            
            with open(log_file, "w", encoding="utf-8") as f:
                subprocess.run(cmd, check=True, stdout=f, stderr=subprocess.STDOUT, env=env)
            
        duration = time.time() - start_time
        print(f"✅ [Finished] Training on {site['project']} in {duration:.2f}s")
    except subprocess.CalledProcessError as e:
        print(f"❌ [Failed] Training on {site['project']}. See logs in {log_file}")
    except Exception as e:
        print(f"❌ [Error] {site['project']}: {e}")

def run_training_loop():
    print("🧠 Starting Advanced Training Loop (Headless & Parallel & Dynamic)")
    
    try:
        all_sites = load_training_sites()
    except Exception as e:
        print(f"❌ Failed to load sites: {e}")
        return

    if not all_sites:
        print("❌ No sites found in config/training_targets.json")
        return

    # Dynamic Sampling for "New Sites Each Time"
    # Dynamic Sampling request
    # Since the user specifically configured the target list for a batch run, we should run ALL of them.
    sites_to_run = all_sites
    
    # Check for Limit Override
    batch_limit = os.environ.get("BATCH_LIMIT")
    if batch_limit:
        sites_to_run = sites_to_run[:int(batch_limit)]

    print(f"   → Mode: BATCH RUN ({len(sites_to_run)} sites)")
    print(f"   → Selected: {[s['project'] for s in sites_to_run]}")
    
    # Safe Concurrency Limit
    max_workers = int(os.environ.get("MAX_WORKERS", "4"))
    print(f"   → Parallel Workers: {max_workers}")
    
    # Use ThreadPoolExecutor to run sites in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_site, site) for site in sites_to_run]
        
        # Wait for all futures to complete
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"Worker exception: {e}")

    print("\n📦 Finalizing Advanced Knowledge Bank...")
    # Import locally to avoid startup overhead/conflicts
    try:
        from core.knowledge_bank import KnowledgeBank
        kb = KnowledgeBank()
        kb.export_knowledge("trained_kb_advanced_v1.json")
        print("🚀 Advanced training complete! Enhanced KB with multi-site patterns saved.")
    except Exception as e:
        print(f"⚠️ Could not export KB: {e}")

if __name__ == "__main__":
    run_training_loop()
