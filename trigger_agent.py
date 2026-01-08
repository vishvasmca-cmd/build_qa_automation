import sys
import os

# Ensure core is in path
sys.path.append(os.getcwd())

from core.engine.orchestrator import run_pipeline

if __name__ == "__main__":

    if len(sys.argv) > 1:
        config_path = os.path.abspath(sys.argv[1])
    else:
        config_path = os.path.abspath("projects/playwright_smoke/config.json")
        
    print(f"Triggering agent with config: {config_path}")
    
    headed_mode = False
    if "--headed" in sys.argv:
        headed_mode = True
        
    robust_mode = "--robust" in sys.argv

    while True:
        success = run_pipeline(config_path, headed=headed_mode)
        if success or not robust_mode:
            break
        print("\n" + "="*60)
        print("🔄 ROBUST MODE: Pipeline failed. Restarting for self-healing...")
        print("="*60 + "\n")
        import time
        time.sleep(5)
