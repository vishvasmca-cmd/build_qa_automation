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
    # We prioritize exploring a random subset each run to ensure variety and coverage over time.
    batch_size = int(os.environ.get("BATCH_SIZE", "3"))
    
    # TEMP: Force specific sites for verification
    target_names = ["train_demoblaze", "train_realworld_conduit"]
    sites_to_run = [s for s in all_sites if s['project'] in target_names]
    
    if len(sites_to_run) < len(target_names):
         print(f"⚠️ warning: Could not find all targets in config. Falling back to random.")
         sites_to_run = random.sample(all_sites, min(len(all_sites), batch_size))

    print(f"   → Mode: FORCED VERIFICATION")
    print(f"   → Pool Size: {len(all_sites)} sites")
    print(f"   → Selected for this run: {[s['project'] for s in sites_to_run]}")
    
    # Use ThreadPoolExecutor to run sites in parallel
    with ThreadPoolExecutor(max_workers=batch_size) as executor:
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
