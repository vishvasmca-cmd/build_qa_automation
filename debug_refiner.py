
import sys
import os
import json
import asyncio
from dotenv import load_dotenv

# Ensure core is in path
sys.path.append(os.getcwd())

from core.agents.refiner import CodeRefiner

def test_refiner():
    # Path to the trace we found (nested weirdly)
    trace_path = r"projects\cli_run_1767916981\projects\cli_run_1767916981\outputs\trace.json"
    
    if not os.path.exists(trace_path):
        print(f"❌ Trace not found at {trace_path}")
        return

    print(f"✅ Loaded trace from {trace_path}")
    
    # Initialize Refiner
    refiner = CodeRefiner()
    
    # Goal
    goal = "Register, Login, Open Account, Transfer Funds, and Request Loan"
    
    # Mock Config
    config = {
        "project_name": "debug_refiner_test",
        "domain": "parabank.parasoft.com",
        "target_url": "https://parabank.parasoft.com/parabank/index.htm"
    }
    
    # Read trace content
    with open(trace_path, "r") as f:
        trace_data = json.load(f)
        # We need a summary string. CodeRefiner expects a JSON string of steps.
        # In real pipeline, orchestrator creates this summary.
        # Let's just dump the 'trace' key.
        trace_summary = json.dumps(trace_data.get("trace", []), indent=2)

    print("⏳ generating code...")
    # Generate Code
    # Signature: generate_code(self, target_url, trace_summary, images=None, error_context=None, domain="general", workflow_goal=None)
    code = refiner.generate_code(
        target_url=config["target_url"], 
        trace_summary=trace_summary, 
        domain=config["domain"],
        workflow_goal=goal
    )
    
    print("\n" + "="*40)
    print("GENERATED CODE:")
    print("="*40)
    print(code)
    print("="*40)

if __name__ == "__main__":
    load_dotenv()
    test_refiner()
