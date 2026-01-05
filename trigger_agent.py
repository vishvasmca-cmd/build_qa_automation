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
        
    print(f"🚀 Triggering agent with config: {config_path}")
    
    # We run headed=True by default for local debugging
    # The ExplorerAgent will automatically downgrade to headless in CI environments
    run_pipeline(config_path, headed=True)
