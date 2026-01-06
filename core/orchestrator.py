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
    # We only care about fields that affect logic (goal, URL). 
    # Timestamps or ephemeral paths should be excluded if they change per run.
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
            # Check TTL
            if time.time() - cp["timestamp"] > ttl_seconds:
                return False
                
            # Check Config Hash (Robustness)
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

def run_pipeline(config_path, headed=False):
    print(colored(f"🚀 Starting Autonomous Pipeline for {os.path.basename(os.path.dirname(config_path))}...", "green", attrs=["bold"]))
    
    with open(config_path, "r") as f:
        config = json.load(f)
        
    # Calculate Config Hash for Checkpointing
    config_hash = _get_config_hash(config)
    
    # Paths
    project_root = os.path.dirname(config_path)
    trace_path = config.get("paths", {}).get("trace", os.path.join(project_root, "outputs/trace.json"))
    test_path = config.get("paths", {}).get("test", os.path.join(project_root, "tests/test_main.py"))

    # Phase 0: Pre-Run Test Planning (REAL WORLD FIRST)
    print(colored("\n[Step 0/7] 📋 Strategic Test Planning...", "cyan"))
    if can_skip_phase(project_root, "planning", config_hash):
        print(colored("⏩ Skipping Planning (Checkpoint found)", "grey"))
    else:
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
                    break 
                else:
                    raise Exception("Plan generation returned empty")
            except Exception as e:
                logger.log_failure("SpecSynthesizer", str(e), {"attempt": attempt, "config": config_path})
                print(colored(f"⚠️ Pre-Planning Attempt {attempt} Failed: {e}", "yellow"))
                if attempt == 3:
                    _log_error(config, "planning", str(e))
                    return # Stop pipeline if planning fails after 3 tries

    # Step 1: Explorer (Guided by the Plan)
    print(colored("\n[Step 1/7] 🗺️  Exploring & Mining (Plan-Guided)...", "cyan"))
    if can_skip_phase(project_root, "exploration", config_hash):
        print(colored("⏩ Skipping Exploration (Checkpoint found)", "grey"))
    else:
        for attempt in range(1, 4):
            start_time = time.time()
            # We pass the config path to explorer
            explorer_script = os.path.join(os.path.dirname(__file__), "explorer.py")
            cmd = ["python", explorer_script, config_path]
            if headed:
                cmd.append("--headed")
            
            env = os.environ.copy()
            env["PYTHONPATH"] = os.getcwd() # Ensure roots are visible
            ret = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore', env=env)
            
            if ret.returncode == 0:
                duration = time.time() - start_time
                logger.log_event("Explorer", "exploration_phase", duration, success=True)
                save_checkpoint(project_root, "exploration", config_hash)
                break
            else:
                error_context = {
                    "attempt": attempt, 
                    "stdout": (ret.stdout or "")[:200],
                    "stderr": (ret.stderr or "")[:500]
                }
                logger.log_failure("Explorer", f"Exit code {ret.returncode}", error_context)
                print(colored(f"⚠️ Exploration Attempt {attempt} Failed. Retrying...", "yellow"))
                if attempt == 3:
                    _log_error(config, "exploration", "Explorer failed after 3 attempts")
                    return
        if ret.returncode != 0:
            # Fallback if all retries failed or if it was a fatal crash
            print(colored("⚠️ Exploration Failed. Triggering Fallback: Generating Basic Test from User Goal...", "yellow"))
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
                    }
                ]
            }
            os.makedirs(os.path.dirname(trace_path), exist_ok=True)
            with open(trace_path, "w") as f:
                json.dump(fake_trace, f, indent=2)
            save_checkpoint(project_root, "exploration", config_hash)
        
        if not os.path.exists(trace_path):
            print(colored("❌ No Trace File Found after Exploration!", "red"))
            _log_error(config, "exploration", "No Trace File Generated")
            return

    # Step 2: Knowledge Update (RAG-Ready)
    print(colored("\n[Step 2/7] Updating Knowledge Bank...", "cyan"))
    if can_skip_phase(project_root, "knowledge_update", config_hash):
        print(colored("⏩ Skipping Knowledge Update (Checkpoint found)", "grey"))
    else:
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
                        print(colored(f"AI Cost: {cost.get('input', 0)} In / {cost.get('output', 0)} Out Tokens", "yellow"))

                    kb.update_from_run(trace_data["trace"], config)
            save_checkpoint(project_root, "knowledge_update", config_hash)
        except Exception as e:
            print(colored(f"Knowledge Update Failed: {e}", "yellow"))

    # Step 3: Generating Robust Code
    # Step 3: Generating Robust Code & Logic Check (Unified Loop)
    print(colored("\n[Step 3/7] Generating Robust Code & Logic Check...", "cyan"))
    if can_skip_phase(project_root, "generation", config_hash) and can_skip_phase(project_root, "review", config_hash):
        print(colored("⏩ Skipping Code Generation & Review (Checkpoints found)", "grey"))
    else:
        # Progressive hints to guide LLM through iterations
        REFINEMENT_HINTS = {
            1: "",  # Let it try naturally first
            2: """\nHINT: If the reviewer mentioned 'self.page', remember:
- Inside POM classes, ALWAYS use 'self.page'
- ✅ self.page.get_by_role(...)
- ❌ page.get_by_role(...)""",
            3: """\nHINT: Follow the locator cascade priority:
1. Site-specific proven locators (from knowledge bank)
2. get_by_role() with accessible names
3. get_by_label() / get_by_placeholder()
4. get_by_text()
5. CSS selectors (last resort)""",
            4: """\nSTRONG HINT: The previous error pattern suggests:
- Check for undefined variables (locator, page, etc.)
- Ensure all @property methods return locator objects
- Verify smart_action receives locator objects, not strings""",
            5: """\nCRITICAL - FINAL ATTEMPT:
- Review EVERY line that was flagged as an error
- If stuck on locators, use regex: re.compile(r'text', re.IGNORECASE)
- If stuck on scope, search/replace 'page.' with 'self.page.'
- Simplify: Remove optional assertions if blocking progress"""
        }
        
        def format_enhanced_feedback(review_msg, attempt_num):
            """Formats reviewer feedback with structure and examples"""
            return f"""\n{'='*80}
❌ CODE REJECTED BY QUALITY GATE (Attempt {attempt_num}/5)
{'='*80}

ISSUES FOUND:
{review_msg}

CRITICAL INSTRUCTIONS FOR NEXT ATTEMPT:
1. Read each error above carefully
2. Locate the exact lines in your previous code
3. Apply fixes ONE BY ONE
4. Re-validate after each fix

EXAMPLE OF CORRECT POM PATTERN:
```python
class LoginPage:
    def __init__(self, page):
        self.page = page  # ✅ Store page reference
    
    @property
    def username_field(self):
        return self.page.get_by_label("Username")  # ✅ Use self.page
    
    def login(self, username, password):
        smart_action(self.page, self.username_field, "fill", value=username)  # ✅ Pass locator object
        smart_action(self.page, self.password_field, "fill", value=password)
        smart_action(self.page, self.login_button, "click")
        self.page.wait_for_url("**/dashboard")  # ✅ self.page for navigation
```

{REFINEMENT_HINTS.get(attempt_num + 1, '')}
{'='*80}
"""
        
        # Loop for Generation -> Review -> Regenerate
        gen_success = False
        error_context = None
        
        # Ensure reviewer is importable
        sys.path.append(os.path.dirname(__file__))
        from reviewer import CodeReviewer

        for attempt in range(1, 6):  # Max 5 full loops (increased from 3 for better success rate)
            print(colored(f"🔄 Generation Loop {attempt}/5...", "cyan"))
            
            # 1. Generate (or Regenerate)
            start_time = time.time()
            refiner_script = os.path.join(os.path.dirname(__file__), "refiner.py")
            domain = config.get("domain", "general")
            
            # Write error context to temp file if exists from previous loop
            error_file_arg = ""
            if error_context:
                error_file = os.path.join(project_root, "outputs", "gen_feedback.log")
                with open(error_file, "w", encoding="utf-8") as f:
                    f.write(error_context)
                error_file_arg = error_file
                print(colored(f"💡 Feeding Reviewer Feedback to Refiner: {error_context[:100]}...", "yellow"))

            # Run Refiner
            ret = subprocess.run(
                ["python", refiner_script, trace_path, test_path, config.get("workflow_description", ""), error_file_arg, domain], 
                capture_output=False
            )
            
            if ret.returncode != 0:
                print(colored(f"⚠️ Generation failed (Code {ret.returncode})", "yellow"))
                # If generation script crashes, we retry loop without changing error context? 
                # Or maybe user error? Let's treat as a fail to retry.
                continue

            # 2. Code Review & Logic Gate
            try:
                rev = CodeReviewer()
                is_approved, review_msg = rev.review_and_fix(test_path, domain=domain)
                
                if is_approved:
                    print(colored("✅ Code Approved by Quality Gate.", "green"))
                    gen_success = True
                    save_checkpoint(project_root, "generation", config_hash)
                    save_checkpoint(project_root, "review", config_hash)
                    
                    # Log metrics
                    duration = time.time() - start_time
                    logger.log_event("Generator", "full_gen_cycle", duration, success=True, metadata={"loops": attempt})
                    break
                else:
                    print(colored(f"❌ Quality Gate Rejected Code: {review_msg}", "red"))
                    # Feed enhanced, structured feedback to Refiner in next loop
                    error_context = format_enhanced_feedback(review_msg, attempt)
                    
            except Exception as e:
                print(colored(f"⚠️ Review Process Crashed: {e}", "red"))
                error_context = f"Reviewer Crashed processing your code: {e}"

        if not gen_success:
            # Phase 2: Fallback to minimal template if all attempts fail
            print(colored("⚠️ All generation attempts exhausted. Creating minimal fallback test...", "yellow"))
            try:
                from minimal_template import generate_minimal_smoke_test
                generate_minimal_smoke_test(config, test_path)
                print(colored("✅ Minimal smoke test created as fallback", "green"))
                gen_success = True  # Allow pipeline to continue
                save_checkpoint(project_root, "generation", config_hash)
            except Exception as e:
                print(colored(f"❌ Fallback generation also failed: {e}", "red"))
                _log_error(config, "generation", f"Failed to generate valid code after 5 refinement loops + fallback. Error: {e}")
                return

    # Step 4: Intelligent Spec Synthesis
    print(colored("\n[Step 4/7] 🧠 Synthesizing Specs & Features...", "cyan"))
    if can_skip_phase(project_root, "spec_synthesis", config_hash):
        print(colored("⏩ Skipping Spec Synthesis (Checkpoint found)", "grey"))
    else:
        try:
            from spec_synthesizer import SpecSynthesizer
            domain = config.get("domain", "generic")
            syn = SpecSynthesizer(project_root, domain)
            syn.generate_specs()
            save_checkpoint(project_root, "spec_synthesis", config_hash)
        except Exception as e:
            print(colored(f"⚠️ Spec Synthesis Failed: {e}", "yellow"))

    # Step 5: Final Report
    print(colored("\n[Step 5/7] 📝 Creating Exploration Report...", "cyan"))
    if can_skip_phase(project_root, "reporting", config_hash):
         print(colored("⏩ Skipping Reporting (Checkpoint found)", "grey"))
    else:
        report_path = config.get("paths", {}).get("report", os.path.join(project_root, "outputs/report.md"))
        reporter_script = os.path.join(os.path.dirname(__file__), "reporter.py")
        ret = subprocess.run(["python", reporter_script, trace_path, report_path], capture_output=False)
        save_checkpoint(project_root, "reporting", config_hash)

    # Step 6: Execution (With Retry)
    print(colored("\n[Step 6/7] 🧪 Executing Verified Test...", "cyan"))
    if can_skip_phase(project_root, "execution", config_hash):
        print(colored("⏩ Skipping Test Execution (Checkpoint found)", "grey"))
        success = True # Assume success if checkpoint exists (checkpoints only saved on success)
    else:
        max_retries = 3
        success = False
        execution_log = ""
        
        execution_log = ""
        for attempt in range(max_retries):
            print(f"Attempt {attempt + 1}/{max_retries}...")
            start_time = time.time()
            # Capture output for the Feedback Agent
            # Using -s to capture all stdout/stderr, and -v for verbose
            ret = subprocess.run(["pytest", test_path, "-v", "-s"], capture_output=True, text=True, encoding='utf-8', errors='replace')
            current_log = (ret.stdout or "") + "\n" + (ret.stderr or "")
            execution_log += f"--- Attempt {attempt + 1} ---\n{current_log}\n"
            print(current_log) # Show to user as well
            
            if ret.returncode == 0:
                print(colored("\n✅ Test Execution SUCCESS!", "green", attrs=["bold"]))
                success = True
                duration = time.time() - start_time
                logger.log_event("Executor", "execute_test", duration, success=True, metadata={"attempt": attempt + 1})
                save_checkpoint(project_root, "execution", config_hash)
                break
            else:
                if attempt < max_retries - 1:
                    print(colored(f"⚠️ Attempt {attempt + 1} Failed. Triggering Self-Healing Regeneration...", "yellow"))
                    # Save error to temp file
                    error_file = os.path.join(project_root, "outputs", "execution_error.log")
                    with open(error_file, "w", encoding="utf-8") as f:
                        f.write(current_log)
                    
                    # Call Refiner with error context
                    refiner_script = os.path.join(os.path.dirname(__file__), "refiner.py")
                    print(colored("🧠 Regenerating code with error context...", "cyan"))
                    domain = config.get("domain", "general")
                    subprocess.run(["python", refiner_script, trace_path, test_path, config.get("workflow_description", ""), error_file, domain])
                    
                    # Optional: Re-run reviewer if needed
                    from reviewer import CodeReviewer
                    domain = config.get("domain", "general")
                    CodeReviewer().review_and_fix(test_path, domain=domain)
                else:
                    print(colored(f"❌ Final Attempt {attempt + 1} Failed.", "red"))
    
        if not success:
            logger.log_failure("Executor", "All test attempts failed", {"path": test_path, "log_tail": execution_log[-1000:]})
            print(colored("\n❌ All test attempts failed!", "red", attrs=["bold"]))
            _log_error(config, "execution", execution_log[-1000:]) # Log tail of error for better visibility

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

    try:
        dashboard_script = os.path.join(os.path.dirname(__file__), "dashboard_generator.py")
        
        # Source Metrics (Global)
        metrics_source = os.path.join("outputs", "metrics.json")
        
        # Target Dashboard (Project Specific)
        dashboard_target = os.path.join(project_root, "outputs", "dashboard.html")
        
        ret = subprocess.run(["python", dashboard_script, metrics_source, dashboard_target], capture_output=False) 
        if ret.returncode == 0:
            print(colored(f"✅ Web Dashboard ready: {dashboard_target}", "green"))
    except Exception as e:
        print(colored(f"⚠️ Dashboard Generation Failed: {e}", "yellow"))
    save_checkpoint(project_root, "dashboard", config_hash)

    if success:
        print(colored("\n✅ Pipeline COMPLETE!", "green", attrs=["bold"]))
    else:
        print(colored("\n⚠️ Pipeline ended with test failures.", "yellow"))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python core/orchestrator.py <config_path> [--headed]")
        sys.exit(1)
        
    config_path = sys.argv[1]
    headed = "--headed" in sys.argv
    
    run_pipeline(config_path, headed=headed)
