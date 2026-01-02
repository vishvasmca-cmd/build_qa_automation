# ✨ Fresh Start Guide - Banking Test Automation

## 🎯 **You're All Set!**

Your framework is now **production-ready** with:
- ✅ **Standardized folder structure** (industry best practices)
- ✅ **Two execution modes** (Custom AI + Playwright Native)
- ✅ **Domain-aware testing** (Auto-detects: Banking, E-commerce, SaaS, ISP, etc.)
- ✅ **Self-healing tests** (Auto-repairs broken locators)
- ✅ **Knowledge Bank** (Learns from every run)

---

## 🚀 **Quick Start - ParaBank Banking Test**

### **Command**
```bash
python run.py \
  --project parabank_demo \
  --url "https://parabank.parasoft.com/parabank/" \
  --goal "Register new user and transfer funds" \
  --domain banking
```

### **What Gets Created**

```
projects/parabank_demo/
├── config/
│   ├── environments.json       # Dev/QA/Prod URLs
│   └── test-data.json          # Generated credentials
│
├── specs/
│   ├── features/               # Gherkin scenarios
│   └── test-plans/             # Test strategy docs
│
├── tests/
│   ├── e2e/
│   │   └── test_registration_transfer.py
│   ├── api/                    # Future: API tests
│   └── integration/            # Future: API+UI tests
│
├── pages/
│   ├── login_page.py
│   ├── registration_page.py
│   └── transfer_page.py        # Page Object Model
│
├── fixtures/
│   └── conftest.py             # Pytest fixtures
│
├── outputs/
│   ├── reports/html/
│   │   └── report.html         # Beautiful HTML report
│   └── screenshots/
│       ├── passed/
│       └── failed/
│
└── traces/
    └── passed/execution.zip    # Playwright trace
```

---

## 📋 **Three Ways to Run Tests**

### **1. Fully Autonomous (AI Explorer)**
```bash
python run.py --project test1 --url URL --goal GOAL --domain auto
```
**Best for**: Learning new sites, exploration, knowledge building

### **2. Playwright Native Agents**
```bash
python run.py --project test2 --url URL --goal GOAL --use-playwright-agents
```
**Best for**: Production sites, visual debugging, manual recording

### **3. Custom Spec-Driven**
```bash
python run.py --project test3 --url URL --goal GOAL --domain banking --generate-spec
```
**Best for**: Comprehensive test planning, compliance testing

---

## 📚 **Documentation Index**

| File | Purpose |
|------|---------|
| `README.md` | Framework overview, quick start |
| `ARCHITECTURE.md` | Technical deep-dive |
| `FOLDER_STRUCTURE.md` | ⭐ Project organization (NEW!) |
| `PLAYWRIGHT_AGENTS.md` | Playwright native mode |
| `UNIVERSAL_SPEC_GUIDE.md` | Domain detection details |

---

## 🏦 **Banking Domain - What's Included**

### **Compliance Checks**
- ✅ FDIC identity verification
- ✅ PCI-DSS password requirements
- ✅ AML transaction monitoring
- ✅ SOC2 access controls

### **Test Scenarios**
```
specs/features/account/
├── registration.feature        # KYC compliance
├── login.feature               # MFA, session timeout
└── profile.feature             # PII updates

specs/features/transactions/
├── fund-transfer.feature       # Internal transfers
├── bill-payment.feature        # Payee management
└── statements.feature          # PDF download
```

### **Knowledge Patterns**
```yaml
# knowledge/domains/banking.yaml
common_workflows:
  - Registration → Login → Transfer
  - Login → Pay Bill → Logout
  - View Statement → Download PDF

security_tests:
  - Session timeout (15-30 min)
  - Password complexity (8+ chars, special)
  - SQL injection prevention
  - XSS protection

stable_locators:
  - "[data-test='username']"
  - "input[name='accountNumber']"
  - "button:has-text('Transfer Funds')"
```

---

## 🎨 **Next Steps**

### **1. Run Your First Test**
```bash
# Clean slate - new project with standard structure
python run.py \
  --project my_bank_test \
  --url "https://parabank.parasoft.com/parabank/" \
  --goal "Full registration workflow" \
  --domain banking
```

### **2. Check Outputs**
```bash
# View HTML report (opens in browser)
explorer projects\my_bank_test\outputs\reports\html\report.html

# View Playwright trace
playwright show-trace projects\my_bank_test\traces\passed\execution.zip
```

### **3. Run Generated Test**
```bash
pytest projects/my_bank_test/tests/e2e/*.py -v --headed
```

### **4. Iterate & Refine**
- Edit `projects/my_bank_test/config/test-data.json` with real credentials
- Update `pages/*.py` if locators change
- Add assertions in `tests/e2e/*.py`
- Re-run: `pytest projects/my_bank_test/tests/e2e/ -v`

---

## 🔄 **CI/CD Integration**

### **GitHub Actions** (`.github/workflows/tests.yml`)
```yaml
name: Banking Tests

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 0 * * *'  # Daily

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      - run: playwright install chromium
      
      - name: Run tests
        env:
          BANK_USER: ${{ secrets.BANK_USER }}
          BANK_PASS: ${{ secrets.BANK_PASS }}
        run: |
          pytest projects/*/tests/e2e/ -v \
            --alluredir=allure-results
      
      - name: Upload artifacts
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: traces
          path: projects/*/traces/failed/
```

---

## 💡 **Pro Tips**

### **Tip 1: Reuse Test Data**
```python
# fixtures/conftest.py
import pytest

@pytest.fixture
def banking_user():
    return {
        "username": "testuser@bank.com",
        "password": "SecurePass@123",
        "account_number": "12345678"
    }
```

### **Tip 2: Page Object Inheritance**
```python
# pages/base_page.py
class BasePage:
    def __init__(self, page):
        self.page = page
    
    def wait_for_load(self):
        self.page.wait_for_load_state("networkidle")

# pages/transfer_page.py
from pages.base_page import BasePage

class TransferPage(BasePage):
    def transfer_funds(self, amount, to_account):
        self.page.locator("input[name='amount']").fill(str(amount))
        # ...
```

### **Tip 3: Environment Switching**
```bash
# Development
pytest --env=dev tests/e2e/

# QA
pytest --env=qa tests/e2e/

# Production (read-only tests)
pytest --env=prod tests/e2e/ -m "not destructive"
```

---

## ✅ **Checklist for New Projects**

- [ ] Run `python run.py --project NAME --url URL --goal GOAL --domain DOMAIN`
- [ ] Verify standard folder structure created
- [ ] Check `outputs/reports/html/report.html`
- [ ] Review generated test in `tests/e2e/`
- [ ] Update `config/test-data.json` with real data
- [ ] Run test: `pytest projects/NAME/tests/e2e/ -v`
- [ ] View trace: `playwright show-trace projects/NAME/traces/*/execution.zip`
- [ ] Commit to git (exclude `config/test-data.json`!)
- [ ] Set up CI/CD with GitHub Actions
- [ ] Document in `specs/test-plans/`

---

## 📞 **Support**

**Documentation**: See `FOLDER_STRUCTURE.md` for detailed folder explanations  
**Examples**: Check `projects/parabank_clean/` for banking test sample  
**Traces**: Use `playwright show-trace` for visual debugging  

---

**🎉 You're ready to build world-class test automation! Start with one banking test and scale from there.**

**Last Updated**: 2026-01-01  
**Version**: 2.0 (Standardized Structure + Playwright Agents)
