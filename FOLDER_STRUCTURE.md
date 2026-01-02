# 📁 Standard Test Automation Folder Structure

## Current Structure (Basic)
```
projects/{project_name}/
├── knowledge/          # Mined data
├── outputs/            # Reports
├── specs/              # Test specifications
├── tests/              # Test files
└── traces/             # Playwright traces
```

## Recommended Structure (Industry Standard)

```
projects/{project_name}/
├── config/
│   ├── environments.json       # Dev, QA, Staging, Prod URLs
│   ├── test-data.json          # Test accounts, credentials
│   └── selectors.json          # Centralized locators
│
├── specs/                      # BDD/Gherkin Feature Files
│   ├── features/
│   │   ├── account/
│   │   │   ├── registration.feature
│   │   │   ├── login.feature
│   │   │   └── profile.feature
│   │   ├── transactions/
│   │   │   ├── fund-transfer.feature
│   │   │   └── bill-payment.feature
│   │   └── admin/
│   │       └── user-management.feature
│   └── test-plans/
│       ├── smoke.md            # Critical path tests
│       ├── regression.md       # Full suite
│       └── security.md         # Penetration tests
│
├── tests/                      # Test Implementation
│   ├── e2e/                    # End-to-end tests
│   │   ├── test_registration.py
│   │   ├── test_login.py
│   │   └── test_fund_transfer.py
│   ├── integration/            # API + UI integration
│   │   └── test_api_ui_sync.py
│   ├── api/                    # API-only tests
│   │   ├── test_accounts_api.py
│   │   └── test_transactions_api.py
│   ├── visual/                 # Screenshot comparison
│   │   └── test_ui_regression.py
│   └── load/                   # Performance tests
│       └── test_concurrent_logins.py
│
├── pages/                      # Page Object Model
│   ├── base_page.py            # Common page methods
│   ├── login_page.py
│   ├── dashboard_page.py
│   ├── registration_page.py
│   └── transfer_page.py
│
├── components/                 # Reusable UI components
│   ├── header.py               # Navigation header
│   ├── footer.py
│   └── alert.py                # Toast notifications
│
├── fixtures/                   # Pytest fixtures
│   ├── conftest.py             # Shared fixtures
│   ├── auth_fixtures.py        # Login/logout
│   └── data_fixtures.py        # Test data generators
│
├── utils/                      # Helper utilities
│   ├── db_helper.py            # Database queries
│   ├── api_helper.py           # REST client
│   ├── email_helper.py         # Email verification
│   └── screenshot_helper.py    # Custom captures
│
├── data/                       # Static test data
│   ├── users.csv               # Test accounts
│   ├── transactions.json       # Sample data
│   └── assertions.yaml         # Expected results
│
├── outputs/                    # Test execution results
│   ├── reports/
│   │   ├── html/
│   │   │   └── report_2026-01-01.html
│   │   ├── allure/             # Allure report data
│   │   └── junit/              # CI/CD compatible
│   ├── screenshots/
│   │   ├── passed/
│   │   └── failed/
│   ├── videos/                 # Test recordings
│   └── logs/
│       ├── test_2026-01-01.log
│       └── debug.log
│
├── traces/                     # Playwright traces
│   ├── passed/
│   │   └── test_login_2026-01-01.zip
│   └── failed/
│       └── test_transfer_fail.zip
│
├── knowledge/                  # AI/ML learned data
│   ├── locators/
│   │   ├── stable.json         # Proven selectors
│   │   └── fallback.json       # Backup locators
│   └── patterns/
│       └── banking_flows.yaml  # Domain patterns
│
├── docker/                     # Containerization
│   ├── Dockerfile
│   └── docker-compose.yml      # Selenium Grid setup
│
├── .github/                    # CI/CD
│   └── workflows/
│       ├── smoke-tests.yml
│       └── nightly-regression.yml
│
├── pytest.ini                  # Pytest configuration
├── playwright.config.ts        # Playwright config
├── requirements.txt            # Dependencies
├── .env.example                # Environment template
└── README.md                   # Project documentation
```

---

## Key Principles

### 1. **Separation of Concerns**
- **Specs**: What to test (business requirements)
- **Tests**: How to test (implementation)
- **Pages**: Element locators (POM)
- **Fixtures**: Test setup/teardown
- **Utils**: Reusable helpers

### 2. **Test Layers**
```
E2E Tests (User journeys)
    ↓
Integration Tests (API + UI)
    ↓
API Tests (Backend only)
    ↓
Visual Tests (UI consistency)
```

