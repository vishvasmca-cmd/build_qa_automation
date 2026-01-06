import sys
import json
import os
import random
import subprocess
import time
from datetime import datetime

# UTF-8 fix
try:
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

def select_random_websites(count=20):
    """Selects random websites from training_targets.json"""
    config_path = os.path.join(os.path.dirname(__file__), "config", "training_targets.json")
    
    if not os.path.exists(config_path):
        print(f"❌ Training targets not found at {config_path}")
        return []
    
    with open(config_path, "r", encoding="utf-8") as f:
        all_targets = json.load(f)
    
    # Select random subset
    selected = random.sample(all_targets, min(count, len(all_targets)))
    
    print(f"🎯 Selected {len(selected)} websites for exploration:")
    for i, target in enumerate(selected, 1):
        print(f"   {i}. {target['url']} (Rank: {target.get('rank', 'N/A')})")
    
    return selected

def create_project_config(target, project_dir):
    """Creates a config.json for a training target"""
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
            "rank": target.get("rank", "Unknown")
        }
    }
    
    config_path = os.path.join(project_dir, "config.json")
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    
    return config_path

def run_exploration_batch():
    """Main runner for continuous exploration"""
    print("="*80)
    print("🚀 CONTINUOUS EXPLORATION & LEARNING BATCH")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    # Select 20 random websites
    targets = select_random_websites(20)
    
    if not targets:
        print("❌ No targets selected. Exiting.")
        return
    
    results = []
    
    for idx, target in enumerate(targets, 1):
        print(f"\n{'='*80}")
        print(f"📌 [{idx}/{len(targets)}] Exploring: {target['url']}")
        print(f"{'='*80}")
        
        project_name = target["project"]
        project_dir = os.path.join("projects", project_name)
        
        # Create project config
        config_path = create_project_config(target, project_dir)
        
        # Run the pipeline
        start_time = time.time()
        
        cmd = ["python", "trigger_agent.py", config_path, "--headless"]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
        
        duration = time.time() - start_time
        success = result.returncode == 0
        
        results.append({
            "project": project_name,
            "url": target["url"],
            "rank": target.get("rank"),
            "success": success,
            "duration": round(duration, 2),
            "timestamp": datetime.now().isoformat()
        })
        
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"\n{status} - Completed in {duration:.1f}s")
    
    # Save batch summary
    summary_path = os.path.join("outputs", f"batch_summary_{int(time.time())}.json")
    os.makedirs("outputs", exist_ok=True)
    
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump({
            "batch_time": datetime.now().isoformat(),
            "total_explored": len(targets),
            "passed": sum(1 for r in results if r["success"]),
            "failed": sum(1 for r in results if not r["success"]),
            "results": results
        }, f, indent=2)
    
    print(f"\n{'='*80}")
    print("📊 BATCH COMPLETE")
    print(f"✅ Passed: {sum(1 for r in results if r['success'])}/{len(results)}")
    print(f"❌ Failed: {sum(1 for r in results if not r['success'])}/{len(results)}")
    print(f"💾 Summary saved to: {summary_path}")
    print(f"{'='*80}")

if __name__ == "__main__":
    run_exploration_batch()
