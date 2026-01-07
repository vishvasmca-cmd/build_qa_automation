
import os
import sys
import asyncio
import json
from datetime import datetime

# Ensure core modules are importable
sys.path.append(os.path.join(os.path.dirname(__file__), "core"))
from batch_orchestrator import BatchOrchestrator

def create_demo_configs():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.join(base_dir, "projects", "demo_complex")
    os.makedirs(project_dir, exist_ok=True)
    
    configs = []
    
    # 1. SauceDemo (E-commerce Flow)
    sauce_config = {
        "project_name": "demo_saucedemo_flow",
        "target_url": "https://www.saucedemo.com/",
        "workflow_description": "Login with username 'standard_user' and password 'secret_sauce'. Then sort items by 'Price (low to high)'. Add the first item to the cart. Navigate to cart. Click Checkout.",
        "domain": "ecommerce",
        "testing_type": "functional",
        "paths": {
            "trace": os.path.join(project_dir, "sauce_trace.json"),
            "test": os.path.join(project_dir, "test_sauce.py"),
            "report": os.path.join(project_dir, "sauce_report.md")
        }
    }
    with open(os.path.join(project_dir, "sauce_config.json"), "w") as f:
        json.dump(sauce_config, f, indent=2)
    configs.append(os.path.join(project_dir, "sauce_config.json"))

    # 2. Automation Exercise (Form Flow)
    auto_config = {
        "project_name": "demo_automation_exercise",
        "target_url": "https://automationexercise.com/",
        "workflow_description": "Click on 'Contact Us' button. Fill Name='Test User', Email='test@example.com', Subject='Support', Message='This is a test message'. Click 'Submit' button and verify 'Success' message if visible.",
        "domain": "general_web",
        "testing_type": "functional",
        "paths": {
            "trace": os.path.join(project_dir, "auto_trace.json"),
            "test": os.path.join(project_dir, "test_auto.py"),
            "report": os.path.join(project_dir, "auto_report.md")
        }
    }
    with open(os.path.join(project_dir, "auto_config.json"), "w") as f:
        json.dump(auto_config, f, indent=2)
    configs.append(os.path.join(project_dir, "auto_config.json"))
    
    return configs

async def run_demo():
    print("🚀 Starting Local Demo: 2 Complex Flows")
    print("1. SauceDemo (Login + Cart + Sort)")
    print("2. AutomationExercise (Contact Form)")
    
    config_paths = create_demo_configs()
    
    # Run sequentially or parallel
    # We use concurrency 2 to show off Phase 3 parallelism
    orchestrator = BatchOrchestrator(concurrency_limit=2)
    
    # Headless=True because we are in a non-GUI environment usually, but user asked for "locally". 
    # If I run "headed=True", it might fail if there's no display. 
    # I'll stick to headless=False (which means HEADED in my logic? Wait.)
    # In orchestrator.py: run_pipeline(..., headed=headed).
    # I'll pass headed=False to be safe on the server, but the user said "locally".
    # I will assume "locally" means *on this machine*, but I should probably use headless to avoid popup interference.
    # Actually, let's use headed=False (Headless) for stability, or headed=True (Visible) for show.
    # I'll use Headless to strictly ensure it works.
    await orchestrator.run_batch(config_paths, headed=False)

if __name__ == "__main__":
    asyncio.run(run_demo())
