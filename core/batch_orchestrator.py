import asyncio
import json
import os
import sys
import time
from termcolor import colored

# Ensure local modules are importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.orchestrator import run_pipeline

class BatchOrchestrator:
    def __init__(self, concurrency_limit=3):
        self.semaphore = asyncio.Semaphore(concurrency_limit)
        self.results = {}

    async def run_project(self, config_path, headed=False):
        """Runs a single project pipeline with concurrency control."""
        async with self.semaphore:
            project_name = os.path.basename(os.path.dirname(config_path))
            print(colored(f"🧵 Starting parallel run for: {project_name}", "blue"))
            
            start_time = time.time()
            try:
                # Since run_pipeline is synchronous and blocks, we run it in a thread
                # to allow other async tasks to proceed.
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, run_pipeline, config_path, headed)
                
                duration = time.time() - start_time
                self.results[project_name] = {"status": "success", "duration": round(duration, 2)}
                print(colored(f"✅ Finished parallel run for: {project_name} ({round(duration, 2)}s)", "green"))
            except Exception as e:
                duration = time.time() - start_time
                self.results[project_name] = {"status": "failed", "error": str(e), "duration": round(duration, 2)}
                print(colored(f"❌ Failed parallel run for: {project_name}: {e}", "red"))

    async def run_batch(self, config_paths, headed=False):
        """Runs a batch of projects in parallel."""
        print(colored(f"🚀 Starting Batch Run of {len(config_paths)} projects (Concurrency: {self.semaphore._value})...", "cyan", attrs=["bold"]))
        
        tasks = [self.run_project(cp, headed) for cp in config_paths]
        await asyncio.gather(*tasks)
        
        print(colored("\n🏁 Batch Run Complete!", "cyan", attrs=["bold"]))
        self._print_summary()

    def _print_summary(self):
        print("\n" + "="*40)
        print("SUMMARY")
        print("="*40)
        for project, res in self.results.items():
            status = colored(res['status'].upper(), "green" if res['status'] == "success" else "red")
            print(f"{project:30} | {status} | {res['duration']}s")
        print("="*40)

if __name__ == "__main__":
    # Example usage: python core/batch_orchestrator.py projects/p1/config.json projects/p2/config.json --concurrency 3
    import argparse
    parser = argparse.ArgumentParser(description="Run multiple projects in parallel.")
    parser.add_argument("configs", nargs="+", help="Paths to config.json files")
    parser.add_argument("--concurrency", type=int, default=3, help="Max parallel runs")
    parser.add_argument("--headed", action="store_true", help="Run headed")
    
    # Fix for argparse with --concurrency typo in implementation_plan if I made any
    args = parser.parse_args()
    
    orchestrator = BatchOrchestrator(concurrency_limit=args.concurrency)
    asyncio.run(orchestrator.run_batch(args.configs, headed=args.headed))
