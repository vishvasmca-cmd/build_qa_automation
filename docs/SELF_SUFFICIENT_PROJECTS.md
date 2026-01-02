# 📦 Self-Sufficient Test Projects

## ✨ **Every Project is Standalone**

When you run:
```bash
python run.py --project my_bank --url URL --goal GOAL --domain banking
```

**You get a complete, production-ready test automation project that can be shared, run, and maintained independently!**

---

## 📁 **What Gets Created**

```
projects/my_bank/                   # ✅ Self-Contained Project
├── README.md                        # ⭐ Project documentation
├── requirements.txt                 # ⭐ Dependencies
├── pytest.ini                       # ⭐ Pytest configuration
├── .env.example                     # ⭐ Environment template
├── setup.bat                        # ⭐ Windows setup script
├── setup.sh                         # ⭐ Linux/Mac setup script
├── .gitignore                       # ⭐ Git exclusions
├── .github/workflows/tests.yml      # ⭐ CI/CD pipeline
│
├── config/
│   ├── environments.json            # Dev/QA/Prod URLs
│   └── test-data.json               # Credentials (git-ignored)
│
├── tests/e2e/
│   └── test_generated.py            # Your test
│
├── pages/
│   └── *.py                         # Page Object Model
│
├── fixtures/
│   └── conftest.py                  # Pytest fixtures
│
└── outputs/reports/html/
    └── report.html                  # Test results
```

---

## 🚀 **How to Use a Project**

### **1. Clone/Download Project**
```bash
# Someone shares the bank_standalone folder
cd bank_standalone
```

### **2. Run Setup Script**

**Windows**:
```bash
setup.bat
```

**Linux/Mac**:
```bash
chmod +x setup.sh
./setup.sh
```

**What setup does**:
1. Creates Python virtual environment
2. Installs all dependencies from `requirements.txt`
3. Installs Playwright browsers

### **3. Configure**
```bash
# Copy environment template
copy .env.example .env

# Edit with real values
notepad .env

# Update test data
notepad config\test-data.json
```

### **4. Run Tests**
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Run all tests
pytest tests/e2e/ -v

# Run with browser visible
pytest tests/e2e/ -v --headed

# Generate Allure report
pytest tests/e2e/ --alluredir=outputs/allure-results
allure serve outputs/allure-results
```

---

## 📝 **Project README Content**

Each project gets a **custom README.md** with:
- Quick start instructions
- Installation commands
- Test execution examples
- Project structure overview
- Configuration guide
- CI/CD integration

**Example** (`projects/bank_standalone/README.md`):
```markdown
# Bank_Standalone - Test Automation Project

## Quick Start

### Prerequisites
```bash
python --version  # Python 3.11+
```

### Installation
```bash
# Windows
setup.bat

# Linux/Mac
./setup.sh
```

### Run Tests
```bash
pytest tests/e2e/ -v
```
```

---

## 🔧 **requirements.txt - Dependencies**

```txt
# Test Framework
pytest==8.0.0
pytest-playwright==0.5.0
pytest-xdist==3.5.0          # Parallel execution
playwright==1.42.0

# Reporting
allure-pytest==2.13.2
pytest-html==4.1.1

# AI/LLM (if needed)
langchain-google-genai==1.0.10
python-dotenv==1.0.0

# Utilities
pydantic==2.6.0
requests==2.31.0
```

**Why**:
- ✅ Locks all dependency versions
- ✅ Ensures reproducibility
- ✅ Anyone can install exact environment

---

## ⚙️ **pytest.ini - Test Configuration**

```ini
[pytest]
testpaths = tests
python_files = test_*.py

addopts = 
    -v
    --tb=short
    --html=outputs/reports/html/report.html
    --self-contained-html

markers =
    smoke: Quick smoke tests
    regression: Full regression suite
    security: Security-focused tests

# Playwright
base-url = https://parabank.parasoft.com/parabank/
headed = False
browser = chromium
```

**Usage**:
```bash
# Run only smoke tests
pytest -m smoke

