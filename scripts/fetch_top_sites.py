import requests
import csv
import json
import os
import zipfile
import io

# Config
TRANCO_LIST_URL = "https://tranco-list.eu/top-1m.csv.zip"
TARGET_COUNT = 200
OUTPUT_FILE = "config/training_targets.json"

def fetch_and_generate_targets():
    print(f"🚀 Fetching Top {TARGET_COUNT} sites from Tranco List...")
    
    sites = []
    
    try:
        # Download Zip
        r = requests.get(TRANCO_LIST_URL)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        
        # Extract CSV content (usually named top-1m.csv)
        file_name = z.namelist()[0]
        print(f"   Reading {file_name}...")
        
        with z.open(file_name) as f:
            content = io.TextIOWrapper(f, encoding='utf-8')
            reader = csv.reader(content)
            
            count = 0
            for row in reader:
                # Tranco format: rank, domain
                if len(row) < 2: continue
                
                rank = row[0]
                domain = row[1]
                
                # Check exclusion list (optional)
                
                # Create Target Object
                site = {
                    "project": f"train_rank{rank}_{domain.replace('.', '_')}",
                    "url": f"https://{domain}",
                    "goal": "Launch website, find Login, Signup/GetStarted, Try for Free etc any 5 buttons and 2 links, 2 menu bar with out clicking any one of them",
                    "domain": "general_web",
                    "rank": int(rank)
                }
                
                sites.append(site)
                count += 1
                
                if count >= TARGET_COUNT:
                    break
                    
    except Exception as e:
        print(f"❌ Failed to fetch list: {e}")
        # Fallback to current list if fetch fails
        return

    # Save
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(sites, f, indent=4)
        
    print(f"✅ Generated {len(sites)} targets in {OUTPUT_FILE}")

if __name__ == "__main__":
    fetch_and_generate_targets()
