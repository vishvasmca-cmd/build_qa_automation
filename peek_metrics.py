
import os
import sys
import json
from core.metrics_logger import logger

def peek():
    print("👀 Peeking into metrics.json (Lock-Aware)...")
    data = logger.data # logger.data is loaded in __init__ which calls _load()
    
    if not data or not data.get("events") and not data.get("failures"):
         print("📭 Metrics file is currently empty or couldn't be loaded.")
         return

    print(f"🆔 Run ID: {data.get('run_id')}")
    print(f"📊 Events: {len(data.get('events', []))}")
    print(f"❌ Failures: {len(data.get('failures', []))}")
    
    if data.get("events"):
        print("\nLatest Events:")
        for e in data["events"][-5:]:
            print(f"- {e.get('agent')} | {e.get('action')} | {e.get('success')}")

if __name__ == "__main__":
    sys.path.append(os.getcwd())
    peek()
