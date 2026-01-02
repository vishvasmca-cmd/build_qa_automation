import os
import subprocess
import time

# Comprehensive Training Sites - From Basic to Advanced
TRAINING_SITES = [
    # === BASIC: Simple Navigation & Forms ===
    {
        "project": "train_ultimateqa",
        "url": "https://ultimateqa.com/automation",
        "goal": "Navigate to Big Page and interact with elements",
        "domain": "tutorial",
        "docs": "Click 'Big page with many elements'. Scroll to discover buttons. Click a few."
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

def run_training_loop():
    print("🧠 Starting Advanced Training Loop with Enhanced Reasoning...")
    print("   → Scenarios: Basic Navigation → CRUD → Complex Forms")
    
    for site in TRAINING_SITES:
        print(f"\n--- 🏫 Training on: {site['project']} ({site['url']}) ---")
        
        cmd = [
            "python", "run.py",
            "--project", site["project"],
            "--url", site["url"],
            "--goal", site["goal"],
            "--domain", site["domain"],
            "--docs", site["docs"]
        ]
        
        try:
            start_time = time.time()
            subprocess.run(cmd, check=True)
            duration = time.time() - start_time
            print(f"✅ Training on {site['project']} completed in {duration:.2f}s")
        except subprocess.CalledProcessError as e:
            print(f"❌ Training on {site['project']} failed: {e}")
            
    print("\n📦 Finalizing Advanced Knowledge Bank...")
    from core.knowledge_bank import KnowledgeBank
    kb = KnowledgeBank()
    kb.export_knowledge("trained_kb_advanced_v1.json")
    print("🚀 Advanced training complete! Enhanced KB with multi-site patterns saved.")

if __name__ == "__main__":
    run_training_loop()
