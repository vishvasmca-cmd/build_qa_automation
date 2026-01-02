import os
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

# Comprehensive Training Sites - From Basic to Advanced
TRAINING_SITES = [
    # === BASIC: Simple Navigation & Forms ===
    {
        "project": "train_ultimateqa",
        "url": "https://ultimateqa.com/automation",
        "goal": "Navigate to Big Page and interact with elements",
        "domain": "tutorial",
        "docs": "Click 'Big page with many elements'. (Hint: It might be a Section Link). If that fails, scroll down and look for 'Complicated Page'."
    },
    {
        "project": "train_webdriveruniv",
        "url": "http://webdriveruniversity.com/index.html",
        "goal": "Complete Contact Us form in new tab",
        "domain": "tutorial",
        "docs": "Click Contact Us. Fill form with dummy data. Submit."
    },
    
    # === INTERMEDIATE: Login & CRUD ===
    {
        "project": "train_contact_list",
        "url": "https://thinking-tester-contact-list.herokuapp.com/",
        "goal": "Register, login, and manage contacts",
        "domain": "saas",
        "docs": "No credentials provided. Find Sign Up. Register realistic user. Login. Add 2 contacts."
    },
    {
        "project": "train_github_search",
        "url": "https://gh-users-search.netlify.app/",
        "goal": "Search users and view profile",
        "domain": "api_ui",
        "docs": "Search 'torvalds'. Click first result. Scroll to see repositories."
    },
    
    # === ADVANCED: Complex Forms & Components ===
    {
        "project": "train_demoqa_forms",
        "url": "https://demoqa.com/automation-practice-form",
        "goal": "Fill complete automation practice form",
        "domain": "forms",
        "docs": "Fill all fields: text, email, gender radio, date picker, subjects, hobbies checkboxes. Submit."
    },
    {
        "project": "train_parabank_full",
        "url": "https://parabank.parasoft.com/parabank/index.htm",
        "goal": "Register new account and explore features",
        "domain": "banking",
        "docs": "Find Register. Fill form. Login with new credentials. Navigate to Account Overview."
    },
    {
        "project": "train_acme_visual",
        "url": "https://demo.applitools.com/",
        "goal": "Login and verify dashboard",
        "domain": "banking",
        "docs": "Click Login (no credentials needed). Verify you see account balances."
    }
]

def process_site(site):
    print(f"🚀 [Started] Training on: {site['project']}")
    
    # Ensure logs dir exists
    log_dir = os.path.join("projects", site["project"])
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "training.log")
    
    cmd = [
        "python", "-u", "continuous_learning.py",
        "--project", site["project"],
        "--url", site["url"],
        "--goal", site["goal"],
        "--domain", site["domain"],
        "--docs", site["docs"],
        "--iterations", os.environ.get("CI_ITERATIONS", "10") # Default 10, override in CI
    ]
    
    try:
        start_time = time.time()
        # Redirect output to log file to avoid console chaos in parallel mode
        # Enable UTF-8 for emojis
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        
        with open(log_file, "w", encoding="utf-8") as f:
            subprocess.run(cmd, check=True, stdout=f, stderr=subprocess.STDOUT, env=env)
            
        duration = time.time() - start_time
        print(f"✅ [Finished] Training on {site['project']} in {duration:.2f}s")
    except subprocess.CalledProcessError as e:
        print(f"❌ [Failed] Training on {site['project']}. See logs in {log_file}")
    except Exception as e:
        print(f"❌ [Error] {site['project']}: {e}")

def run_training_loop():
    print("🧠 Starting Advanced Training Loop (Headless & Parallel)")
    print("   → Max Workers: 3")
    print("   → Logging to: projects/{name}/training.log")
    
    # Use ThreadPoolExecutor to run 3 sites in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(process_site, site) for site in TRAINING_SITES]
        
        # Wait for all futures to complete
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"Worker exception: {e}")

    print("\n📦 Finalizing Advanced Knowledge Bank...")
    # Import locally to avoid startup overhead/conflicts
    try:
        from core.knowledge_bank import KnowledgeBank
        kb = KnowledgeBank()
        kb.export_knowledge("trained_kb_advanced_v1.json")
        print("🚀 Advanced training complete! Enhanced KB with multi-site patterns saved.")
    except Exception as e:
        print(f"⚠️ Could not export KB: {e}")

if __name__ == "__main__":
    run_training_loop()
