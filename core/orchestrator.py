import sys
import json
import subprocess
import os
import time
from termcolor import colored
import hashlib

# Force UTF-8 for console output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Import Metrics Logger
try:
    from .metrics_logger import logger
except ImportError:
    from metrics_logger import logger

CHECKPOINT_FILE = ".checkpoint.json"

def get_checkpoint_path(project_root):
    return os.path.join(project_root, CHECKPOINT_FILE)

def _get_config_hash(config):
    """Generates a stable hash of the configuration."""
    subset = {
        "url": config.get("target_url"),
        "goal": config.get("workflow_description") or config.get("goal"),
        "domain": config.get("domain")
    }
    s = json.dumps(subset, sort_keys=True)
    return hashlib.md5(s.encode()).hexdigest()

def save_checkpoint(project_root, phase, config_hash=None, data=None):
    """Save a phase as complete."""
    path = get_checkpoint_path(project_root)
    checkpoints = {}
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                checkpoints = json.load(f)
        except: pass
    
    checkpoints[phase] = {
        "status": "complete",
        "timestamp": time.time(),
        "config_hash": config_hash,
        "data": data or {}
    }
    
    try:
        with open(path, "w") as f:
            json.dump(checkpoints, f, indent=2)
            print(colored(f"💾 Checkpoint saved: {phase}", "grey"))
    except Exception as e:
        print(colored(f"⚠️ Failed to save checkpoint: {e}", "yellow"))

def can_skip_phase(project_root, phase, current_config_hash=None, ttl_seconds=7200): # 2 hours TTL
    """Check if phase can be skipped."""
    path = get_checkpoint_path(project_root)
    if not os.path.exists(path):
        return False
        
    try:
        with open(path, "r") as f:
            checkpoints = json.load(f)
        
        if phase in checkpoints:
            cp = checkpoints[phase]
            if time.time() - cp["timestamp"] > ttl_seconds:
                return False
            if current_config_hash and cp.get("config_hash") != current_config_hash:
                print(colored(f"🔄 Config changed. Invalidating checkpoint for {phase}.", "yellow"))
                return False
            return True
    except:
        return False
    return False

def _log_error(config, phase, error_msg):
    try:
        sys.path.append(os.path.dirname(__file__))
        from feedback_agent import FeedbackAgent
        context = {
            "site": config.get("target_url"),
            "project": config.get("project_name"),
            "phase": phase
        }
        FeedbackAgent().log_failure(context, error_msg)
    except Exception as e:
        print(colored(f"⚠️ Failed to log error: {e}", "yellow"))

# --- PHASES ---

def _run_planning(project_root, config, config_hash, config_path):
    print(colored("\n[Step 0/7] 📋 Strategic Test Planning...", "cyan"))
    if can_skip_phase(project_root, "planning", config_hash):
        print(colored("⏩ Skipping Planning (Checkpoint found)", "grey"))
        return True

    for attempt in range(1, 4):
        try:
            sys.path.append(os.path.dirname(__file__))
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
                save_checkpoint(project_root, "planning", config_hash)
                return True
            else:
                raise Exception("Plan generation returned empty")
        except Exception as e:
            logger.log_failure("SpecSynthesizer", str(e), {"attempt": attempt, "config": config_path})
            print(colored(f"⚠️ Pre-Planning Attempt {attempt} Failed: {e}", "yellow"))
            if attempt == 3:
                _log_error(config, "planning", str(e))
                return False
    return False

def _run_exploration(project_root, config, config_hash, config_path, headed=False):
    print(colored("\n[Step 1/7] 🗺️  Exploring & Mining (Plan-Guided)...", "cyan"))
    trace_path = config.get("paths", {}).get("trace", os.path.join(project_root, "outputs/trace.json"))
    
    if can_skip_phase(project_root, "exploration", config_hash):
        print(colored("⏩ Skipping Exploration (Checkpoint found)", "grey"))
        return True

    for attempt in range(1, 4):
        start_time = time.time()
        explorer_script = os.path.join(os.path.dirname(__file__), "explorer.py")
        cmd = ["python", explorer_script, config_path]
        if headed: cmd.append("--headed")
        
        env = os.environ.copy()
        env["PYTHONPATH"] = os.getcwd()
        ret = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore', env=env)
        
        if ret.returncode == 0:
            duration = time.time() - start_time
            logger.log_event("Explorer", "exploration_phase", duration, success=True)
            save_checkpoint(project_root, "exploration", config_hash)
            return True
        else:
            error_context = {"attempt": attempt, "stdout": (ret.stdout or "")[:200], "stderr": (ret.stderr or "")[:500]}
            logger.log_failure("Explorer", f"Exit code {ret.returncode}", error_context)
            print(colored(f"⚠️ Exploration Attempt {attempt} Failed. Retrying...", "yellow"))
    
    # Fallback
    print(colored("⚠️ Exploration Failed. Triggering Fallback: Generating Basic Test from User Goal...", "yellow"))
    fake_trace = {
        "workflow": config.get("workflow_description"),
        "trace": [{"step": 1, "url": config.get("target_url"), "action": "navigate", "decision_reason": "Fallback", "locator_used": None, "success": True}]
    }
    os.makedirs(os.path.dirname(trace_path), exist_ok=True)
    with open(trace_path, "w") as f:
        json.dump(fake_trace, f, indent=2)
    save_checkpoint(project_root, "exploration", config_hash)
    
    if not os.path.exists(trace_path):
        print(colored("❌ No Trace File Found after Exploration!", "red"))
        _log_error(config, "exploration", "No Trace File Generated")
        return False
    return True

