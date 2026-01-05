import json
import os
import subprocess
import time

def run_verification():
    print("Starting Broad Local Verification for 10 Sites...")
    
    # Load targets
    config_path = "config/verification_targets.json"
    with open(config_path, "r") as f:
        targets = json.load(f)
        
    results = []
    
    for i, target in enumerate(targets):
        project_name = target['project']
        url = target['url']
        goal = target['goal']
        
        print(f"\n[{i+1}/{len(targets)}] Verifying: {project_name} ({url})")
        
        # 1. Setup Project Config
        project_dir = f"projects/{project_name}"
        if not os.path.exists(project_dir):
            os.makedirs(project_dir, exist_ok=True)
            
        config_data = {
            "project_name": project_name,
            "target_url": url,
            "goal": goal,
            "depth_limit": 15,
            "strategies": ["search_first", "interactive_exploration"],
            "paths": {
                "trace": os.path.abspath(f"projects/{project_name}/outputs/trace.json"),
                "outputs": os.path.abspath(f"projects/{project_name}/outputs"),
                "test": os.path.abspath(f"projects/{project_name}/tests/e2e/test_main.py"),
                "report": os.path.abspath(f"projects/{project_name}/outputs/report.md")
            }
        }
        
        config_file = f"{project_dir}/config.json"
        with open(config_file, "w") as f:
            json.dump(config_data, f, indent=4)
        
        print(f"   Config created at {config_file}")
        
        start_time = time.time()
        try:
            # 2. Trigger Agent via Config
            print(f"   Running Agent...")
            # Use same python interpreter as current process
            cmd = ["python", "trigger_agent.py", config_file]
            
            # Force UTF-8 encoding for subprocess to handle emojis on Windows
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            
            # Using subprocess.run directly
            proc = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd(), encoding='utf-8', errors='ignore', env=env)
            
            if proc.returncode != 0:
                print(f"   Agent Error: {proc.stderr[-300:]}")
            
            # 3. Run Verified Test
            test_file = f"projects/{project_name}/tests/e2e/test_main.py"
            if os.path.exists(test_file):
                print(f"   Running Pytest Verification...")
                test_res = subprocess.run(["pytest", test_file], capture_output=True, text=True, encoding='utf-8', errors='ignore')
                
                status = "PASS" if test_res.returncode == 0 else "FAIL"
                print(f"   Result: {status}")
                if status == "FAIL":
                    print(f"   Error: {test_res.stdout[-500:]}")
            else:
                status = "NO TEST GENERATED"
                print("   Result: NO TEST GENERATED")
                if proc.returncode != 0:
                     status += " (Agent Crash)"

        except Exception as e:
            status = f"CRASH: {e}"
            print(status)
            
        duration = round(time.time() - start_time, 2)
        results.append({
            "project": project_name,
            "status": status,
            "duration": duration
        })
        
    # Summary
    print("\n" + "="*40)
    print("VERIFICATION SUMMARY")
    print("="*40)
    for res in results:
        print(f"{res['status']} | {res['project']} ({res['duration']}s)")
    print("="*40)

if __name__ == "__main__":
    run_verification()
