"""
Banking Domain Test Specification Generator

Uses LLM to generate comprehensive test scenarios for banking/finance applications
based on domain expertise and regulatory compliance requirements.
"""

import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

BANKING_DOMAIN_PROMPT = """
You are a Senior QA Engineer specializing in Banking & Financial Services testing.

Given a banking application URL and its available features, generate a comprehensive test specification.

**REQUIREMENTS**:
1. Consider regulatory compliance (FDIC, PCI-DSS, SOC2)
2. Cover critical banking workflows
3. Include security test scenarios
4. Account for different user roles (Customer, Admin, Teller)

**OUTPUT FORMAT** (JSON):
{{
  "domain": "Banking & Finance",
  "features": [
    {{
      "feature_name": "Account Registration",
      "priority": "P0",
      "scenarios": [
        {{
          "scenario": "New customer registration with valid data",
          "given": "I am on the registration page",
          "when": "I fill all required fields with valid data",
          "then": "Account should be created successfully",
          "test_data": {{"firstName": "John", "lastName": "Doe"}},
          "assertions": ["Account confirmation message appears", "User is redirected to login"]
        }}
      ],
      "security_considerations": ["Password complexity", "SSN encryption"],
      "compliance_notes": "FDIC requires identity verification"
    }}
  ],
  "test_suites": [
    {{
      "suite_name": "Smoke Tests",
      "features": ["Account Registration", "Login", "View Balance"]
    }}
  ]
}}

**CRITICAL BANKING FEATURES TO COVER**:
- Account Registration & KYC
- Login/Logout & Session Management
- Account Overview & Balance Check
- Fund Transfer (Internal & External)
- Bill Payment
- Transaction History
- Account Statements
- Profile Management
- Security Settings (2FA, Security Questions)

Generate spec for: {site_description}
"""

def generate_banking_spec(site_url, site_description):
    """Generate comprehensive test specification for banking site"""
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)
    
    prompt = BANKING_DOMAIN_PROMPT.format(site_description=site_description)
    resp = llm.invoke(prompt)
    
    # Parse JSON
    spec_json = resp.content.replace("```json", "").replace("```", "").strip()
    return json.loads(spec_json)

def create_feature_files(spec, output_dir="specs/features"):
    """Create Gherkin-style feature files"""
    os.makedirs(output_dir, exist_ok=True)
    
    for feature in spec["features"]:
        feature_name = feature["feature_name"].replace(" ", "_").lower()
        feature_file = os.path.join(output_dir, f"{feature_name}.feature")
        
        with open(feature_file, "w") as f:
            f.write(f"Feature: {feature['feature_name']}\n")
            f.write(f"  Priority: {feature['priority']}\n")
            f.write(f"  Compliance: {feature.get('compliance_notes', 'N/A')}\n\n")
            
            for scenario in feature["scenarios"]:
                f.write(f"  Scenario: {scenario['scenario']}\n")
                f.write(f"    Given {scenario['given']}\n")
                f.write(f"    When {scenario['when']}\n")
                f.write(f"    Then {scenario['then']}\n")
                
                # Add assertions
                for assertion in scenario.get("assertions", []):
                    f.write(f"    And {assertion}\n")
                f.write("\n")
        
        print(f"✅ Created: {feature_file}")

