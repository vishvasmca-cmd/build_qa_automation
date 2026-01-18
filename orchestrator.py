import os
import sys
import json
import argparse
import subprocess
import core.lib.llm_utils # Ensure any early side effects don't break
from datetime import datetime
from termcolor import colored
from typing import Dict, Any

# Framework Version

# Framework Version
VERSION = "1.0.0"

class Orchestrator:
    def __init__(self, project_dir: str, deep_mode: bool = False):
        self.project_dir = os.path.abspath(project_dir)
        self.project_name = os.path.basename(self.project_dir)
        
        # Ensure project directory exists
        os.makedirs(self.project_dir, exist_ok=True)
        
        self.workflow_path = os.path.join(self.project_dir, "workflow.json")
        self.execution_path = os.path.join(self.project_dir, "execution.json")
        self.checkpoint_path = os.path.join(self.project_dir, ".checkpoint.json")
        self.config_path = os.path.join(self.project_dir, "config.json")
        self.config = self._load_config()
        self.deep_mode = deep_mode  # New flag to trigger deep explorer
        
    def _load_config(self) -> Dict:
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                try:
                    return json.load(f)
                except:
                    return {}
        return {}
        
    def _save_checkpoint(self, phase: str):
        checkpoint = {}
        if os.path.exists(self.checkpoint_path):
            with open(self.checkpoint_path, 'r') as f:
                try:
                    checkpoint = json.load(f)
                except:
                    checkpoint = {}
        
        checkpoint[phase] = {
            "status": "completed",
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.checkpoint_path, 'w') as f:
            json.dump(checkpoint, f, indent=2)

    def _is_phase_completed(self, phase: str) -> bool:
        if not os.path.exists(self.checkpoint_path):
            return False
        with open(self.checkpoint_path, 'r') as f:
            try:
                checkpoint = json.load(f)
                return checkpoint.get(phase, {}).get("status") == "completed"
            except:
                return False

    def run_phase(self, phase_name: str, script_name: str, args: list, skip_if_done: bool = True):
        if skip_if_done and self._is_phase_completed(phase_name):
            print(colored(f"SKIP] Phase '{phase_name}' already completed. Skipping...", "cyan"))
            return True

        print(colored(f"\n[PHASE] Running Phase: {phase_name.upper()}", "blue", attrs=["bold"]))
        
        # Use absolute path for script
        script_path = os.path.join(os.path.dirname(__file__), "core", "agents", script_name)
        if not os.path.exists(script_path):
            # Try root level for script_name
            script_path = os.path.join(os.path.dirname(__file__), script_name)
            
        cmd = [sys.executable, script_path] + args
        print(colored(f"   Command: {' '.join(cmd)}", "grey"))
        
        try:
            # Run from project root to ensure imports work
            project_root = os.path.dirname(__file__)
            result = subprocess.run(cmd, check=True, cwd=project_root)
            if result.returncode == 0:
                self._save_checkpoint(phase_name)
                print(colored(f"✅ Phase '{phase_name}' completed successfully.", "green"))
                return True
        except subprocess.CalledProcessError as e:
            print(colored(f"❌ Phase '{phase_name}' failed with error: {e}", "red"))
            return False
        
        return False

    def execute_pipeline(self, goal: str = None, force: bool = False, security: bool = False, headed: bool = False, phase: str = None, base_url: str = None):
        # Use config defaults if not provided
        goal = goal or self.config.get("goal") or self.config.get("workflow_description")  # Try "goal" first, fallback to old key
        base_url = base_url or self.config.get("target_url")

        if force and os.path.exists(self.checkpoint_path):
            os.remove(self.checkpoint_path)

        # 1. INITIAL DISCOVERY PHASE (Discovery-First)
        # This captures the landing page structure to help the planner
        # We only run this in DEEP mode by default, or if explicitly requested.
        if (not phase and self.deep_mode) or phase == "discovery":
             # Use the new Semantic Discovery Agent
             discovery_script = "discovery.py"
             # Use configured URL or default
             url = base_url or self.config.get("target_url") or "https://automationexercise.com"
             discovery_args = ["--project", self.project_dir, "--url", url]
             
             if self.deep_mode:
                 discovery_args.append("--deep")
             
             # Check if sitemap exists to potentially skip
             sitemap_path = os.path.join(self.project_dir, "sitemap.json")
             should_skip = not (phase == "discovery")
             
             if os.path.exists(sitemap_path) and os.path.getsize(sitemap_path) > 100:
                 print(colored(f"⚡ [SKIP] Sitemap found ({os.path.getsize(sitemap_path)} bytes). Skipping Discovery.", "cyan"))
                 # Update checkpoint to satisfy dependencies
                 self._save_checkpoint("discovery")
             else:
                 if not self.run_phase("discovery", discovery_script, discovery_args, skip_if_done=should_skip):
                     print(colored("⚠️ Initial discovery failed, but proceeding to planning...", "yellow"))

        # 2. PLANNING PHASE
        if not phase or phase == "planning":
            planner_script = "planner.py"
            planner_args = ["--project", self.project_dir]
            if goal:
                planner_args += ["--goal", goal]
            if base_url:
                planner_args += ["--url", base_url]
            if self.deep_mode:
                planner_args.append("--deep")
            
            # If specifically requested via --phase, don't skip
            
            # If specifically requested via --phase, don't skip
            skip = not (phase == "planning")
            if not self.run_phase("planning", planner_script, planner_args, skip_if_done=skip):
                print(colored("⛔ Pipeline aborted at Planning phase.", "red"))
                return

        # 3. EXPLORATION / MINING PHASE
        if not phase or phase == "exploration":
            # Choose script based on deep mode
            explorer_script = "deep_explorer.py" if self.deep_mode else "explorer.py"
            explorer_args = ["--project", self.project_dir]
            if headed:
                explorer_args.append("--headed")
            
            skip = not (phase == "exploration")
            if not self.run_phase("exploration", explorer_script, explorer_args, skip_if_done=skip):
                print(colored("⛔ Pipeline aborted at Exploration phase.", "red"))
                return
            
            # Validation: Did exploration actually find things?
            if not self._is_exploration_healthy():
                print(colored("⚠️ Exploration failed to find stable locators for key steps. Execution might fail.", "yellow"))
                # Optionally stop here if we want to be strict

        # 3. EXECUTION PHASE
        if not phase or phase == "execution":
            executor_script = "executor.py"
            executor_args = ["--project", self.project_dir]
            if headed:
                executor_args.append("--headed")
            
            skip = not (phase == "execution")
            if not self.run_phase("execution", executor_script, executor_args, skip_if_done=skip):
                print(colored("⛔ Pipeline aborted at Execution phase.", "red"))
                return

        # 4. SECURITY AUDIT (Optional)
        if security or phase == "security":
            security_script = "security_auditor.py"
            # Need to read URL from config or workflow
            with open(self.workflow_path, 'r') as f:
                wf = json.load(f)
                url = wf.get("base_url")
            
            security_args = [url, self.project_dir]
            self.run_phase("security", security_script, security_args, skip_if_done=False)

        print(colored("\n[DONE] Pipeline Execution Finished! [DONE]", "green", attrs=["bold"]))

    def _is_exploration_healthy(self) -> bool:
        """Checks if exploration phase populated locators for most steps."""
        if not os.path.exists(self.workflow_path):
            return False
        try:
            with open(self.workflow_path, 'r', encoding='utf-8') as f:
                wf = json.load(f)
            
            total_steps = 0
            steps_with_locators = 0
            for scenario in wf.get("scenarios", []):
                for step in scenario.get("steps", []):
                    # We skip 'navigate' as it doesn't need locators
                    if step.get("keyword") == "navigate":
                        continue
                    total_steps += 1
                    if step.get("locators"):
                        steps_with_locators += 1
            
            if total_steps == 0: return True
            success_rate = (steps_with_locators / total_steps) * 100
            print(colored(f"📊 Exploration Discovery Success Rate: {success_rate:.1f}%", "cyan"))
            
            # If less than 50% found, consider it unhealthy
            return success_rate > 50
        except:
            return False

def main():
    parser = argparse.ArgumentParser(description="Keyword-Driven AI Automation Orchestrator")
    parser.add_argument("--project", required=True, help="Path to the project directory")
    parser.add_argument("--goal", help="High-level goal for the planner")
    parser.add_argument("--force", action="store_true", help="Clear checkpoints and re-run all phases")
    parser.add_argument("--security", action="store_true", help="Run security auditor after execution")
    parser.add_argument("--headed", action="store_true", help="Run browsers in headed mode")
    parser.add_argument("--phase", choices=["planning", "exploration", "execution", "security"], help="Run a specific phase only")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")

    parser.add_argument("--base_url", help="Base URL for the project")
    parser.add_argument("--deep", action="store_true", help="Run deep explorer mode (generate regression test scenarios)")
    
    args = parser.parse_args()
    
    orchestrator = Orchestrator(args.project, deep_mode=args.deep)
    
    # 3. RUN
    orchestrator.execute_pipeline(
        goal=args.goal, 
        force=args.force, 
        security=args.security, 
        headed=args.headed,
        phase=args.phase,
        base_url=args.base_url
    )

if __name__ == "__main__":
    main()
