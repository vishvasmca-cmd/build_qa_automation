import sys
import json
import subprocess
import os
from termcolor import colored

def run_pipeline(config_path):
    print(colored(f"🚀 Starting Autonomous Pipeline for {os.path.basename(os.path.dirname(config_path))}...", "green", attrs=["bold"]))
    
    with open(config_path, "r") as f:
        config = json.load(f)
    
    # Paths
    project_root = os.path.dirname(config_path)
    trace_path = config.get("paths", {}).get("trace", os.path.join(project_root, "outputs/trace.json"))
    test_path = config.get("paths", {}).get("test", os.path.join(project_root, "tests/test_main.py"))

    # Step 1: Explorer
    print(colored("\n[Step 1/6] 🗺️  Exploring & Mining...", "cyan"))
    # We pass the config path to explorer
    explorer_script = os.path.join(os.path.dirname(__file__), "explorer.py")
    ret = subprocess.run(["python", explorer_script, config_path], capture_output=False)
    if ret.returncode != 0:
        print(colored("❌ Exploration Failed!", "red"))
        return

    # Step 2: Knowledge Update (RAG-Ready)
    print(colored("\n[Step 2/6] 📖 Updating Knowledge Bank...", "cyan"))
    try:
        sys.path.append(os.path.dirname(__file__))
        from knowledge_bank import KnowledgeBank
        kb = KnowledgeBank()
        if os.path.exists(trace_path):
            with open(trace_path, "r") as f:
                trace_data = json.load(f)
                
                # Report Cost
                cost = trace_data.get("metadata", {}).get("cost", {})
                if cost:
                    # Input/Output tokens
                    print(colored(f"💰 AI Cost: {cost.get('input', 0)} In / {cost.get('output', 0)} Out Tokens", "yellow"))

                kb.update_from_run(trace_data["trace"], config)
    except Exception as e:
        print(colored(f"⚠️ Knowledge Update Failed: {e}", "yellow"))

    # Step 3: Code Generation
    print(colored("\n[Step 3/6] 💻 Generating Robust Code...", "cyan"))
    refiner_script = os.path.join(os.path.dirname(__file__), "refiner.py")
    ret = subprocess.run(["python", refiner_script, trace_path, test_path], capture_output=False)
    if ret.returncode != 0:
        print(colored("❌ Code Generation Failed!", "red"))
        return

    # Step 4: Intelligent Spec Synthesis
    print(colored("\n[Step 4/6] 🧠 Synthesizing Specs & Features...", "cyan"))
    try:
        from spec_synthesizer import SpecSynthesizer
        domain = config.get("domain", "generic")
        syn = SpecSynthesizer(project_root, domain)
        syn.generate_specs()
    except Exception as e:
        print(colored(f"⚠️ Spec Synthesis Failed: {e}", "yellow"))

    # Step 5: Final Report
    print(colored("\n[Step 5/6] 📝 Creating Exploration Report...", "cyan"))
    report_path = config.get("paths", {}).get("report", os.path.join(project_root, "outputs/report.md"))
    reporter_script = os.path.join(os.path.dirname(__file__), "reporter.py")
    ret = subprocess.run(["python", reporter_script, trace_path, report_path], capture_output=False)

    # Step 6: Execution (With Retry)
    print(colored("\n[Step 6/6] 🧪 Executing Verified Test...", "cyan"))
    max_retries = 2
    for attempt in range(max_retries):
        print(f"Attempt {attempt + 1}/{max_retries}...")
        ret = subprocess.run(["pytest", test_path, "-v"], capture_output=False)
        if ret.returncode == 0:
            print(colored("\n✅ Pipeline SUCCESS!", "green", attrs=["bold"]))
            return
        print(colored(f"⚠️ Attempt {attempt + 1} Failed. Retrying...", "yellow"))

    print(colored("\n❌ All test attempts failed!", "red", attrs=["bold"]))
