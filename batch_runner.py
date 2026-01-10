import os
import sys
import argparse
import subprocess
import time
import random
import glob
import json
from core.lib.git_utils import GitManager

def find_projects(projects_dir="projects"):
    """Finds all config.json files in the projects directory."""
    patterns = [
        os.path.join(projects_dir, "*", "config.json"),
        os.path.join(projects_dir, "stress_*", "config.json")
    ]
    projects = []
    for p in patterns:
        projects.extend(glob.glob(p))
    return list(set(projects))

def run_project(config_path, headless=True):
    """Runs a single project with a timeout."""
    project_dir = os.path.dirname(config_path)
    project_name = os.path.basename(project_dir)
    
    print(colored(f"\n🚀 Launching {project_name}...", "cyan"))
    
    cmd = ["python", "trigger_agent.py", config_path]
    if headless:
        cmd.append("--headless")
        
    start_time = time.time()
    try:
        # 30-minute timeout per project
        # We allow output to flow to stdout/stderr so user sees progress
        result = subprocess.run(cmd, capture_output=False, text=True, encoding='utf-8', errors='replace', timeout=1800)
        duration = time.time() - start_time
        
        success = result.returncode == 0
        if success:
            print(colored(f"✅ Passed ({duration:.1f}s)", "green"))
        else:
            print(colored(f"❌ Failed ({duration:.1f}s)", "red"))
            # Output is already printed, so no need to print stderr again
                
        return success, duration
        
    except subprocess.TimeoutExpired:
        print(colored(f"⏱️ TIMEOUT (30m) - Process killed.", "red"))
        return False, 1800
    except Exception as e:
        print(colored(f"⚠️ Execution Error: {e}", "yellow"))
        return False, 0

def main():
    parser = argparse.ArgumentParser(description="Batch Runner for AI Pipelines")
    parser.add_argument("--limit", type=int, default=10, help="Max number of projects to run")
    parser.add_argument("--headed", action="store_true", help="Run with browser visible")
    parser.add_argument("--sequential", action="store_true", help="Run in alphabetical order instead of random")
    
    args = parser.parse_args()
    
    print(colored("🏁 Starting Batch Runner...", "cyan"))
    
    projects = find_projects()
    if not projects:
        print(colored("❌ No projects found in projects/ directory.", "red"))
        sys.exit(1)
        
    print(colored(f"ℹ️ Found {len(projects)} total projects.", "blue"))
    
    # Selection Logic
    if not args.sequential:
        random.shuffle(projects)
    
    selected_projects = projects[:args.limit]
    print(colored(f"ℹ️ Queueing {len(selected_projects)} projects for execution.", "blue"))
    
    passed = 0
    failed = 0
    
    for i, config_path in enumerate(selected_projects):
        print(colored(f"\n--- Project {i+1}/{len(selected_projects)} ---", "white"))
        success, duration = run_project(config_path, headless=not args.headed)
        
        if success:
            passed += 1
            status = "PASS"
        else:
            failed += 1
            status = "FAIL"
            
        # Git Sync after each project (Learn as we go)
        # Using the fixed static method
        try:
            project_name = os.path.basename(os.path.dirname(config_path))
            commit_msg = f"BatchRun: {project_name} - {status}"
            GitManager.commit_and_push(commit_msg)
        except Exception as e:
            print(colored(f"⚠️ Git Sync failed: {e}", "yellow"))
            
    print("\n" + "="*40)
    print(f"BATCH SUMMARY: Passed: {passed} | Failed: {failed}")
    print("="*40)
    
    sys.exit(1 if failed > 0 else 0)

if __name__ == "__main__":
    main()