def _run_knowledge_update(project_root, config, config_hash, trace_path):
    print(colored("\n[Step 2/7] Updating Knowledge Bank...", "cyan"))
    if can_skip_phase(project_root, "knowledge_update", config_hash):
        print(colored("⏩ Skipping Knowledge Update (Checkpoint found)", "grey"))
        return

    try:
        sys.path.append(os.path.dirname(__file__))
        from knowledge_bank import KnowledgeBank
        kb = KnowledgeBank()
        if os.path.exists(trace_path):
            with open(trace_path, "r") as f:
                trace_data = json.load(f)
                cost = trace_data.get("metadata", {}).get("cost", {})
                if cost:
                    print(colored(f"AI Cost: {cost.get('input', 0)} In / {cost.get('output', 0)} Out Tokens", "yellow"))
                kb.update_from_run(trace_data["trace"], config)
        save_checkpoint(project_root, "knowledge_update", config_hash)
    except Exception as e:
        print(colored(f"Knowledge Update Failed: {e}", "yellow"))

def _run_code_generation(project_root, config, config_hash, trace_path, test_path):
    print(colored("\n[Step 3/7] Generating Robust Code & Logic Check...", "cyan"))
    if can_skip_phase(project_root, "generation", config_hash) and can_skip_phase(project_root, "review", config_hash):
        print(colored("⏩ Skipping Code Generation & Review (Checkpoints found)", "grey"))
        return True

    # Helper for hints
    def get_dynamic_hint(review_msg, attempt_num):
        msg_lower = review_msg.lower()
        hints = []
        if "page." in msg_lower or "self.page" in msg_lower or "scope" in msg_lower:
             hints.append("🔐 **SCOPE ERROR**: Inside POM classes, you MUST use `self.page`, NEVER `page`.")
        if "selector" in msg_lower or "locator" in msg_lower:
            hints.append("📍 **LOCATOR ISSUE**: Follow the cascade: Proven > Role > Label > Text.")
        if not hints:
            if attempt_num == 2: hints.append("💡 HINT: Review the POM structure.")
            if attempt_num >= 4: hints.append("🔥 CRITICAL: Simplify the logic.")
        return "\n".join(hints)

    gen_success = False
    error_context = None
    sys.path.append(os.path.dirname(__file__))
    from reviewer import CodeReviewer

    for attempt in range(1, 6):
        print(colored(f"🔄 Generation Loop {attempt}/5...", "cyan"))
        start_time = time.time()
        refiner_script = os.path.join(os.path.dirname(__file__), "refiner.py")
        domain = config.get("domain", "general")
        
        error_file_arg = ""
        if error_context:
            error_file = os.path.join(project_root, "outputs", "gen_feedback.log")
            with open(error_file, "w", encoding="utf-8") as f: f.write(str(error_context))
            error_file_arg = error_file
            print(colored(f"💡 Feeding Reviewer Feedback to Refiner: {str(error_context)[:100]}...", "yellow"))

        ret = subprocess.run(["python", refiner_script, trace_path, test_path, config.get("workflow_description", ""), error_file_arg, domain], capture_output=False)
        
        if ret.returncode != 0:
            print(colored(f"⚠️ Generation failed (Code {ret.returncode})", "yellow"))
            continue

        try:
            rev = CodeReviewer()
            is_approved, review_msg = rev.review_and_fix(test_path, domain=domain)
            
            if is_approved:
                print(colored("✅ Code Approved by Quality Gate.", "green"))
                gen_success = True
                save_checkpoint(project_root, "generation", config_hash)
                save_checkpoint(project_root, "review", config_hash)
                duration = time.time() - start_time
                logger.log_event("Generator", "full_gen_cycle", duration, success=True, metadata={"loops": attempt})
                break
            else:
                print(colored(f"❌ Quality Gate Rejected Code: {review_msg}", "red"))
                error_context = f"ISSUES:\n{review_msg}\nHINTS:\n{get_dynamic_hint(review_msg, attempt)}"
        except Exception as e:
            print(colored(f"⚠️ Review Process Crashed: {e}", "red"))
            error_context = f"Reviewer Crashed: {e}"

    if not gen_success:
        print(colored("⚠️ All generation attempts exhausted. Creating minimal fallback...", "yellow"))
        try:
            from minimal_template import generate_minimal_smoke_test
            generate_minimal_smoke_test(config, test_path)
            print(colored("✅ Minimal smoke test created as fallback", "green"))
            gen_success = True
            save_checkpoint(project_root, "generation", config_hash)
        except Exception as e:
            print(colored(f"❌ Fallback generation also failed: {e}", "red"))
            _log_error(config, "generation", f"Failed generation: {e}")
            return False
            
    return True

