import subprocess
import time
import argparse
import os
import sys

def continuous_learning():
    parser = argparse.ArgumentParser(description="Run the agent in a continuous learning loop.")
    parser.add_argument("--project", required=True, help="Project specific name")
    parser.add_argument("--url", required=True, help="Target URL")
    parser.add_argument("--goal", required=True, help="Test goal")
    parser.add_argument("--domain", default="auto", help="Project domain")
    parser.add_argument("--iterations", type=int, default=5, help="Number of learning feedback loops to run")
    args = parser.parse_args()

    print(f"🚀 Starting Continuous Learning Loop for {args.project}")
    print(f"🎯 Goal: {args.goal}")
    print(f"🔄 Iterations: {args.iterations}\n")

    for i in range(1, args.iterations + 1):
        print(f"╔{'═'*50}╗")
        print(f"║ 🔁 Learning Iteration {i}/{args.iterations}".ljust(51) + "║")
        print(f"╚{'═'*50}╝")
        
        # 1. Clean previous short-term memory (trace) to force re-thinking
        #    but KEEP long-term memory (Knowledge Bank/locators.json)
        trace_path = os.path.join("projects", args.project, "outputs", "trace.json")
        screenshot_dir = os.path.join("projects", args.project, "screenshots")
        
        if os.path.exists(trace_path):
            try:
                os.remove(trace_path)
                print("🧹 Cleared short-term memory (trace.json) to force fresh exploration.")
            except Exception as e:
                print(f"⚠️ Could not clear trace: {e}")

        # 2. Run the Agent Pipeline
        #    This will:
        #    - Explore (using Long-Term Knowledge)
        #    - Generate Trace
        #    - Update Long-Term Knowledge (Stability++)
        #    - Generate Test
        #    - Execute Test
        cmd = [
            sys.executable, "run.py",
            "--project", args.project,
            "--url", args.url,
            "--goal", args.goal,
            "--domain", args.domain
        ]
        
        try:
            # Run and stream output
            result = subprocess.run(cmd, capture_output=False) # capture_output=False lets it print to console
            
            if result.returncode == 0:
                print(f"\n✅ Iteration {i} SUCCESS.")
                print("🧠 Knowledge Bank has been reinforced with stable locators.")
            else:
                print(f"\n❌ Iteration {i} FAILED.")
                print("🧠 Knowledge Bank has been updated to avoid unstable locators.")
                
        except Exception as e:
            print(f"🚨 Critical Error in execution: {e}")
            break
            
        print("\n⏳ Cooldown (5s)...\n")
        time.sleep(5)

    print("\n🎓 Continuous Learning Complete.")
    print("Check 'knowledge/sites/' to see the evolved Locator Stability scores.")

if __name__ == "__main__":
    continuous_learning()
