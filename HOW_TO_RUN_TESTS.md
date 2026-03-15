# 🚀 Running Tests - Complete Guide

## 📍 **Where You Are**

After running:
```bash
python run.py --project my_bank --url URL --goal GOAL --domain banking
```

You have a project in: `projects/my_bank/`

---

## 🎯 **Quick Start - Run Tests Immediately**

### **Option 1: From Parent Directory** (Easiest)
```bash
# You're here: inner-event/
pytest projects/my_bank/tests/e2e/ -v
```

### **Option 2: From Project Directory** (Standalone)
```bash
cd projects/my_bank
pytest tests/e2e/ -v
```

---

## 🔧 **Setup First Time (If Shared Project)**

If someone sent you just the project folder:

### **Windows**
```bash
cd projects/my_bank
setup.bat
```

### **Linux/Mac**
```bash
cd projects/my_bank
chmod +x setup.sh
./setup.sh
```

**What it does**:
1. Creates virtual environment (`venv/`)
2. Installs dependencies from `requirements.txt`
3. Installs Playwright browsers

---

## 🧪 **All Ways to Run Tests**

### **1. Basic Run**
```bash
pytest projects/my_bank/tests/e2e/ -v
```

### **2. With Browser Visible** (See what's happening)
```bash
pytest projects/my_bank/tests/e2e/ -v --headed
```

### **3. Slow Motion** (Debugging)
```bash
pytest projects/my_bank/tests/e2e/ -v --headed --slowmo=1000
```

### **4. Specific Test File**
```bash
pytest projects/my_bank/tests/e2e/test_registration.py -v
```

### **5. Specific Test Function**
```bash
pytest projects/my_bank/tests/e2e/test_registration.py::test_new_user_signup -v
```

### **6. Only Smoke Tests** (Markers)
```bash
pytest projects/my_bank/tests/e2e/ -v -m smoke
```

### **7. Parallel Execution** (Faster)
```bash
pytest projects/my_bank/tests/e2e/ -v -n auto
```

### **8. Stop on First Failure**
```bash
pytest projects/my_bank/tests/e2e/ -v -x
```

### **9. Rerun Failed Tests**
```bash
pytest projects/my_bank/tests/e2e/ -v --lf
```

### **10. Generate HTML Report**
```bash
pytest projects/my_bank/tests/e2e/ -v \
  --html=projects/my_bank/outputs/reports/html/report.html \
  --self-contained-html
```

### **11. Generate Allure Report** (Beautiful)
```bash
# Run with Allure
pytest projects/my_bank/tests/e2e/ -v --alluredir=projects/my_bank/outputs/allure-results

# View report
allure serve projects/my_bank/outputs/allure-results
```

### **12. With Tracing** (Full Playwright trace)
```bash
pytest projects/my_bank/tests/e2e/ -v --tracing=on
```

---

## 🎬 **View Test Trace** (Debug Tool)

After test runs, view the Playwright trace:

```bash
# View specific trace
playwright show-trace projects/my_bank/traces/passed/execution.zip

# View failed test trace
playwright show-trace projects/my_bank/traces/failed/test_*.zip
```

**What you see**:
- 🎬 Action timeline
- 📸 Screenshots at each step
- 🌐 Network requests
- 🔍 DOM snapshots
- 📊 Console logs
- 🐛 Errors with stack traces

---

## ⚙️ **Configuration Options**

### **Using pytest.ini**

Edit `projects/my_bank/pytest.ini`:
```ini
[pytest]
testpaths = tests
addopts = 
    -v
    --headed           # Always show browser
    --slowmo=500       # Slow down 500ms
    --html=outputs/reports/html/report.html

# Playwright
base-url = https://parabank.parasoft.com/parabank/
browser = chromium
```

Then just run:
```bash
pytest projects/my_bank/tests/e2e/
# Uses all settings from pytest.ini
```

### **Using Environment Variables**

Create `.env` file:
```env
BASE_URL=https://qa.example.com
TEST_USERNAME=testuser@qa.com
TEST_PASSWORD=SecurePass123
HEADLESS=false
```

Access in test:
```python
import os
from dotenv import load_dotenv

load_dotenv()

def test_login(page):
    page.goto(os.getenv('BASE_URL'))
    # ...
```

Run:
```bash
pytest projects/my_bank/tests/e2e/ -v
```

---

## 📊 **Viewing Results**

### **1. HTML Report**
```bash
# Open in browser
explorer projects\my_bank\outputs\reports\html\report.html
```

### **2. Allure Report**
```bash
allure serve projects/my_bank/outputs/allure-results
```

### **3. Console Output**
```bash
# Verbose output
pytest projects/my_bank/tests/e2e/ -v

# Even more verbose
pytest projects/my_bank/tests/e2e/ -vv
```

### **4. JUnit XML** (For CI/CD)
```bash
pytest projects/my_bank/tests/e2e/ -v --junitxml=projects/my_bank/outputs/junit.xml
```

---

## 🔄 **Common Workflows**

### **Workflow 1: Daily Development**
```bash
# Run with browser visible
pytest projects/my_bank/tests/e2e/test_login.py -v --headed

# Fix issues, rerun
pytest projects/my_bank/tests/e2e/test_login.py -v --headed

# Once working, run all
pytest projects/my_bank/tests/e2e/ -v
```