def _run_spec_synthesis(project_root, config, config_hash):
    print(colored("\n[Step 4/7] 🧠 Synthesizing Specs & Features...", "cyan"))
    if can_skip_phase(project_root, "spec_synthesis", config_hash):
        print(colored("⏩ Skipping Spec Synthesis (Checkpoint found)", "grey"))
        return

    try:
        from spec_synthesizer import SpecSynthesizer
        domain = config.get("domain", "generic")
        syn = SpecSynthesizer(project_root, domain)
        syn.generate_specs()
        save_checkpoint(project_root, "spec_synthesis", config_hash)
    except Exception as e:
        print(colored(f"⚠️ Spec Synthesis Failed: {e}", "yellow"))

def _run_reporting(project_root, config, config_hash, trace_path):
    print(colored("\n[Step 5/7] 📝 Creating Exploration Report...", "cyan"))
    if can_skip_phase(project_root, "reporting", config_hash):
        print(colored("⏩ Skipping Reporting (Checkpoint found)", "grey"))
        return

    report_path = config.get("paths", {}).get("report", os.path.join(project_root, "outputs/report.md"))
    reporter_script = os.path.join(os.path.dirname(__file__), "reporter.py")
    subprocess.run(["python", reporter_script, trace_path, report_path], capture_output=False)
    save_checkpoint(project_root, "reporting", config_hash)

def _run_execution(project_root, config, config_hash, test_path, trace_path):
    print(colored("\n[Step 6/7] 🧪 Executing Verified Test...", "cyan"))
    execution_log = ""
    
    if can_skip_phase(project_root, "execution", config_hash):
        print(colored("⏩ Skipping Test Execution (Checkpoint found)", "grey"))
        execution_log = "Execution skipped (Checkpoint found)."
        return True, execution_log

    max_retries = 3
    success = False
    
    for attempt in range(max_retries):
        print(f"Attempt {attempt + 1}/{max_retries}...")
        start_time = time.time()
        
        # Prepare Environment with PYTHONPATH
        env = os.environ.copy()
        env["PYTHONPATH"] = os.getcwd() # Ensure 'core' is importable from root

        ret = subprocess.run(["pytest", test_path, "-v", "-s"], capture_output=True, text=True, encoding='utf-8', errors='replace', env=env)
        current_log = (ret.stdout or "") + "\n" + (ret.stderr or "")
        execution_log += f"--- Attempt {attempt + 1} ---\n{current_log}\n"
        print(current_log)
        
        if ret.returncode == 0:
            print(colored("\n✅ Test Execution SUCCESS!", "green", attrs=["bold"]))
            success = True
            duration = time.time() - start_time
            logger.log_event("Executor", "execute_test", duration, success=True, metadata={"attempt": attempt + 1})
            save_checkpoint(project_root, "execution", config_hash)
            break
        else:
            if attempt < max_retries - 1:
                print(colored(f"⚠️ Attempt {attempt + 1} Failed. Triggering Self-Healing...", "yellow"))
                error_file = os.path.join(project_root, "outputs", "execution_error.log")
                with open(error_file, "w", encoding="utf-8") as f: f.write(current_log)
                
                refiner_script = os.path.join(os.path.dirname(__file__), "refiner.py")
                domain = config.get("domain", "general")
                subprocess.run(["python", refiner_script, trace_path, test_path, config.get("workflow_description", ""), error_file, domain])
            else:
                print(colored(f"❌ Final Attempt {attempt + 1} Failed.", "red"))

    if not success:
        print(colored("\n❌ All test attempts failed!", "red", attrs=["bold"]))
        _log_error(config, "execution", execution_log[-1000:])
        
    return success, execution_log

