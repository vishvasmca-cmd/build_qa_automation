import sys
import json
import os
import subprocess
import time
from datetime import datetime

# UTF-8 fix for Windows console
try:
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

def load_core_targets():
    """Loads the 5 core websites from config/core_targets.json"""
    config_path = os.path.join(os.path.dirname(__file__), "config", "core_targets.json")
    
    if not os.path.exists(config_path):
        print(f"❌ Core targets not found at {config_path}")
        return []
    
    with open(config_path, "r", encoding="utf-8") as f:
        targets = json.load(f)
    
    print(f"🎯 Loaded {len(targets)} core websites for monitoring:")
    for i, target in enumerate(targets, 1):
        print(f"   {i}. {target['url']} ({target['project']})")
    
    return targets

def create_project_config(target, project_dir):
    """Creates a config.json for a core target"""
    os.makedirs(project_dir, exist_ok=True)
    
    config = {
        "project_name": target["project"],
        "target_url": target["url"],
        "workflow_description": target["goal"],
        "domain": target.get("domain", "general_web"),
        "testing_type": "smoke",
        "paths": {
            "trace": os.path.join(project_dir, "outputs", "trace.json"),
            "test": os.path.join(project_dir, "tests", "test_main.py"),
            "report": os.path.join(project_dir, "outputs", "report.md")
        },
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "is_core": True
        }
    }
    
    config_path = os.path.join(project_dir, "config.json")
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    
    return config_path

def sync_to_github():
    """ Robustly syncs results and learnings to GitHub """
    print("\n" + "="*80)
    print("🔄 SYNCING RESULTS TO GITHUB (CORE MONITOR)")
    print("="*80)
    
    commands = [
        ["git", "config", "--global", "user.name", "Antigravity Core Monitor"],
        ["git", "config", "--global", "user.email", "core-monitor@antigravity.ai"],
        ["git", "stash"], 
        ["git", "pull", "--rebase", "origin", "main"],
        ["git", "stash", "pop"], 
        ["git", "add", "knowledge/", "outputs/", "projects/", "config/core_targets.json"],
        ["git", "commit", "-m", "Core Monitoring Update: Knowledge & Results [skip ci]"],
        ["git", "push", "origin", "main"]
    ]

    for cmd in commands:
        try:
            if "stash" in cmd and "pop" in cmd:
                subprocess.run(cmd, check=False, capture_output=True)
                continue
            print(f"Exec: {' '.join(cmd)}")
            subprocess.run(cmd, check=True, capture_output=False)
        except subprocess.CalledProcessError as e:
            if "nothing to commit" in str(e) or "clean" in str(e):
                print("✅ Nothing to commit.")
                return
            print(f"⚠️ Git Command Failed: {e}")
            if "pull" in cmd:
                 print("❌ Pull failed. Aborting sync.")
                 return

    print("✅ Sync Complete.")

def run_core_monitor(sync_git=False, dry_run=False):
    """Main runner for core monitoring"""
    print("="*80)
    print("🚀 CORE MONITORING SYSTEM")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    targets = load_core_targets()
    
    if not targets:
        return
    
    if dry_run:
        print("🧪 Dry run enabled. Configs created, but no exploration will run.")
    
    # Create configs
    config_paths = []
    for target in targets:
        project_dir = os.path.join("projects", target["project"])
        config_path = create_project_config(target, project_dir)
        config_paths.append(config_path)

    if dry_run:
        return

    # Run in Parallel
    print(f"\n🚀 Launching Core Monitoring for {len(config_paths)} sites...")
    failures = []
    
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), "core"))
        from batch_orchestrator import BatchOrchestrator
        import asyncio
        
        orchestrator = BatchOrchestrator(concurrency_limit=5)
        asyncio.run(orchestrator.run_batch(config_paths, headed=False))
        
        # Detect Failures
        failures = [p for p, res in orchestrator.results.items() if res.get('status') != 'success']
        
        # Aggregate dashboard
        print("\n📊 Aggregating Global Dashboard...")
        subprocess.run([sys.executable, "core/dashboard_aggregator.py"], check=False)
            
    except Exception as e:
        print(f"❌ Core Monitor Batch Failed: {e}")
        # If the batch system itself crashed, we definitely failed
        sys.exit(1)
    
    if sync_git:
        sync_to_github()

    if failures:
        print(f"\n❌ MONITOR FAILED: {len(failures)} projects failed: {', '.join(failures)}")
        sys.exit(1)

if __name__ == "__main__":
    should_sync = "--sync-git" in sys.argv
    is_dry = "--dry-run" in sys.argv
    run_core_monitor(sync_git=should_sync, dry_run=is_dry)