### **Workflow 2: Pre-Commit Check**
```bash
# Run smoke tests only
pytest projects/my_bank/tests/e2e/ -v -m smoke

# If pass, commit
git add .
git commit -m "Updated login test"
```

### **Workflow 3: CI/CD Pipeline**
```bash
# Run headless with reports
pytest projects/my_bank/tests/e2e/ -v \
  --html=outputs/reports/html/report.html \
  --junitxml=outputs/junit.xml \
  --alluredir=outputs/allure-results
```

### **Workflow 4: Debugging Failed Test**
```bash
# Run single test with trace
pytest projects/my_bank/tests/e2e/test_transfer.py -v --tracing=on --headed

# View trace
playwright show-trace projects/my_bank/traces/failed/test_transfer.zip

# Fix, rerun
pytest projects/my_bank/tests/e2e/test_transfer.py -v
```

---

## 🐛 **Debugging Tips**

### **1. Pause Test Execution**
```python
def test_login(page):
    page.goto(URL)
    page.pause()  # Browser pauses, shows inspector
    # Continue manually or resume programmatically
```

### **2. Step Through Test**
```bash
# Run with debugger
pytest projects/my_bank/tests/e2e/ -v --pdb

# Breakpoint in code
def test_login(page):
    breakpoint()  # Stops here
    page.goto(URL)
```

### **3. Verbose Logging**
```bash
pytest projects/my_bank/tests/e2e/ -v --log-cli-level=DEBUG
```

### **4. Keep Browser Open on Failure**
```bash
pytest projects/my_bank/tests/e2e/ -v --headed --screenshot=on --video=on
```

---

## 🔐 **Running with Different Credentials**

### **Method 1: Environment Variables**
```bash
# Windows
set TEST_USERNAME=admin@bank.com
set TEST_PASSWORD=AdminPass123
pytest projects/my_bank/tests/e2e/ -v

# Linux/Mac
export TEST_USERNAME=admin@bank.com
export TEST_PASSWORD=AdminPass123
pytest projects/my_bank/tests/e2e/ -v
```

### **Method 2: Config File**
Edit `projects/my_bank/config/test-data.json`:
```json
{
  "username": "admin@bank.com",
  "password": "AdminPass123"
}
```

### **Method 3: Command Line Parameter**
```bash
pytest projects/my_bank/tests/e2e/ -v --env=qa
```

---

## 📅 **Scheduled Runs**

### **Windows Task Scheduler**
```bash
# Create batch file: run_nightly.bat
cd C:\path\to\inner-event
venv\Scripts\activate
pytest projects\my_bank\tests\e2e\
```

Schedule in Task Scheduler: Daily at 2 AM

### **Linux Cron**
```bash
# Add to crontab
0 2 * * * cd /path/to/inner-event && source venv/bin/activate && pytest projects/my_bank/tests/e2e/
```

### **GitHub Actions** (Already included!)
`.github/workflows/tests.yml` runs automatically on:
- Every push
- Daily schedule (2 AM)
- Manual trigger

---

## 🎯 **Complete Example Session**

```bash
# 1. Navigate to project
cd C:\Users\vishv\.gemini\antigravity\playground\inner-event

# 2. Check what's there
dir projects\bank_standalone\tests\e2e

# 3. Run smoke tests first
pytest projects\bank_standalone\tests\e2e\ -v -m smoke

# 4. If pass, run all tests with browser visible
pytest projects\bank_standalone\tests\e2e\ -v --headed

# 5. Generate report
pytest projects\bank_standalone\tests\e2e\ -v --html=projects\bank_standalone\outputs\reports\html\report.html --self-contained-html

# 6. Open report
explorer projects\bank_standalone\outputs\reports\html\report.html

# 7. View trace if failed
playwright show-trace projects\bank_standalone\traces\failed\*.zip
```

---

## ✅ **Checklist Before Running**

- [ ] Virtual environment activated (if standalone)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Playwright browsers installed (`playwright install`)
- [ ] `.env` file created from `.env.example`
- [ ] `config/test-data.json` has correct credentials
- [ ] Network/VPN connected (if needed)

---

## 🆘 **Troubleshooting**

### **Problem: `pytest: command not found`**
```bash
# Solution: Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### **Problem: `ModuleNotFoundError: No module named 'playwright'`**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
playwright install
```

### **Problem: `TimeoutError: waiting for locator`**
```bash
# Solution: Run with visible browser to debug
pytest -v --headed --slowmo=1000
```

### **Problem: Test data missing**
```bash
# Solution: Check config file
cat projects/my_bank/config/test-data.json
```

---

## 📞 **Quick Reference**

| Command | Purpose |
|---------|---------|
| `pytest tests/e2e/ -v` | Run all tests |
| `pytest tests/e2e/ -v --headed` | Show browser |
| `pytest tests/e2e/ -v -m smoke` | Smoke tests only |
| `pytest tests/e2e/ -v -x` | Stop on first failure |
| `pytest tests/e2e/ -v --lf` | Rerun last failed |
| `pytest tests/e2e/ -v -n auto` | Run in parallel |
| `playwright show-trace traces/failed/*.zip` | Debug failures |

---

**🎉 You're ready to run tests! Start with `pytest projects/{name}/tests/e2e/ -v --headed` to see it in action.**
