
import sys

# Windows Unicode Fix
try:
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

import os
import json
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

PROJECTS = [
    {
        "name": "verify_stress_sauce",
        "url": "https://www.saucedemo.com/",
        "domain": "ecommerce",
        "description": "Login 'standard_user'/'secret_sauce'. Sort Z-A. Add 'Test.allTheThings() T-Shirt'. Go to item details 'Sauce Labs Onesie'. go back. Add 'Sauce Labs Bike Light'. Go to Cart. Checkout. Info 'Jane' 'Doe' '12345'. Finish. Back Home. Logout."
    },
    {
        "name": "verify_stress_magento",
        "url": "https://magento.softwaretestingboard.com/",
        "domain": "ecommerce",
        "description": "Search 'Jacket'. Click 'Olivia 1/4 Zip'. Size 'M', Color 'Purple'. Add to Cart. Click 'Sale'. Click 'Tees'. Click 'Desiree Fitness Tee'. Size 'L', Color 'Black'. Add to Cart. Edit Cart. Update 'Desiree' qty to 2. Update Cart. Checkout as guest 'test@example.com', 'Test' 'User', '123 St', 'New York', 'NY', '10001', '1234567890'. Shipping 'Table Rate'. Payment. Place Order."
    },
    {
        "name": "verify_stress_parabank",
        "url": "https://parabank.parasoft.com/parabank/index.htm",
        "domain": "banking",
        "description": "Register new user (unique). Open New Account (Savings). Click Accounts Overview. Click the new account. Click Transfer Funds. Transfer $50 to new account. Click Bill Pay. Pay 'Electric Co' $100. Find Transactions by Amount $50. Update Contact Info 'Phone' to '555-0000'. Logout."
    },
    {
        "name": "verify_stress_automationexercise",
        "url": "https://automationexercise.com/",
        "domain": "ecommerce",
        "description": "Click Products. Search 'Dress'. Add first result. Continue Shopping. Add second result. Click Cart. Click Signup/Login. Signup 'NewUser' (unique email). Fill details 'Mr', 'Pass123', '1', 'Jan', '2000', 'First', 'Last', 'Company', 'Address', 'State', 'City', '10001', '123123123'. Create Account. Continue. Cart. Proceed to Checkout. Place Order. Card 'Name', '1234567812345678', '123', '01', '2030'. Pay. Delete Account."
    },
    {
        "name": "verify_stress_demoblaze",
        "url": "https://www.demoblaze.com/",
        "domain": "ecommerce",
        "description": "Sign up (unique). Login. Click 'Laptops'. Click 'Sony vaio i5'. Add to cart. Home. Click 'Monitors'. Click 'Apple monitor 24'. Add to cart. Cart. Delete 'Sony vaio i5'. Place Order. Name 'Test', Card '1234'. Purchase. Log out."
    },
    {
        "name": "verify_stress_computers",
        "url": "https://computer-database.gatling.io/computers",
        "domain": "generic",
        "description": "Click 'Add a new computer'. Name 'TestComp_Unique'. Introduced '2023-01-01'. Discontinued '2024-01-01'. Company 'Apple Inc.'. Create. Filter by 'TestComp_Unique'. Click result. Edit name to 'TestComp_Edited'. Save. Filter 'TestComp_Edited'. Click result. Delete."
    },
    {
        "name": "verify_stress_orangehrm",
        "url": "https://opensource-demo.orangehrmlive.com/",
        "domain": "hr",
        "description": "Login 'Admin'/'admin123'. Click Admin. Click Add (User). Role 'ESS'. Name 'Ranga Akunuri'. Status 'Enabled'. User 'testuser_unique'. Pass 'Password123!'. Save. Click PIM. Add Employee. First 'John', Last 'Doe'. Save. Click Directory. Search 'John Doe'. Logout."
    },
    {
        "name": "verify_stress_rahulshetty",
        "url": "https://rahulshettyacademy.com/client",
        "domain": "ecommerce",
        "description": "Register (unique). Login. Filter 'zara coat 3'. Add to Cart. Click Cart. Checkout. Select Country 'India'. Place Order. Click Orders. Click View on first order. Verify summary. Sign Out."
    },
    {
        "name": "verify_stress_internet",
        "url": "https://the-internet.herokuapp.com/",
        "domain": "generic",
        "description": "Click 'Form Authentication'. Login 'tomsmith'/'SuperSecretPassword!'. Logout. Back. Click 'Checkboxes'. Check both. Back. Click 'Dropdown'. Select Option 2. Back. Click 'Dynamic Controls'. Click Remove. Wait for 'It's gone!'. Click Add. Wait for 'It's back!'. Back. Click 'Inputs'. Type number. Back."
    },
    {
        "name": "verify_stress_ultimateqa",
        "url": "https://ultimateqa.com/automation",
        "domain": "generic",
        "description": "Click 'Big page with many elements'. Fill Name. Fill Email. Click Button. Back. Click 'Fill out forms'. Fill Name. Fill Message. Submit. Back. Click 'Fake Landing Page'. Click 'View Courses'. Search 'Python'. Verify results."
    }
]

