# Banking Test Framework - ParaBank

## 🏦 Overview
AI-powered test framework for banking/finance applications with domain-specific test generation.

## 📁 Structure

```
inner-event/
├── specs/
│   ├── parabank_spec.json          # Master specification
│   └── features/                    # Gherkin feature files
│       ├── account_registration.feature
│       ├── login.feature
│       ├── fund_transfer.feature
│       └── ...
├── tests/
│   ├── steps/
│   │   └── banking_steps.py        # Reusable step definitions
│   └── suites/
│       ├── test_smoke_tests.py
│       ├── test_regression_tests.py
│       └── test_security_tests.py
└── core/
    └── spec_generator.py            # LLM-powered spec generator
```

## 🚀 Quick Start

### 1. Generate Test Specifications
```bash
python core/spec_generator.py
```

This uses Claude's banking domain expertise to:
- ✅ Create comprehensive test scenarios
- ✅ Consider regulatory compliance (FDIC, PCI-DSS)
- ✅ Generate feature files in Gherkin format
- ✅ Create reusable step definitions
- ✅ Organize tests into suites

### 2. Review Generated Specs
```bash
cat specs/parabank_spec.json
```

### 3. Customize Step Definitions
Edit `tests/steps/banking_steps.py` to match ParaBank's actual locators.

### 4. Run Test Suites
```bash
# Smoke tests
pytest tests/suites/test_smoke_tests.py

# Full regression
pytest tests/suites/

# Specific feature
pytest tests/suites/ -k "registration"
```

## 📝 Feature File Example

```gherkin
Feature: Account Registration
  Priority: P0
  Compliance: FDIC requires identity verification

  Scenario: New customer registration with valid data
    Given I am on the registration page
    When I fill all required fields with valid data
    Then Account should be created successfully
    And Account confirmation message appears
    And User is redirected to login
```

## 🔧 Step Definition Example

```python
from tests.steps.banking_steps import BankingSteps

def test_registration(page, banking_steps):
    page.goto("https://parabank.parasoft.com/parabank/")
    
    # Navigate
    banking_steps.navigate_to_registration()
    
    # Fill form
    user_data = {
        "firstName": "John",
        "lastName": "Doe",
        "address": "123 Main St",
        "city": "New York",
        "state": "NY",
        "zipCode": "10001",
        "phoneNumber": "555-1234",
        "ssn": "123-45-6789",
        "username": "johndoe123",
        "password": "SecurePass@123"
    }
    banking_steps.fill_registration_form(user_data)
    banking_steps.submit_registration()
    
    # Verify
    banking_steps.verify_registration_success()
```

## 🏦 Banking Domain Coverage

### Critical Features
- ✅ Account Registration (KYC/AML)
- ✅ Login/Logout & Session Management
- ✅ Account Overview & Balance Check
- ✅ Fund Transfer (Internal & External)
- ✅ Bill Payment
- ✅ Transaction History
- ✅ Account Statements
- ✅ Profile Management
- ✅ Security Settings (2FA, Security Questions)

### Compliance Considerations
- **FDIC**: Identity verification, account ownership
- **PCI-DSS**: Secure credential storage, encryption
- **SOC2**: Access controls, audit trails
- **AML**: Transaction monitoring, suspicious activity reporting

## 🧪 Test Suite Organization

### Smoke Tests (Fast, Critical Paths)
- User registration
- Login/Logout
- View account balance
- Simple fund transfer

### Regression Tests (Comprehensive)
- All features + edge cases
- Cross-browser compatibility
- Mobile responsiveness

### Security Tests (Penetration Focus)
- SQL injection attempts
- XSS prevention
- CSRF token validation
- Session hijacking prevention
- Password complexity enforcement

## 📊 Test Execution

```bash
# Generate fresh specs (if ParaBank changes)
python core/spec_generator.py

# Run with coverage
pytest tests/suites/ --cov=tests --cov-report=html

# Run in parallel
pytest tests/suites/ -n auto

# Generate Allure report
pytest tests/suites/ --alluredir=allure-results
allure serve allure-results
```

## 🔄 Integration with Autonomous Agent

The spec generator works with the autonomous explorer:

```bash
# Run autonomous test against ParaBank
python run.py \
  --project parabank_transfer \
  --url "https://parabank.parasoft.com/parabank/" \
  --goal "Execute fund transfer" \
  --domain "banking"

# Generated test will be added to Knowledge Bank
# Future runs become faster and more accurate
```

## 📈 Advanced Usage

### Custom Domain Specifications
Edit `core/spec_generator.py` to add your organization's specific requirements:

```python
CUSTOM_REQUIREMENTS = """
- Support multi-currency transactions
- Handle international wire transfers
- Comply with GDPR for EU customers
- Support mobile check deposit
"""
```

### Extend Step Definitions
```python
class BankingSteps:
    def transfer_with_forex(self, amount, from_currency, to_currency):
        """Transfer with foreign exchange"""
        # Custom implementation
        pass
```

## 🎯 Next Steps

1. ✅ Generate specs: `python core/spec_generator.py`
2. 📝 Review `specs/features/*.feature`
3. 🔧 Customize `tests/steps/banking_steps.py`
4. 🧪 Run: `pytest tests/suites/`
5. 📊 View reports in `allure-results/`

---

**Generated by**: AI-Powered Test Specification Generator  
**Domain Expertise**: Banking & Financial Services  
**Compliance**: FDIC, PCI-DSS, SOC2, AML