def _run_validation(project_root, config, success):
    if success:
        print(colored("\n[Step 6.2] 🕵️ Validating Business Goal Achievement...", "cyan"))
        try:
            from validator import BusinessValidator
            validator = BusinessValidator()
            
            # Find newest screenshot
            screenshot_path = None
            screenshots_dir = os.path.join(project_root, "outputs", "screenshots")
            if os.path.exists(screenshots_dir):
                files = [os.path.join(screenshots_dir, f) for f in os.listdir(screenshots_dir) if f.endswith(".png")]
                if files: screenshot_path = max(files, key=os.path.getctime)
            
            trace_path = os.path.join(project_root, "outputs/trace.json")
            goal = config.get("goal") or config.get("workflow_description", "Unknown Goal")
            
            result = validator.validate_goal_completion(goal, trace_path, screenshot_path)
            
            if result.get("status") == "FAIL":
                print(colored(f"⚠️ TEST PASSED BUT GOAL FAILED: {result.get('reason')}", "red", attrs=["bold"]))
                logger.log_event("Validator", "validate_goal", None, success=False, metadata=result)
            else:
                print(colored(f"✅ GOAL VERIFIED: {result.get('reason')}", "green"))
                logger.log_event("Validator", "validate_goal", None, success=True, metadata=result)
        except Exception as e:
            print(colored(f"⚠️ Validation Skipped: {e}", "yellow"))

def _run_feedback(config_path, execution_log, success):
    print(colored("\n[Step 6.5] 🧠 Feedback & Self-Training...", "cyan"))
    try:
        from feedback_agent import FeedbackAgent
        feedback = FeedbackAgent()
        feedback.analyze_run(config_path, execution_log, success)
    except Exception as e:
        print(colored(f"⚠️ Feedback Loop Failed: {e}", "yellow"))

def _run_security_audit(project_root, config, config_hash):
    if "security check" in config.get("workflow_description", "").lower():
        print(colored("\n[Step 7/7] 🛡️  Running Security Audit...", "cyan"))
        if can_skip_phase(project_root, "security", config_hash):
            print(colored("⏩ Skipping Security Audit (Checkpoint found)", "grey"))
        else:
            try:
                from security_auditor import SecurityAuditor
                auditor = SecurityAuditor(config.get("target_url"), project_root)
                auditor.run_all_checks()
                save_checkpoint(project_root, "security", config_hash)
            except Exception as e:
                print(colored(f"⚠️ Security Audit Failed: {e}", "yellow"))
    else:
        print(colored("\n[Step 7/7] 🛡️  Security Audit skipped (not requested).", "white"))

def _run_dashboard(project_root, config_hash):
    try:
        dashboard_script = os.path.join(os.path.dirname(__file__), "dashboard_generator.py")
        metrics_source = os.path.join("outputs", "metrics.json")
        dashboard_target = os.path.join(project_root, "outputs", "dashboard.html")
        ret = subprocess.run(["python", dashboard_script, metrics_source, dashboard_target], capture_output=False) 
        if ret.returncode == 0:
            print(colored(f"✅ Web Dashboard ready: {dashboard_target}", "green"))
    except Exception as e:
        print(colored(f"⚠️ Dashboard Generation Failed: {e}", "yellow"))
    save_checkpoint(project_root, "dashboard", config_hash)

# --- WORKFLOW ---

def run_pipeline(config_path, headed=False):
    print(colored(f"🚀 Starting Autonomous Pipeline for {os.path.basename(os.path.dirname(config_path))}...", "green", attrs=["bold"]))
    
    with open(config_path, "r") as f:
        config = json.load(f)
        
    config_hash = _get_config_hash(config)
    project_root = os.path.dirname(config_path)
    trace_path = config.get("paths", {}).get("trace", os.path.join(project_root, "outputs/trace.json"))
    test_path = config.get("paths", {}).get("test", os.path.join(project_root, "tests/test_main.py"))

    # Execute Phases
    if not _run_planning(project_root, config, config_hash, config_path): return
    if not _run_exploration(project_root, config, config_hash, config_path, headed): return
    _run_knowledge_update(project_root, config, config_hash, trace_path)
    if not _run_code_generation(project_root, config, config_hash, trace_path, test_path): return
    _run_spec_synthesis(project_root, config, config_hash)
    _run_reporting(project_root, config, config_hash, trace_path)
    
    success, execution_log = _run_execution(project_root, config, config_hash, test_path, trace_path)
    
    _run_validation(project_root, config, success)
    _run_feedback(config_path, execution_log, success)
    _run_security_audit(project_root, config, config_hash)
    _run_dashboard(project_root, config_hash)

    if success:
        print(colored("\n✅ Pipeline COMPLETE!", "green", attrs=["bold"]))
    else:
        print(colored("\n⚠️ Pipeline ended with test failures.", "yellow"))
    
    return success

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python core/orchestrator.py <config_path> [--headed]")
        sys.exit(1)
        
    config_path = sys.argv[1]
    headed = "--headed" in sys.argv
    
    run_pipeline(config_path, headed=headed)
