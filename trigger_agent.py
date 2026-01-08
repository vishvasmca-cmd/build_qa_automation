import sys
import os
import argparse
import json
import time

# Ensure core is in path
sys.path.append(os.getcwd())

from core.engine.orchestrator import run_pipeline

def create_temp_config(args):
    """Creates a temporary config file from CLI args"""
    project_slug = args.name or "cli_run_" + str(int(time.time()))
    project_dir = os.path.join("projects", project_slug)
    os.makedirs(project_dir, exist_ok=True)
    
    config = {
        "project_name": project_slug,
        "target_url": args.url,
        "workflow_description": args.goal,
        "domain": args.domain or "general",
        "paths": {
            "test": f"projects/{project_slug}/tests/test_main.py",
            "report": f"projects/{project_slug}/outputs/report.md"
        }
    }
    
    config_path = os.path.join(project_dir, "config.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
        
    return config_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trigger the Antigravity Agent")
    
    # Mode 1: Config File
    parser.add_argument("config_path", nargs="?", help="Path to config.json")
    
    # Mode 2: Direct CLI
    parser.add_argument("--url", help="Target Website URL")
    parser.add_argument("--goal", help="What should the agent achieve?")
    parser.add_argument("--name", help="Project Name (optional)")
    parser.add_argument("--domain", help="Domain (e.g., banking, ecommerce)")
    
    # Global Flags
    parser.add_argument("--headed", action="store_true", help="Watch the browser")
    parser.add_argument("--robust", action="store_true", help="Run in continuous self-healing mode")

    args = parser.parse_args()

    # Determine Config Source
    if args.url and args.goal:
        print(f"⚡ Running in CLI Mode: {args.project_name if hasattr(args, 'project_name') else 'Ad-hoc'}")
        config_path = create_temp_config(args)
    elif args.config_path:
        config_path = os.path.abspath(args.config_path)
    else:
        print("❌ Error: You must provide either a config path OR (--url AND --goal)")
        sys.exit(1)

    print(f"🚀 Triggering agent with config: {config_path}")

    while True:
        success = run_pipeline(config_path, headed=args.headed)
        if success or not args.robust:
            break
        print("\n" + "="*60)
        print("🔄 ROBUST MODE: Pipeline failed. Restarting for self-healing...")
        print("="*60 + "\n")
        time.sleep(5)
