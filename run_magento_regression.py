
import os
import sys
import json
import shutil
from termcolor import colored

# Add core to path
sys.path.append(os.path.join(os.getcwd(), 'core'))
from orchestrator import run_pipeline

def run_regression_e2e():
    print(colored("🚀 Starting Regression E2E Test: Luma Magento Store", "green", attrs=["bold"]))
    
    # 1. Project Setup
    project_name = "regression_magento_e2e"
    project_dir = os.path.join("projects", project_name)
    
    # Clean previous run if exists
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)
    os.makedirs(project_dir, exist_ok=True)
    os.makedirs(os.path.join(project_dir, "outputs"), exist_ok=True)
    os.makedirs(os.path.join(project_dir, "tests"), exist_ok=True)
    
    # 2. Configuration
    config = {
        "project_name": project_name,
        "target_url": "https://magento.softwaretestingboard.com/",
        "workflow_description": "Search for 'Radiant Tee', select size S, color Blue, add to cart, and go to checkout page.",
        "domain": "e_commerce",
        "testing_type": "regression",
        "paths": {
            "trace": os.path.join(project_dir, "outputs", "trace.json").replace("\\", "/"),
            "test": os.path.join(project_dir, "tests", "test_main.py").replace("\\", "/"),
            "report": os.path.join(project_dir, "outputs", "report.md").replace("\\", "/")
        }
    }
    
    config_path = os.path.join(project_dir, "config.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
        
    print(f"📄 Config created at: {config_path}")
    
    # 3. Clean global metrics to start fresh for this regression
    metrics_path = os.path.join("outputs", "metrics.json")
    if os.path.exists(metrics_path):
        os.remove(metrics_path)
    
    # 4. Execute Pipeline
    print(colored("🛠️  Invoking Orchestrator...", "cyan"))
    run_pipeline(config_path, headed=True)
    
    # 5. Summary
    print(colored("\n✨ Regression Run Finished!", "green", attrs=["bold"]))
    dashboard_path = os.path.join(project_dir, "outputs", "dashboard.html")
    if os.path.exists(dashboard_path):
        print(f"📊 Performance Dashboard: {dashboard_path}")

if __name__ == "__main__":
    run_regression_e2e()