# Run with headed browser
pytest --headed

# Override base URL
pytest --base-url=https://qa.example.com
```

---

## 🔐 **.env.example - Environment Template**

```env
# Environment Configuration
# Copy this to .env and fill in real values

# API Keys
GOOGLE_API_KEY=your_gemini_api_key_here

# Test Accounts
TEST_USERNAME=testuser@example.com
TEST_PASSWORD=SecurePass123

# URLs
BASE_URL=https://parabank.parasoft.com/parabank/
API_URL=https://api.example.com

# Playwright
HEADLESS=true
SLOWMO=0
```

**Security**:
- ✅ `.env` is git-ignored
- ✅ Example file shows structure
- ✅ Never commit real credentials

---

## 🔄 **CI/CD Integration**

Each project includes `.github/workflows/tests.yml`:

```yaml
name: Banking Tests

on:
  push:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

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
          TEST_USERNAME: ${{ secrets.TEST_USERNAME }}
          TEST_PASSWORD: ${{ secrets.TEST_PASSWORD }}
        run: pytest tests/e2e/ -v
      
      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: outputs/reports/
```

**Setup**:
1. Push project to GitHub
2. Add secrets: `TEST_USERNAME`, `TEST_PASSWORD`
3. GitHub Actions runs automatically

---

## 📤 **Sharing Projects**

### **Method 1: Git Repository**
```bash
cd projects/my_bank
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-user/my-bank-tests
git push -u origin main
```

**Recipient**:
```bash
git clone https://github.com/your-user/my-bank-tests
cd my-bank-tests
setup.bat  # or ./setup.sh
pytest tests/e2e/ -v
```

### **Method 2: ZIP File**
```bash
# Compress project folder
Compress-Archive -Path projects\my_bank -DestinationPath my_bank_tests.zip
```

**Recipient**:
```bash
# Extract
Expand-Archive my_bank_tests.zip
cd my_bank_tests\my_bank
setup.bat
```

---

## 🎯 **Benefits**

### **For Developers**
✅ **Portable**: Works on any machine  
✅ **Reproducible**: Locked dependencies  
✅ **Documented**: README + comments  
✅ **CI-Ready**: GitHub Actions included  

### **For Teams**
✅ **Standardized**: Same structure across projects  
✅ **Shareable**: Easy to distribute  
✅ **Maintainable**: Clear separation of concerns  
✅ **Scalable**: Add more tests easily  

### **For Organizations**
✅ **Compliance**: Version-controlled test assets  
✅ **Auditable**: Git history of all changes  
✅ **Reusable**: Template for new projects  
✅ **Trainable**: New team members get started fast  

---

## 🔄 **Updating Dependencies**

```bash
# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade pytest

# Regenerate requirements
pip freeze > requirements.txt
```

---

## 🧪 **Example Workflow**

**Day 1**: Generate project
```bash
python run.py --project login_tests --url URL --goal "Login" --domain banking
```

**Day 2**: Teammate clones
```bash
git clone repo
cd login_tests
setup.bat
```

**Day 3**: Add new test
```bash
# Edit tests/e2e/test_login.py
pytest tests/e2e/test_login.py -v
git commit -am "Added MFA test"
```

**Day 4**: CI/CD runs automatically
```
GitHub Actions: ✅ 15 tests passed
```

---

## ✅ **Checklist for Self-Sufficient Projects**

Every project should have:
- [x] README.md with instructions
- [x] requirements.txt with locked versions
- [x] pytest.ini with markers
- [x] .env.example template
- [x] setup.bat / setup.sh scripts
- [x] .gitignore for sensitive files
- [x] .github/workflows/ for CI/CD
- [x] config/ folder for environments
- [x] tests/e2e/ with actual tests
- [x] pages/ for Page Object Model
- [x] outputs/ for reports

---

**🎉 Bottom Line**: Every generated project is a complete, production-ready test automation suite that can be run by anyone, anywhere, with just 2 commands: `setup.bat` and `pytest`!