def create_step_definitions(spec, output_dir="tests/steps"):
    """Generate Python step definition templates"""
    os.makedirs(output_dir, exist_ok=True)
    
    step_file = os.path.join(output_dir, "banking_steps.py")
    
    with open(step_file, "w") as f:
        f.write("""import pytest
from playwright.sync_api import Page, expect

# Reusable Banking Test Steps

class BankingSteps:
    def __init__(self, page: Page):
        self.page = page
    
    # REGISTRATION STEPS
    def navigate_to_registration(self):
        \"\"\"Navigate to registration page\"\"\"
        self.page.get_by_role("link", name="Register").click()
        expect(self.page).to_have_url(re.compile(".*register"))
    
    def fill_registration_form(self, user_data):
        \"\"\"Fill complete registration form\"\"\"
        self.page.locator("input[name='firstName']").fill(user_data["firstName"])
        self.page.locator("input[name='lastName']").fill(user_data["lastName"])
        self.page.locator("input[name='address']").fill(user_data["address"])
        self.page.locator("input[name='city']").fill(user_data["city"])
        self.page.locator("input[name='state']").fill(user_data["state"])
        self.page.locator("input[name='zipCode']").fill(user_data["zipCode"])
        self.page.locator("input[name='phoneNumber']").fill(user_data["phoneNumber"])
        self.page.locator("input[name='ssn']").fill(user_data["ssn"])
        self.page.locator("input[name='username']").fill(user_data["username"])
        self.page.locator("input[name='password']").fill(user_data["password"])
        self.page.locator("input[name='repeatedPassword']").fill(user_data["password"])
    
    def submit_registration(self):
        \"\"\"Submit registration form\"\"\"
        self.page.locator("input[type='submit'][value='Register']").click()
    
    def verify_registration_success(self):
        \"\"\"Verify successful registration\"\"\"
        expect(self.page.locator("text=success")).to_be_visible()
    
    # LOGIN STEPS
    def login(self, username, password):
        \"\"\"Perform login\"\"\"
        self.page.locator("input[name='username']").fill(username)
        self.page.locator("input[name='password']").fill(password)
        self.page.locator("input[type='submit'][value='Log In']").click()
    
    def verify_login_success(self):
        \"\"\"Verify successful login\"\"\"
        expect(self.page.locator("text=Account Overview")).to_be_visible()
    
    # ACCOUNT STEPS
    def navigate_to_account_overview(self):
        \"\"\"Navigate to account overview\"\"\"
        self.page.get_by_role("link", name="Accounts Overview").click()
    
    def get_account_balance(self):
        \"\"\"Get current account balance\"\"\"
        balance_element = self.page.locator(".balance")
        return balance_element.inner_text()
    
    def verify_balance_displayed(self):
        \"\"\"Verify balance is displayed\"\"\"
        expect(self.page.locator(".balance")).to_be_visible()
    
    # TRANSFER STEPS  
    def navigate_to_transfer_funds(self):
        \"\"\"Navigate to fund transfer page\"\"\"
        self.page.get_by_role("link", name="Transfer Funds").click()
    
    def transfer_funds(self, amount, from_account, to_account):
        \"\"\"Transfer funds between accounts\"\"\"
        self.page.locator("input[name='amount']").fill(str(amount))
        self.page.locator("select[name='fromAccountId']").select_option(from_account)
        self.page.locator("select[name='toAccountId']").select_option(to_account)
        self.page.locator("input[type='submit'][value='Transfer']").click()
    
    def verify_transfer_success(self):
        \"\"\"Verify successful fund transfer\"\"\"
        expect(self.page.locator("text=Transfer Complete")).to_be_visible()
""")
    
    print(f"✅ Created: {step_file}")

def create_test_suites(spec, output_dir="tests/suites"):
    """Generate pytest test suite files"""
    os.makedirs(output_dir, exist_ok=True)
    
    for suite in spec.get("test_suites", []):
        suite_name = suite["suite_name"].replace(" ", "_").lower()
        suite_file = os.path.join(output_dir, f"test_{suite_name}.py")
        
        with open(suite_file, "w") as f:
            f.write(f'''"""
{suite["suite_name"]} for ParaBank
Auto-generated test suite based on domain specification
"""

import pytest
from playwright.sync_api import Page
from tests.steps.banking_steps import BankingSteps

@pytest.fixture
def banking_steps(page: Page):
    return BankingSteps(page)

class Test{suite["suite_name"].replace(" ", "")}:
    """Test suite: {suite["suite_name"]}"""
    
''')
            
            # Generate test methods based on features
            if suite["features"] == ["All"]:
                features_to_test = spec["features"]
            else:
                features_to_test = [f for f in spec["features"] if f["feature_name"] in suite["features"]]
            
            for feature in features_to_test:
                test_name = feature["feature_name"].replace(" ", "_").lower()
                f.write(f'''    def test_{test_name}(self, page: Page, banking_steps):
        """Test: {feature["feature_name"]}"""
        page.goto("https://parabank.parasoft.com/parabank/index.htm")
        
        # TODO: Implement test steps based on scenarios
        # See specs/features/{test_name}.feature for scenario details
        pass
    
''')
        
        print(f"✅ Created: {suite_file}")

if __name__ == "__main__":
    print("🏦 Banking Test Specification Generator")
    print("=" * 60)
    
    site_description = """
    ParaBank - Online Banking Demo Application
    URL: https://parabank.parasoft.com/parabank/
    
    Available Features:
    - User Registration
    - Login/Logout
    - Account Overview
    - Account Details
    - Transfer Funds
    - Bill Payment
    - Find Transactions
    - Update Contact Info
    - Request Loan
    - Admin Page
    """
    
    print("\n📋 Generating comprehensive test specification...")
    spec = generate_banking_spec("https://parabank.parasoft.com/parabank/", site_description)
    
    # Save spec
    os.makedirs("specs", exist_ok=True)
    with open("specs/parabank_spec.json", "w") as f:
        json.dump(spec, f, indent=2)
    print("✅ Spec saved: specs/parabank_spec.json")
    
    print("\n📝 Creating feature files...")
    create_feature_files(spec)
    
    print("\n🔧 Creating step definitions...")
    create_step_definitions(spec)
    
    print("\n🧪 Creating test suites...")
    create_test_suites(spec)
    
    print("\n🎉 Complete! Test framework generated.")
    print("\nNext steps:")
    print("1. Review specs/features/*.feature files")
    print("2. Customize tests/steps/banking_steps.py")
    print("3. Run: pytest tests/suites/")
