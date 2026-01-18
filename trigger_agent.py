import sys
import os
import subprocess
import json

def main():
    if len(sys.argv) < 2:
        print("Usage: python trigger_agent.py <config_path> [--headless]")
        sys.exit(1)
    
    config_path = sys.argv[1]
    project_dir = os.path.dirname(config_path)
    if not project_dir:
        project_dir = "."
        
    project_dir = os.path.abspath(project_dir)
    
    # Run orchestrator
    # We use --force to ensure we don't skip phases in CI
    cmd = [sys.executable, "orchestrator.py", "--project", project_dir, "--force"]
    
    # Headless is default in orchestrator (as it passes headless=True to agents by default)
    # agents default to headless=True unless --headed is passed to them.
    # orchestrator default for args.headed is False.
    
    print(f"🚀 Running Orchestrator for project: {project_dir}")
    print(f"Command: {' '.join(cmd)}")
    
    # Ensure current directory is project root so it can find orchestrator.py
    result = subprocess.run(cmd, capture_output=False)
    
    # Compatibility fix for CI: Ensure execution.json is copied to outputs/trace.json
    exec_path = os.path.join(project_dir, "execution.json")
    output_dir = os.path.join(project_dir, "outputs")
    trace_path = os.path.join(output_dir, "trace.json")
    
    if os.path.exists(exec_path):
        os.makedirs(output_dir, exist_ok=True)
        
        with open(exec_path, 'r', encoding='utf-8') as f:
            exec_data = json.load(f)
            
        # Transform for CI compatibility (old trace format)
        all_steps = []
        for scenario in exec_data.get("scenarios", []):
            for step in scenario.get("steps", []):
                all_steps.append(step)
            
        trace_data = {"trace": all_steps}
        
        with open(trace_path, 'w', encoding='utf-8') as f:
            json.dump(trace_data, f, indent=2)
        print(f"✅ Generated trace.json at {trace_path}")
    else:
        print(f"❌ Error: execution.json not found at {exec_path}")
        # Even if execution.json is missing, if orchestrator returned 0, we might have skipped everything
        # But in CI we want it to fail if no results were produced.
        if result.returncode == 0:
            sys.exit(1) # Force failure if results are missing
        sys.exit(result.returncode)

if __name__ == "__main__":
    main()
