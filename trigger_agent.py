import sys
import os

# Ensure core is in path
sys.path.append(os.getcwd())

from core.orchestrator import run_pipeline

if __name__ == "__main__":
    config_path = os.path.abspath("projects/playwright_smoke/config.json")
    # user asked for "mining" and "test plan", which run_pipeline does.
    # We run headed=True so user can see it if they want (though they usually can't see the screen directly, it helps debugging)
    run_pipeline(config_path, headed=True)
