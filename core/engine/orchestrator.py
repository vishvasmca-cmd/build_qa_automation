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
    from core.lib.metrics_logger import logger
except ImportError:
    # Fallback if run directly
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lib"))
    from metrics_logger import logger

from core.lib.git_utils import GitManager

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
        from core.agents.feedback_agent import FeedbackAgent
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
    print(colored("\n[Step 0/7] 📋 Validating Target URL...", "cyan"))
    if can_skip_phase(project_root, "planning", config_hash):
        print(colored("⏩ Skipping URL Validation (Checkpoint found)", "grey"))
        return True

    target_url = config.get("target_url")
    if not target_url:
        print(colored("❌ No target URL provided", "red"))
        return False
    
    # Quick validation: Check if website exists using Playwright
    try:
        from playwright.sync_api import sync_playwright
        print(f"🌐 Checking if {target_url} is accessible...")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-infobars"
                ]
            )
            context = browser.new_context(
                viewport={"width": 1280, "height": 800},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                ignore_https_errors=True,
                locale="en-US",
                extra_http_headers={
                    "Accept-Language": "en-US,en;q=0.9",
                    "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                }
            )
            context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                window.chrome = {runtime: {}};
            """)
            page = context.new_page()
            try:
                response = page.goto(target_url, timeout=30000, wait_until="domcontentloaded")
                if response and response.ok:
                    print(colored(f"✅ Website is accessible (HTTP {response.status})", "green"))
                    browser.close()
                    save_checkpoint(project_root, "planning", config_hash)
                    return True
                else:
                    status = response.status if response else "No Response"
                    print(colored(f"❌ Website returned HTTP {status}", "red"))
                    browser.close()
                    return False
            except Exception as nav_error:
                print(colored(f"❌ Cannot access website: {nav_error}", "red"))
                browser.close()
                return False
    except Exception as e:
        logger.log_failure("URLValidator", str(e), {"url": target_url})
        print(colored(f"❌ URL Validation Failed: {e}", "red"))
        return False

def _run_exploration(project_root, config, config_hash, config_path, headed=False):
    print(colored("\n[Step 1/7] 🗺️  Exploring & Mining (Plan-Guided)...", "cyan"))
    trace_path = config.get("paths", {}).get("trace", os.path.join(project_root, "outputs/trace.json"))
    
    if can_skip_phase(project_root, "exploration", config_hash):
        print(colored("⏩ Skipping Exploration (Checkpoint found)", "grey"))
        return True

    for attempt in range(1, 4):
        start_time = time.time()
        # Adjusted path: core/engine/orchestrator.py -> core/agents/explorer.py
        explorer_script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "agents", "explorer.py")
        cmd = ["python", explorer_script, config_path]
        if headed: cmd.append("--headed")
        
        env = os.environ.copy()
        env["PYTHONPATH"] = os.getcwd()
        # Enable real-time output by removing capture_output=True and letting it inherit stdout/stderr
        ret = subprocess.run(cmd, capture_output=False, text=True, encoding='utf-8', errors='ignore', env=env)
        
        if ret.returncode == 0:
            duration = time.time() - start_time
            logger.log_event("Explorer", "exploration_phase", duration, success=True)
            save_checkpoint(project_root, "exploration", config_hash)
            return True
        else:
            print(colored(f"⚠️ Exploration Attempt {attempt} Failed (Code {ret.returncode}).", "yellow"))
            # Output is now directly on console, so we can't reprint it from memory
            error_context = {"attempt": attempt, "stdout": "See console", "stderr": "See console"}
            logger.log_failure("Explorer", f"Exit code {ret.returncode}", error_context)
    
    # NO FALLBACK - Let it fail properly so robust mode can retry
    print(colored("❌ Explorer Failed after 3 attempts. Robust mode will retry the entire pipeline.", "red"))
    _log_error(config, "exploration", "Explorer failed after all retries")
    return False

def _run_knowledge_update(project_root, config, config_hash, trace_path):
    print(colored("\n[Step 2/7] Updating Knowledge Bank...", "cyan"))
    if can_skip_phase(project_root, "knowledge_update", config_hash):
        print(colored("⏩ Skipping Knowledge Update (Checkpoint found)", "grey"))
        return

    try:
        from core.knowledge.knowledge_bank import KnowledgeBank
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
    from core.agents.reviewer import CodeReviewer

    for attempt in range(1, 6):
        print(colored(f"🔄 Generation Loop {attempt}/5...", "cyan"))
        start_time = time.time()
        # Adjusted path: core/engine/orchestrator.py -> core/agents/refiner.py
        refiner_script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "agents", "refiner.py")
        domain = config.get("domain", "general")
        
        error_file_arg = ""
        if error_context:
            error_file = os.path.join(project_root, "outputs", "gen_feedback.log")
            with open(error_file, "w", encoding="utf-8") as f: f.write(str(error_context))
            error_file_arg = error_file
            print(colored(f"💡 Feeding Reviewer Feedback to Refiner: {str(error_context)[:100]}...", "yellow"))

        env = os.environ.copy()
        env["PYTHONPATH"] = os.getcwd()
        ret = subprocess.run(["python", refiner_script, trace_path, test_path, config.get("workflow_description", ""), error_file_arg, domain], capture_output=False, env=env)
        
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
            from core.lib.minimal_template import generate_minimal_smoke_test
            generate_minimal_smoke_test(config, test_path)
            print(colored("✅ Minimal smoke test created as fallback", "green"))
            gen_success = True
            save_checkpoint(project_root, "generation", config_hash)
        except Exception as e:
            print(colored(f"❌ Fallback generation also failed: {e}", "red"))
            _log_error(config, "generation", f"Failed generation: {e}")
            return False
            
    return True

def _run_batch_mining(project_root, config, config_hash):
    """Phase 2: Run Batch Miner to discover page models."""
    print(colored("\n[Step 2/7] ⛏️ Batch Mining & Discovery...", "cyan"))
    
    # We don't skip this yet as it's fast and crucial for new snapshots
    
    try:
        from core.agents.miner import BatchMiner
        
        miner = BatchMiner(project_root)
        import asyncio
        asyncio.run(miner.mine())
        
        save_checkpoint(project_root, "mining", config_hash)
        return True
    except Exception as e:
        print(colored(f"❌ Batch Mining Failed: {e}", "red"))
        return False

def _run_framework_generation(project_root, config, config_hash):
    """Phase 3: Generate strict POM Framework."""
    print(colored("\n[Step 3/7] 🏭 Framework Generation...", "cyan"))
    
    try:
        from core.agents.refiner import FrameworkGenerator
        
        gen = FrameworkGenerator(project_root)
        success = gen.generate()
        
        if success:
             save_checkpoint(project_root, "framework_gen", config_hash)
             return True
        return False
    except Exception as e:
        print(colored(f"❌ Framework Generation Failed: {e}", "red"))
        return False

def _run_spec_synthesis(project_root, config, config_hash):
    print(colored("\n[Step 4/7] 🧠 Synthesizing Specs & Features...", "cyan"))
    if can_skip_phase(project_root, "spec_synthesis", config_hash):
        print(colored("⏩ Skipping Spec Synthesis (Checkpoint found)", "grey"))
        return

    try:
        from core.knowledge.spec_synthesizer import SpecSynthesizer
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
    # Adjusted path: core/engine/orchestrator.py -> core/lib/reporter.py
    reporter_script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "lib", "reporter.py")
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    subprocess.run(["python", reporter_script, trace_path, report_path], capture_output=False, env=env)
    save_checkpoint(project_root, "reporting", config_hash)

def _run_execution(project_root, config, config_hash, test_path, trace_path):
    print(colored("\n[Step 6/7] 🧪 Executing Verified Test...", "cyan"))
    execution_log = ""
    
    if can_skip_phase(project_root, "execution", config_hash):
        print(colored("⏩ Skipping Test Execution (Checkpoint found)", "grey"))
        execution_log = "Execution skipped (Checkpoint found)."
        return True, execution_log

    max_retries = 10
    success = False
    
    for attempt in range(max_retries):
        print(f"Attempt {attempt + 1}/{max_retries}...")
        start_time = time.time()
        
        # Prepare Environment with PYTHONPATH
        env = os.environ.copy()
        # Add project_root to path so 'from pages import ...' works
        env["PYTHONPATH"] = project_root + os.pathsep + os.getcwd()

        # Define output directory for test results
        # Define output directory for test results
        output_dir = os.path.join(project_root, "outputs", "test-results")
        ret = subprocess.run(["pytest", test_path, "-v", "-s", f"--output={output_dir}"], capture_output=True, text=True, encoding='utf-8', errors='replace', env=env)
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
                print(colored(f"⚠️ Attempt {attempt + 1} Failed. Triggering MASTER AGENT Self-Correction...", "yellow"))
                
                # 1. IMMEDIATE LEARNING (The "Master Agent" Step)
                try:
                    from core.agents.feedback_agent import FeedbackAgent
                    print(colored(f"🧠 Analyzing failure to update Knowledge Base...", "cyan"))
                    feedback = FeedbackAgent()
                    # We pass 'success=False' to force failure analysis. 
                    # This updates knowledge/sites/{domain}/rules.md and failures.json
                    feedback.analyze_run(config, current_log, success=False)
                    print(colored(f"✅ Knowledge Updated. Re-generating code with new insights...", "green"))
                except Exception as e:
                    print(colored(f"⚠️ Feedback Loop Failed: {e}", "red"))

                # 2. RE-GENERATION (Refiner now sees the new rules.md)
                error_file = os.path.join(project_root, "outputs", "execution_error.log")
                with open(error_file, "w", encoding="utf-8") as f: f.write(current_log)
                
                # Adjusted path: core/engine/orchestrator.py -> core/agents/refiner.py
                refiner_script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "agents", "refiner.py")
                domain = config.get("domain", "general")
                
                # Prepare Environment for Refiner
                re_env = os.environ.copy()
                re_env["PYTHONPATH"] = os.getcwd()
                # The Refiner will now read the updated rules.md and generate better code
                subprocess.run(["python", refiner_script, trace_path, test_path, config.get("workflow_description", ""), error_file, domain], env=re_env)

                # 3. COMMIT & PUSH FIX (User Request)
                # GitManager.commit_and_push(f"Auto-fix iteration {attempt + 1} for {config.get('project_name')}")
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
            from core.lib.validator import BusinessValidator
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
                logger.log_event("Validator", "validate_goal", 0.0, success=False, metadata=result)
            else:
                print(colored(f"✅ GOAL VERIFIED: {result.get('reason')}", "green"))
                logger.log_event("Validator", "validate_goal", 0.0, success=True, metadata=result)
        except Exception as e:
            print(colored(f"⚠️ Validation Skipped: {e}", "yellow"))

def _run_feedback(config_path, execution_log, success):
    print(colored("\n[Step 6.5] 🧠 Feedback & Self-Training...", "cyan"))
    print(colored("\n[Step 6.5] 🧠 Feedback & Self-Training...", "cyan"))
    try:
        from core.agents.feedback_agent import FeedbackAgent
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
                from core.agents.security_auditor import SecurityAuditor
                auditor = SecurityAuditor(config.get("target_url"), project_root)
                auditor.run_all_checks()
                save_checkpoint(project_root, "security", config_hash)
            except Exception as e:
                print(colored(f"⚠️ Security Audit Failed: {e}", "yellow"))
    else:
        print(colored("\n[Step 7/7] 🛡️  Security Audit skipped (not requested).", "white"))

def _run_dashboard(project_root, config_hash):
    try:
        # Adjusted path: core/engine/orchestrator.py -> core/lib/dashboard_generator.py
        dashboard_script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "lib", "dashboard_generator.py")
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
    with open(config_path, "r") as f:
        config = json.load(f)
    
    # 0. SYNC (User Request)
    GitManager.sync()
        
    print(colored("\n" + "="*60, "green", attrs=["bold"]))
    print(colored(f"🚀 MISSION: {config.get('project_name', 'Unnamed Project')}", "green", attrs=["bold"]))
    print(colored(f"🌐 TARGET: {config.get('target_url')}", "white"))
    print(colored(f"📝 GOAL: {config.get('workflow_description') or config.get('goal')}", "white"))
    print(colored("="*60, "green", attrs=["bold"]))
        
    config_hash = _get_config_hash(config)
    project_root = os.path.dirname(config_path)
    trace_path_initial = config.get("paths", {}).get("trace", os.path.join(project_root, "outputs/trace.json")) # Renamed to avoid conflict
    test_path_initial = config.get("paths", {}).get("test", os.path.join(project_root, "tests/test_main.py")) # Renamed to avoid conflict
    logger.log_event("Orchestrator", "pipeline_start", duration=0, success=True, metadata={"config": config})
    
    # === MASTER AGENT SUPERVISOR ===
    
    SERVER_REGISTRY = {
        "Planner": "available",
        "Explorer": "available",
        "KnowledgeBase": "available",
        "Coder": "available",
        "Executor": "available",
        "SecurityOfficer": "available"
    }
    
    def _update_master_status(phase, status, details=None):
        """
        Writes real-time status to master_status.json for User visibility.
        """
        status_file = os.path.join(project_root, "outputs", "master_status.json")
        try:
            # Load existing
            if os.path.exists(status_file):
                with open(status_file, "r") as f:
                    data = json.load(f)
            else:
                data = {
                    "project": config["project_name"],
                    "master_status": "ACTIVE", 
                    "agents": SERVER_REGISTRY
                }
            
            # Update specific agent
            if phase in data["agents"]:
                data["agents"][phase] = status
            
            # Add event log
            if "events" not in data: data["events"] = []
            import datetime
            data["events"].append({
                "timestamp": datetime.datetime.now().isoformat(),
                "agent": phase,
                "status": status,
                "details": details or ""
            })
            
            # Keep log short
            if len(data["events"]) > 20: data["events"] = data["events"][-20:]
            
            os.makedirs(os.path.dirname(status_file), exist_ok=True)
            with open(status_file, "w") as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"⚠️ Failed to update Master Status: {e}")

    def _run_sub_agent(phase_name, func, *args, max_retries=20):
        """
        The 'Boss' wrapper. Executes a sub-agent with monitoring, error handling, and self-correction.
        """
        _update_master_status(phase_name, "assigned", "Task assigned to agent")
        
        for attempt in range(max_retries):
            try:
                # 1. Execute Sub-Agent
                _update_master_status(phase_name, "working", f"Attempt {attempt+1}/{max_retries}")
                print(colored(f"\n[Boss] 🕵️ Starting Agent: {phase_name} (Attempt {attempt+1}/{max_retries})...", "magenta"))
                result = func(*args)
                
                # Handling return values (some return bool, others void)
                success = True
                if isinstance(result, bool): success = result
                elif isinstance(result, tuple) and len(result) > 0: success = result[0]
                
                if success:
                    print(colored(f"[Boss] ✅ Agent {phase_name} Succeeded.", "green", attrs=["bold"]))
                    _update_master_status(phase_name, "idle", "Task completed successfully")
                    return result # Return the original output
                else:
                    raise Exception(f"Agent {phase_name} returned failure status.")

            except Exception as e:
                print(colored(f"[Boss] ❌ Agent {phase_name} Failed permanently.", "red", attrs=["bold"]))
                _update_master_status(phase_name, "error", str(e))
                
                # 2. Trigger Feedback / Recovery
                if attempt < max_retries - 1:
                    print(colored(f"[Boss] 🧠 Consult Feedback Agent for {phase_name}...", "cyan"))
                    _update_master_status(phase_name, "healing", "Consulting Feedback Agent")
                    _update_master_status(phase_name, "healing", "Consulting Feedback Agent")
                    try:
                        from core.agents.feedback_agent import FeedbackAgent
                        fb = FeedbackAgent()
                        if phase_name == "Coder":
                            # Special case: The refiner failing usually means generation failed, 
                            # we might want to analyze the error log if it exists.
                            pass
                        elif phase_name == "Executor":
                             # Already handled inside _run_execution usually, but good to double check
                             pass
                        else:
                             fb.analyze_generic_error(phase_name, str(e))
                    except: pass
                    time.sleep(2) # Breath before retry
                else:
                    print(colored(f"[Boss] ❌ Agent {phase_name} Failed permanently.", "red"))
                    _update_master_status(phase_name, "dead", "Max retries exceeded")
                    return result if 'result' in locals() else False

        return False

    # --- Phase Execution with Supervisor ---
    
    # 1. PLANNING
    # _run_sub_agent("Planner", _run_planning, project_root, config, config_hash)
    
    # For now, we keep the original flow but we will migrate them one by one or wrap them here.
    # To minimize diff size, we will wrap the calls below.

    # [Step 0/7] Planning
    if not _run_sub_agent("Planner", _run_planning, project_root, config, config_hash, config_path): return

    # [Step 1/7] Exploration (Miner)
    trace_path = os.path.join(project_root, "outputs", "trace.json")
    print(colored("\n" + "⠿"*60, "yellow"))
    print(colored("🔍 PHASE: EXPLORATION & MINING", "yellow", attrs=["bold"]))
    print(colored("⠿"*60, "yellow"))
    
    start_explore = time.time()
    if not _run_sub_agent("Explorer", _run_exploration, project_root, config, config_hash, config_path, headed):
        return
    print(colored(f"✅ Exploration complete in {time.time() - start_explore:.1f}s", "green"))

    # 4. Mine (New Phase)
    print(colored("\n🛠️  PHASE: BATCH MINING (AUTO-DISCOVERY)", "magenta", attrs=["bold"]))
    _run_batch_mining(project_root, config, config_hash)

    # 5. Knowledge Update
    print(colored("\n📖 PHASE: KNOWLEDGE BANK SYNCHRONIZATION", "cyan", attrs=["bold"]))
    _run_knowledge_update(project_root, config, config_hash, trace_path) 

    # 6. Framework Generation
    print(colored("\n🏗️  PHASE: POM FRAMEWORK GENERATION", "blue", attrs=["bold"]))
    if not _run_framework_generation(project_root, config, config_hash):
        return

    # [Step 3/7] Code Generation (Refiner)
    print(colored("\n📝 PHASE: TEST SCRIPT REFINEMENT", "white", attrs=["bold"]))
    test_path = config.get("paths", {}).get("test", os.path.join(project_root, "tests/test_main.py"))
    gen_success = _run_sub_agent("Coder", _run_code_generation, project_root, config, config_hash, trace_path, test_path)
    
    if not gen_success:
        print(colored("❌ Pipeline Halting: Code Generation Failed.", "red"))
        return False

    # [Step 4/7] Spec Synthesis
    _run_spec_synthesis(project_root, config, config_hash)

    # [Step 5/7] Reporting
    _run_reporting(project_root, config, config_hash, trace_path)
    
    # [Step 6/7] Execution
    success, execution_log = _run_execution(project_root, config, config_hash, test_path, trace_path)
    
    # [Step 6.2] Validation
    _run_validation(project_root, config, success)

    # [Step 6.5] Feedback
    _run_feedback(config_path, execution_log, success)

    # [Step 7/7] Security Audit
    _run_security_audit(project_root, config, config_hash)

    # [Step 8/7] Dashboard
    _run_dashboard(project_root, config_hash)

    if success:
        print(colored("\n✅ Pipeline COMPLETE!", "green", attrs=["bold"]))
        GitManager.commit_and_push(f"SUCCESS: Mission Accomplished for {config.get('project_name')}")
    else:
        print(colored("\n⚠️ Pipeline ended with test failures.", "yellow"))
        # GitManager.commit_and_push(f"FAILURE: Unresolved issues in {config.get('project_name')}")
    
    return success

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python core/orchestrator.py <config_path> [--headed]")
        sys.exit(1)
        
    config_path = sys.argv[1]
    headed = "--headed" in sys.argv
    
    run_pipeline(config_path, headed=headed)
