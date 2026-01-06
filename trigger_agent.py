import sys
import os

# Ensure core is in path
sys.path.append(os.getcwd())

from core.orchestrator import run_pipeline

if __name__ == "__main__":

    if len(sys.argv) > 1:
        config_path = os.path.abspath(sys.argv[1])
    else:
        config_path = os.path.abspath("projects/playwright_smoke/config.json")
        
    print(f"Triggering agent with config: {config_path}")
    
    headed_mode = True
    if "--headless" in sys.argv:
        headed_mode = False

    run_pipeline(config_path, headed=headed_mode)
