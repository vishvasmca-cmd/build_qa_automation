import json
import os
import subprocess
import sys
import time
from datetime import datetime

STATE_FILE = "batch_state.json"
TARGETS_FILE = "config/training_targets.json"
BATCH_SIZE = 10
LIMIT = 100

def load_targets():
    if not os.path.exists(TARGETS_FILE):
        print(f"Error: {TARGETS_FILE} not found.")
        sys.exit(1)
    with open(TARGETS_FILE, 'r') as f:
        return json.load(f)

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"last_index": 0}

def save_state(index):
    with open(STATE_FILE, 'w') as f:
        json.dump({"last_index": index, "last_updated": str(datetime.now())}, f)

def run_batch():
    print(f"🔥 Continuous Batch Runner Initialized")
    targets = load_targets()
    state = load_state()
    start_index = state['last_index']
    
    # Sort by rank just in case
    targets.sort(key=lambda x: x.get('rank', 9999))
    
    if start_index >= len(targets) or start_index >= LIMIT:
        print(f"✅ All targets processed (Index: {start_index}, Limit: {LIMIT})")
        return

    end_index = min(start_index + BATCH_SIZE, min(len(targets), LIMIT))
    batch = targets[start_index:end_index]
    
    print(f"🚀 Processing Batch: {start_index} -> {end_index} (Size: {len(batch)})")
    
    for i, item in enumerate(batch):
        project_name = item['project']
        url = item['url']
        goal = item['goal']
        rank = item.get('rank', '?')
        
        print(f"\n[{i+1}/{len(batch)}] 🌍 Site #{rank}: {url}")
        print(f"   📂 Project: {project_name}")
        
        # Construct command
        cmd = [
            sys.executable, "trigger_agent.py",
            "--url", url,
            "--goal", goal,
            "--name", project_name,
            "--headless" # Ensure headless for batch
        ]
        
        start_time = time.time()
        try:
            # Run with screen output visible so user can monitor
            subprocess.run(cmd, check=False, timeout=2400) # 40 min timeout per site (generous)
        except subprocess.TimeoutExpired:
            print(f"   ❌ Timeout expired (40m). Moving to next.")
        except Exception as e:
            print(f"   ⚠️ Unexpected Error: {e}")
            
        duration = time.time() - start_time
        print(f"   🕒 Duration: {duration:.1f}s")
        
        # Update state immediately after each successful run to avoid re-work on crash
        # Actually, let's keep batch transactional? No, granular is better.
        # But for 'batch' concept, typically valid to update at end. 
        # But if it crashes at item 5, we re-run 0-5. 
        # I'll update at end of batch as requested "10 website each run".
        
    save_state(end_index)
    print(f"\n✅ Batch {int(start_index/BATCH_SIZE) + 1} Complete. New State Index: {end_index}")
    print(f"   To run next batch, execute this script again.\n")

if __name__ == "__main__":
    run_batch()
