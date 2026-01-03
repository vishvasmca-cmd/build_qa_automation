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

    # Phase 0: Pre-Run Test Planning (REAL WORLD FIRST)
    print(colored("\n[Step 0/7] 📋 Strategic Test Planning...", "cyan"))
    try:
        from spec_synthesizer import SpecSynthesizer
        domain = config.get("domain", "generic")
        syn = SpecSynthesizer(project_root, domain)
        plan = syn.generate_master_plan(
            url=config.get("target_url"),
            testing_type=config.get("testing_type", "regression"),
            goal=config.get("workflow_description")
        )
        if plan:
            config["master_plan"] = plan
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)
    except Exception as e:
        print(colored(f"⚠️ Pre-Planning Failed: {e}", "yellow"))

    # Step 1: Explorer (Guided by the Plan)
    print(colored("\n[Step 1/7] 🗺️  Exploring & Mining (Plan-Guided)...", "cyan"))
    # We pass the config path to explorer
    explorer_script = os.path.join(os.path.dirname(__file__), "explorer.py")
    ret = subprocess.run(["python", explorer_script, config_path], capture_output=False)
    
    if ret.returncode != 0:
        print(colored("❌ Explorer Agent Failed / Crashed!", "red"))
        print(colored("⚠️ Triggering Fallback: Generating Basic Test from User Goal...", "yellow"))
        
        # FALLBACK: Create a dummy trace so Refiner can still generate valid code
        fake_trace = {
            "workflow": config.get("workflow_description"),
            "trace": [
                {
                    "step": 1,
                    "url": config.get("target_url"),
                    "action": "navigate", 
                    "decision_reason": "Fallback: Navigating to target.",
                    "locator_used": None,
                    "success": True
                },
                {
                    "step": 2, 
                    "url": config.get("target_url"),
                    "action": "check",
                    "decision_reason": "Fallback: Checking if page loaded and contains goal keywords.",
                    "locator_used": "body",
                    "success": True
                }
            ]
        }
        with open(trace_path, "w") as f:
            json.dump(fake_trace, f, indent=2)
            
    if not os.path.exists(trace_path):
        print(colored("❌ Critical: No trace available even after fallback. Aborting.", "red"))
        return

    # Step 2: Knowledge Update (RAG-Ready)
    print(colored("\n[Step 2/7] 📖 Updating Knowledge Bank...", "cyan"))
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
    print(colored("\n[Step 3/7] 💻 Generating Robust Code...", "cyan"))
    refiner_script = os.path.join(os.path.dirname(__file__), "refiner.py")
    ret = subprocess.run(["python", refiner_script, trace_path, test_path], capture_output=False)
    if ret.returncode != 0:
        print(colored("❌ Code Generation Failed!", "red"))
        return

    # Step 3.5: AI Code Review (Quality Gate)
    print(colored("\n[Step 3.5] 🕵️  Code Review & Quality Gate...", "cyan"))
    reviewer_script = os.path.join(os.path.dirname(__file__), "reviewer.py")
    ret = subprocess.run(["python", reviewer_script, test_path], capture_output=False)
    if ret.returncode != 0:
         print(colored("⚠️ Reviewer Failed (Continuing with original code)...", "yellow"))

    # Step 4: Intelligent Spec Synthesis
    print(colored("\n[Step 4/7] 🧠 Synthesizing Specs & Features...", "cyan"))
    try:
        from spec_synthesizer import SpecSynthesizer
        domain = config.get("domain", "generic")
        syn = SpecSynthesizer(project_root, domain)
        syn.generate_specs()
    except Exception as e:
        print(colored(f"⚠️ Spec Synthesis Failed: {e}", "yellow"))

    # Step 5: Final Report
    print(colored("\n[Step 5/7] 📝 Creating Exploration Report...", "cyan"))
    report_path = config.get("paths", {}).get("report", os.path.join(project_root, "outputs/report.md"))
    reporter_script = os.path.join(os.path.dirname(__file__), "reporter.py")
    ret = subprocess.run(["python", reporter_script, trace_path, report_path], capture_output=False)

    # Step 6: Execution (With Retry)
    print(colored("\n[Step 6/7] 🧪 Executing Verified Test...", "cyan"))
    max_retries = 2
    success = False
    execution_log = ""
    
    for attempt in range(max_retries):
        print(f"Attempt {attempt + 1}/{max_retries}...")
        # Capture output for the Feedback Agent
        ret = subprocess.run(["pytest", test_path, "-v"], capture_output=True, text=True)
        execution_log = ret.stdout + "\n" + ret.stderr
        print(execution_log) # Show to user as well
        
        if ret.returncode == 0:
            print(colored("\n✅ Test Execution SUCCESS!", "green", attrs=["bold"]))
            success = True
            break
        print(colored(f"⚠️ Attempt {attempt + 1} Failed. Retrying...", "yellow"))

    if not success:
        print(colored("\n❌ All test attempts failed!", "red", attrs=["bold"]))

    # Step 6.5: Feedback & Self-Training
    print(colored("\n[Step 6.5] 🧠 Feedback & Self-Training...", "cyan"))
    try:
        from feedback_agent import FeedbackAgent
        feedback = FeedbackAgent()
        feedback.analyze_run(config_path, execution_log, success)
    except Exception as e:
        print(colored(f"⚠️ Feedback Loop Failed: {e}", "yellow"))

    # Step 7: Security Audit (Conditional)
    if "security check" in config.get("workflow_description", "").lower():
        print(colored("\n[Step 7/7] 🛡️  Running Security Audit...", "cyan"))
        try:
            from security_auditor import SecurityAuditor
            auditor = SecurityAuditor(config.get("target_url"), project_root)
            auditor.run_all_checks()
        except Exception as e:
            print(colored(f"⚠️ Security Audit Failed: {e}", "yellow"))
    else:
        print(colored("\n[Step 7/7] 🛡️  Security Audit skipped (not requested).", "white"))

    # Step 8: Premium Web Dashboard
    print(colored("\n[Step 8] 🚀 Generating Premium Web Dashboard...", "cyan"))
    try:
        dashboard_script = os.path.join(os.path.dirname(__file__), "generator_dashboard.py")
        ret = subprocess.run(["python", dashboard_script, project_root, str(success)], capture_output=False)
        if ret.returncode == 0:
            print(colored(f"✅ Web Dashboard ready: {os.path.join(project_root, 'outputs/dashboard.html')}", "green"))
    except Exception as e:
        print(colored(f"⚠️ Dashboard Generation Failed: {e}", "yellow"))

    if success:
        print(colored("\n✅ Pipeline COMPLETE!", "green", attrs=["bold"]))
    else:
        print(colored("\n⚠️ Pipeline ended with test failures.", "yellow"))