### 3. **Environment Management**
```json
// config/environments.json
{
  "dev": {
    "base_url": "https://dev.parabank.com",
    "api_url": "https://api.dev.parabank.com",
    "timeout": 30000
  },
  "qa": {
    "base_url": "https://qa.parabank.com",
    "api_url": "https://api.qa.parabank.com",
    "timeout": 60000
  },
  "prod": {
    "base_url": "https://parabank.com",
    "api_url": "https://api.parabank.com",
    "timeout": 120000
  }
}
```

Usage:
```bash
pytest --env=qa tests/e2e/
```

---

## Implementation Example

### **Feature File** (`specs/features/account/login.feature`)
```gherkin
Feature: User Login
  As a ParaBank customer
  I want to login to my account
  So that I can access banking services

  Background:
    Given I am on the ParaBank login page

  Scenario: Successful login with valid credentials
    When I enter username "testuser@example.com"
    And I enter password "SecurePass123"
    And I click the "Login" button
    Then I should see the account dashboard
    And I should see "Welcome, Test User"

  Scenario: Failed login with invalid credentials
    When I enter username "invalid@example.com"
    And I enter password "wrongpass"
    And I click the "Login" button
    Then I should see error message "Invalid credentials"
```

### **Page Object** (`pages/login_page.py`)
```python
from pages.base_page import BasePage

class LoginPage(BasePage):
    # Locators
    USERNAME_INPUT = "input[name='username']"
    PASSWORD_INPUT = "input[name='password']"
    LOGIN_BUTTON = "input[type='submit'][value='Log In']"
    ERROR_MESSAGE = ".error"
    
    def __init__(self, page):
        super().__init__(page)
        self.url = "/login"
    
    def login(self, username, password):
        """Perform login action"""
        self.page.locator(self.USERNAME_INPUT).fill(username)
        self.page.locator(self.PASSWORD_INPUT).fill(password)
        self.page.locator(self.LOGIN_BUTTON).click()
    
    def get_error_message(self):
        """Get error message text"""
        return self.page.locator(self.ERROR_MESSAGE).inner_text()
```

### **Test File** (`tests/e2e/test_login.py`)
```python
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

class TestLogin:
    def test_successful_login(self, page, test_user):
        """Test successful login flow"""
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(test_user['email'], test_user['password'])
        
        dashboard = DashboardPage(page)
        assert dashboard.is_loaded()
        assert dashboard.get_welcome_message() == f"Welcome, {test_user['name']}"
    
    def test_invalid_credentials(self, page):
        """Test login with wrong credentials"""
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("invalid@test.com", "wrongpass")
        
        assert login_page.get_error_message() == "Invalid credentials"
```

### **Fixture** (`fixtures/conftest.py`)
```python
import pytest
import json

@pytest.fixture
def test_user():
    """Provide test user credentials"""
    with open('data/users.json') as f:
        users = json.load(f)
    return users['standard_user']

@pytest.fixture
def authenticated_page(page, test_user):
    """Page with user already logged in"""
    from pages.login_page import LoginPage
    login = LoginPage(page)
    login.navigate()
    login.login(test_user['email'], test_user['password'])
    return page
```

---

## CI/CD Integration (`.github/workflows/smoke-tests.yml`)

```yaml
name: Smoke Tests

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install chromium
      
      - name: Run smoke tests
        env:
          ENV: qa
        run: |
          pytest tests/e2e/ -m smoke --alluredir=allure-results
      
      - name: Generate Allure Report
        uses: simple-elf/allure-report-action@master
        with:
          allure_results: allure-results
      
      - name: Upload trace on failure
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-traces
          path: projects/*/traces/failed/
```

---

## Benefits of This Structure

✅ **Scalability**: Easy to add new tests/features  
✅ **Maintainability**: Clear separation, easy to find files  
✅ **Reusability**: Page objects, fixtures, utils  
✅ **CI/CD Ready**: GitHub Actions, Jenkins, GitLab  
✅ **Team Collaboration**: Clear ownership (specs vs implementation)  
✅ **Reporting**: Multiple formats (HTML, Allure, JUnit)  

---

## Migration from Current Structure

```bash
# Old
projects/parabank_clean/
├── tests/test_main.py
└── outputs/report.html

# New
projects/parabank_clean/
├── tests/e2e/test_registration.py
├── pages/registration_page.py
├── fixtures/conftest.py
└── outputs/reports/html/registration_2026-01-01.html
```

**Migration Steps**:
1. Create new folder structure
2. Move `test_main.py` → `tests/e2e/`
3. Extract page locators → `pages/`
4. Move test data → `data/`
5. Update imports
6. Run tests: `pytest tests/e2e/ -v`

---

**Recommendation**: Implement this structure in `run.py` to auto-create these folders for new projects! 🚀
