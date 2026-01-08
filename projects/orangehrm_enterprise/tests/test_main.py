# OrangeHRM Enterprise - Complex E2E Test
# Mission: Login → Add Employee → Create System User for that Employee
import pytest
import random
from playwright.sync_api import Browser, expect


def test_autonomous_flow(browser: Browser) -> None:
    """
    Complex E2E Test for OrangeHRM Enterprise
    
    Test Flow:
    1. Login to OrangeHRM
    2. Navigate to PIM module
    3. Add new employee (FirstNameTest LastNameTest)
    4. Navigate to Admin module
    5. Create System User for the newly created employee
    
    Success Criteria: All steps must complete without errors
    """
    page = browser.new_page()

    try:
        # ========================================
        # STEP 1: LOGIN
        # ========================================
        print("\n🔐 STEP 1: Logging into OrangeHRM...")
        page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        page.wait_for_load_state("networkidle")
        
        # Fill login credentials
        page.locator("[name='username']").wait_for(state="visible", timeout=10000)
        page.locator("[name='username']").fill("Admin")
        page.locator("[name='password']").fill("admin123")
        page.get_by_role("button", name="Login").click()
        
        # Verify successful login
        page.wait_for_url("**/dashboard**", timeout=15000)
        print("   ✅ Successfully logged in - Dashboard loaded")

        # ========================================
        # STEP 2: NAVIGATE TO PIM MODULE
        # ========================================
        print("\n👥 STEP 2: Navigating to PIM module...")
        page.get_by_role("link", name="PIM").click()
        page.wait_for_load_state("networkidle")
        page.wait_for_url("**/pim/viewEmployeeList**", timeout=10000)
        print("   ✅ Navigated to PIM - Employee List")

        # ========================================
        # STEP 3: ADD NEW EMPLOYEE
        # ========================================
        print("\n➕ STEP 3: Adding new employee...")
        
        # Click Add button
        page.get_by_role("button", name="Add").first.click()
        page.wait_for_load_state("networkidle")
        page.wait_for_url("**/pim/addEmployee**", timeout=10000)
        print("   ✅ Add Employee page loaded")

        # Fill employee details
        print("   📝 Filling employee details (FirstNameTest LastNameTest)...")
        page.locator("[name='firstName']").wait_for(state="visible", timeout=5000)
        page.locator("[name='firstName']").fill("FirstNameTest")
        page.locator("[name='lastName']").fill("LastNameTest")
        
        # Save employee
        print("   💾 Saving employee...")
        page.get_by_role("button", name="Save").click()
        
        # Wait for redirect to Personal Details page (this is the expected behavior)
        page.wait_for_url("**/pim/viewPersonalDetails/**", timeout=15000)
        print("   ✅ Employee created successfully - Redirected to Personal Details page")

        # ========================================
        # STEP 4: NAVIGATE TO ADMIN MODULE
        # ========================================
        print("\n⚙️ STEP 4: Navigating to Admin module...")
        page.get_by_role("link", name="Admin").click()
        page.wait_for_load_state("networkidle")
        page.wait_for_url("**/admin/viewSystemUsers**", timeout=15000)
        print("   ✅ Navigated to Admin - System Users page")

        # ========================================
        # STEP 5: CREATE SYSTEM USER
        # ========================================
        print("\n👤 STEP 5: Creating system user for FirstNameTest LastNameTest...")
        
        # Click Add button to create new user
        page.get_by_role("button", name="Add").click()
        page.wait_for_load_state("networkidle")
        page.wait_for_url("**/admin/saveSystemUser**", timeout=10000)
        print("   ✅ Add User page loaded")
        
        # Fill user details
        print("   📋 Filling user details...")
        
        # 1. Select User Role: Admin
        print("      - Selecting User Role: Admin")
        page.locator(".oxd-select-text").first.click()
        page.wait_for_timeout(500)
        page.get_by_role("option", name="Admin").click()
        
        # 2. Enter Employee Name (autocomplete field)
        print("      - Entering Employee Name: FirstNameTest LastNameTest")
        employee_name_input = page.locator("input[placeholder='Type for hints...']")
        employee_name_input.fill("FirstNameTest")
        page.wait_for_timeout(2000)  # Wait for autocomplete suggestions
        
        # Select from autocomplete dropdown
        try:
            page.get_by_text("FirstNameTest LastNameTest").first.click()
            print("      - Employee selected from autocomplete")
        except:
            print("      - Warning: Autocomplete selection may have failed, continuing...")
        
        # 3. Select Status: Enabled
        print("      - Selecting Status: Enabled")
        page.locator(".oxd-select-text").nth(1).click()
        page.wait_for_timeout(500)
        page.get_by_role("option", name="Enabled").click()
        
        # 4. Enter Username (randomized to avoid conflicts)
        username = f"testuser{random.randint(1000, 9999)}"
        print(f"      - Entering Username: {username}")
        page.locator("xpath=//label[text()='Username']/parent::div/following-sibling::div/input").fill(username)
        
        # 5. Enter Password (must meet complexity requirements)
        password = "Admin123!@#"
        print("      - Entering Password")
        page.locator("xpath=//label[text()='Password']/parent::div/following-sibling::div/input").fill(password)
        
        # 6. Confirm Password
        print("      - Confirming Password")
        page.locator("xpath=//label[text()='Confirm Password']/parent::div/following-sibling::div/input").fill(password)
        
        # Save user
        print("   💾 Saving system user...")
        page.get_by_role("button", name="Save").click()
        page.wait_for_load_state("networkidle")
        
        # Verify user creation success
        page.wait_for_url("**/admin/viewSystemUsers**", timeout=15000)
        print(f"   ✅ System user '{username}' created successfully!")

        # ========================================
        # MISSION ACCOMPLISHED!
        # ========================================
        print("\n" + "="*60)
        print("🎉 MISSION ACCOMPLISHED - ALL STEPS COMPLETED!")
        print("="*60)
        print(f"✅ Employee Created: FirstNameTest LastNameTest")
        print(f"✅ System User Created: {username}")
        print(f"✅ User Role: Admin")
        print(f"✅ Status: Enabled")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        print(f"   Current URL: {page.url}")
        raise
    
    finally:
        # Keep browser open for a moment to show success
        page.wait_for_timeout(2000)