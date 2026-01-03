import csv
import os
import subprocess
import sys
import re
import argparse

def clean_project_name(brand):
    # Sanitize brand name for project folder using only alphanumeric and underscore
    clean = re.sub(r'[^a-zA-Z0-9]', '_', brand).lower()
    return f"train_{clean}"

def run_batch():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0, help="Max number of sites to run (0 for all)")
    parser.add_argument("--offset", type=int, default=0, help="Start index")
    args = parser.parse_args()

    csv_path = os.path.join("config", "landing_pages_targets.csv")
    if not os.path.exists(csv_path):
        print(f"❌ CSV not found: {csv_path}")
        return

    print(f"📂 Reading targets from {csv_path}...")
    
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        targets = list(reader)

    print(f"🚀 Found {len(targets)} total landing pages.")
    
    # Slice list based on offset/limit
    start = args.offset
    end = len(targets)
    if args.limit > 0:
        end = start + args.limit
    
    targets_to_run = targets[start:end]
    print(f"▶️ Processing {len(targets_to_run)} sites (Index {start} to {end})...")

    for i, row in enumerate(targets_to_run):
        brand = row.get("Brand", "Unknown")
        url = row.get("URL", "")
        cta = row.get("Primary CTA", "")
        headline = row.get("Hero Headline Pattern", "")
        
        if not url:
            continue

        project_name = clean_project_name(brand)
        goal = f"Navigate to {brand} homepage. Verify the hero headline contains '{headline}'. Find and click the '{cta}' button."
        
        real_index = start + i + 1
        print(f"\n[{real_index}/{len(targets)}] 🚂 Mining {brand} ({url})...")
        print(f"   Goal: {goal}")
        
        cmd = [
            sys.executable, "run.py",
            "--project", project_name,
            "--url", url,
            "--goal", goal,
            "--type", "smoke",
            "--generate-spec" # Generate spec and trace
        ]
        
        try:
            # Run with a timeout to prevent hanging on one bad site
            # Increase timeout if needed, mining can be slow
            # Using 5 minutes per site
            subprocess.run(cmd, timeout=300) 
            print(f"✅ Finished {brand}")
        except subprocess.TimeoutExpired:
            print(f"⚠️ Timeout running {brand}")
        except Exception as e:
            print(f"❌ Error running {brand}: {e}")

if __name__ == "__main__":
    run_batch()
