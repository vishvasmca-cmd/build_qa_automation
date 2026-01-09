import sys
import os
import json
import subprocess
import time
import random
import argparse
from concurrent.futures import ThreadPoolExecutor

# Import RAG and Git utilities
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core.knowledge.rag_synthesizer import RAGSynthesizer
try:
    from core.lib.git_utils import GitManager
except ImportError:
    # Basic fallback if git_utils is moved/renamed
    GitManager = None

# Windows Unicode Fix
try:
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

def setup_project(proj):
    """Creates directory and config.json"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    proj_dir = os.path.join(base_dir, "projects", proj["name"])
    outputs_dir = os.path.join(proj_dir, "outputs")
    os.makedirs(outputs_dir, exist_ok=True)
    
    # Randomize unique values in description to prevent collisions
    unique_id = f"{random.randint(1000,9999)}"
    desc = proj.get("description", proj.get("goal", "")).replace("(unique)", unique_id).replace("unique", unique_id)
    
    config = {
        "project_name": proj["name"],
        "target_url": proj["url"],
        "domain": proj.get("domain", "general"),
        "workflow_description": desc,
        "depth_limit": 40,
        "strategies": ["interactive_exploration", "long_flow"],
        "paths": {
            "trace": os.path.join(outputs_dir, "trace.json").replace("\\", "\\\\"),
            "outputs": outputs_dir.replace("\\", "\\\\"),
            "test": os.path.join(proj_dir, "tests", "e2e", "test_main.py").replace("\\", "\\\\"),
            "report": os.path.join(outputs_dir, "report.md").replace("\\", "\\\\")
        }
    }
    
    with open(os.path.join(proj_dir, "config.json"), "w") as f:
        json.dump(config, f, indent=2)
    
    return os.path.join(proj_dir, "config.json")

def run_project(config_path, headless=True):
    print(f"🚀 Launching {config_path}...")
    cmd = ["python", "trigger_agent.py", config_path]
    if headless:
        cmd.append("--headless")
        
    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    duration = time.time() - start
    
    success = result.returncode == 0 and "Test Execution SUCCESS!" in result.stdout
    
    if not success:
        print(f"DEBUG: Return Code: {result.returncode}")
        print(f"DEBUG: StdErr: {result.stderr}")
    
    return {
        "config": config_path,
        "success": success,
        "duration": duration,
        "log_tail": result.stdout[-500:],
        "error": result.stderr if not success else ""
    }

def main():
    parser = argparse.ArgumentParser(description="Batch Stress Tester")
    parser.add_argument("--random", type=int, help="Number of random projects to run")
    parser.add_argument("--targets", default="config/stress_targets.json", help="Path to targets JSON")
    parser.add_argument("--headed", action="store_true", help="Run in headed mode")
    args = parser.parse_args()

    # Load targets
    if not os.path.exists(args.targets):
        print(f"❌ Error: Targets file not found at {args.targets}")
        sys.exit(1)
        
    with open(args.targets, "r") as f:
        all_targets = json.load(f)

    selected_targets = all_targets
    if args.random:
        selected_targets = random.sample(all_targets, min(args.random, len(all_targets)))

    results = []
    print(f"🏁 Starting Batch Test for {len(selected_targets)} projects (Pool: {len(all_targets)})...")
    
    for p in selected_targets:
        cfg = setup_project(p)
        # Clear previous checkpoints to force fresh run
        checkpoints = [
            os.path.join(os.path.dirname(cfg), ".checkpoint_planning"),
            os.path.join(os.path.dirname(cfg), ".checkpoint_exploration"),
            os.path.join(os.path.dirname(cfg), ".checkpoint_generation"),
            os.path.join(os.path.dirname(cfg), ".checkpoint_review"),
            os.path.join(os.path.dirname(cfg), ".checkpoint_execution"),
            os.path.join(os.path.dirname(cfg), ".checkpoint.json")
        ]
        for cp in checkpoints:
            if os.path.exists(cp): os.remove(cp)
            
        res = run_project(cfg, headless=not args.headed)
        results.append(res)
        
        status = "✅ PASS" if res['success'] else "❌ FAIL"
        status = "✅ PASS" if res['success'] else "❌ FAIL"
        print(f"Finished {p['name'] if 'name' in p else p.get('project', 'unknown')}: {status} ({res['duration']:.1f}s)")

        # ---------------------------------------------------------
        # POST-RUN AUTOMATION (RAG & GIT)
        # ---------------------------------------------------------
        try:
            # 1. RAG Synthesis (Active Learning)
            print("🧠 Running RAG Synthesis...")
            synthesizer = RAGSynthesizer()
            synthesizer.harvest_failures()
            synthesizer.generate_knowledge_graph()
            
            # 2. Git Sync (Commit & Push)
            if GitManager:
                print("🔄 Syncing with Remote...")
                git = GitManager(os.getcwd())
                commit_msg = f"Auto-Learned: {p.get('name', 'unknown')} - {status}"
                git.safe_commit_and_push(commit_msg)
            else:
                # Fallback CLI Git
                subprocess.run(["git", "add", "."], check=False)
                subprocess.run(["git", "commit", "-m", f"Auto-Learned: {p.get('name', 'unknown')} - {status}"], check=False)
                subprocess.run(["git", "pull", "--rebase", "origin", "main"], check=False)
                subprocess.run(["git", "push", "origin", "main"], check=False)
                
        except Exception as e:
            print(f"⚠️ Post-run automation failed: {e}")
        # ---------------------------------------------------------

    # Summary
    print("\n" + "="*50)
    print("BATCH TEST SUMMARY")
    print("="*50)
    passed = sum(1 for r in results if r['success'])
    print(f"Total: {len(results)}, Passed: {passed}, Failed: {len(results) - passed}")
    
    for r in results:
        name = os.path.basename(os.path.dirname(r['config']))
        status = "PASS" if r['success'] else "FAIL"
        print(f"{name:30} | {status}")

if __name__ == "__main__":
    main()