def setup_project(proj):
    """Creates directory and config.json"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    proj_dir = os.path.join(base_dir, "projects", proj["name"])
    outputs_dir = os.path.join(proj_dir, "outputs")
    os.makedirs(outputs_dir, exist_ok=True)
    
    # Randomize unique values in description to prevent collisions
    import random
    unique_id = f"{random.randint(1000,9999)}"
    desc = proj["description"].replace("(unique)", unique_id).replace("unique", unique_id)
    
    config = {
        "project_name": proj["name"],
        "target_url": proj["url"],
        "domain": proj["domain"],
        "workflow_description": desc,
        "depth_limit": 40,
        "strategies": ["interactive_exploration", "long_flow"],
        "paths": {
            "trace": os.path.join(outputs_dir, "trace.json").replace("\\", "\\\\"),
            "outputs": outputs_dir.replace("\\", "\\\\"),
            "test": os.path.join(proj_dir, "tests", "e2e", "test_main.py").replace("\\", "\\\\"),
            "report": os.path.join(outputs_dir, "report.md").replace("\\", "\\\\")
        }
    }
    
    with open(os.path.join(proj_dir, "config.json"), "w") as f:
        json.dump(config, f, indent=2)
    
    return os.path.join(proj_dir, "config.json")

def run_project(config_path):
    print(f"🚀 Launching {config_path}...")
    cmd = ["python", "trigger_agent.py", config_path, "--headless"]
    # We run sequentially to avoid browser conflicts / resource exhaustion
    # But could be parallelized if robust enough
    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    duration = time.time() - start
    
    success = result.returncode == 0 and "Test Execution SUCCESS!" in result.stdout
    
    if not success:
        print(f"DEBUG: Return Code: {result.returncode}")
        print(f"DEBUG: StdOut Len: {len(result.stdout)}")
        print(f"DEBUG: StdErr: {result.stderr}")
    
    # Extract metrics (simple parsing)
    steps = 0
    if "Step 30" in result.stdout: steps = 35 # rough guess
    elif "Step 20" in result.stdout: steps = 25
    
    return {
        "config": config_path,
        "success": success,
        "duration": duration,
        "log_tail": result.stdout[-500:],
        "error": result.stderr if not success else ""
    }

def main():
    results = []
    print(f"Starting Batch Stress Test for {len(PROJECTS)} projects...")
    
    for p in PROJECTS:
        cfg = setup_project(p)
        # Clear previous checkpoints to force fresh run
        checkpoints = [
            os.path.join(os.path.dirname(cfg), ".checkpoint_planning"),
            os.path.join(os.path.dirname(cfg), ".checkpoint_exploration"),
            os.path.join(os.path.dirname(cfg), ".checkpoint_generation"),
            os.path.join(os.path.dirname(cfg), ".checkpoint_review"),
            os.path.join(os.path.dirname(cfg), ".checkpoint_execution"),
            os.path.join(os.path.dirname(cfg), ".checkpoint.json")
        ]
        for cp in checkpoints:
            if os.path.exists(cp): os.remove(cp)
            
        res = run_project(cfg)
        results.append(res)
        
        status = "✅ PASS" if res['success'] else "❌ FAIL"
        print(f"Finished {p['name']}: {status} ({res['duration']:.1f}s)")
        if not res['success']:
            print(f"Error Tail:\n{res['log_tail']}")

    # Summary
    print("\n" + "="*50)
    print("BATCH STRESS TEST SUMMARY")
    print("="*50)
    passed = sum(1 for r in results if r['success'])
    print(f"Total: {len(results)}, Passed: {passed}, Failed: {len(results) - passed}")
    
    for r in results:
        name = os.path.basename(os.path.dirname(r['config']))
        status = "PASS" if r['success'] else "FAIL"
        print(f"{name}: {status}")

if __name__ == "__main__":
    main()
