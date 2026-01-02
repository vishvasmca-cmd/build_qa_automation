import os
import json
import argparse
import sys
import asyncio

# Add core to path
sys.path.append(os.path.join(os.getcwd(), "core"))

from knowledge_bank import KnowledgeBank
from orchestrator import run_pipeline

async def detect_and_generate_spec(url, project_name):
    """Auto-detect domain and generate comprehensive spec"""
    from playwright.async_api import async_playwright
    from langchain_google_genai import ChatGoogleGenerativeAI
    from dotenv import load_dotenv
    
    load_dotenv()
    
    print(f"\n🔍 Auto-detecting domain for: {url}")
    
    # Step 1: Analyze website
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            title = await page.title()
            content = await page.inner_text("body")
            content_sample = content[:1000]
            
            nav_links = await page.evaluate("""
                () => {
                    const links = Array.from(document.querySelectorAll('nav a, header a, .menu a'));
                    return links.map(a => a.textContent.trim()).slice(0, 20);
                }
            """)
        except Exception as e:
            print(f"   ⚠️ Could not analyze page: {e}")
            await browser.close()
            return "general"
        
        await browser.close()
    
    # Step 2: Classify domain with LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.1)
    
    prompt = f"""
You are a Domain Classification Expert.

Analyze this website and classify it accurately:
URL: {url}
Title: {title}
Navigation: {', '.join(nav_links)}
Content Sample: {content_sample[:500]}

**CLASSIFICATION RULES**:
- ISP/Telecommunications: Internet providers (RCN, Comcast, AT&T), mobile carriers, cable companies
- Utilities: Electric, water, gas companies (not ISPs)
- E-commerce: Online retail, product sales, shopping carts
- Banking/Finance: Banks, credit unions, investment platforms
- SaaS: Cloud software, subscription services, CRM, project management
- Healthcare: Hospitals, patient portals, telehealth, medical records
- Social Media: User-generated content, feeds, messaging
- Government: DMV, tax portals, public services
- Education: LMS, online courses, student portals
- News/Media: News sites, blogs, content platforms
- Entertainment: Streaming, gaming, events

**CONTEXT CLUES**:
- "Bill Pay", "Account Balance", "Service Plan" + Internet/Cable → ISP/Telecom
- "Cart", "Checkout", "Products" → E-commerce
- "Transfer Funds", "Accounts" → Banking
- "Dashboard", "Workspace", "Projects" → SaaS

Output JSON ONLY:
{{
  "domain": "isp_telecom | utilities | ecommerce | banking | saas | healthcare | social_media | government | education | news | entertainment",
  "confidence": "high | medium | low",
  "key_features": ["feature1", "feature2"],
  "reasoning": "Brief explanation of why this classification"
}}
"""
    
    resp = llm.invoke(prompt)
    domain_info = json.loads(resp.content.replace("```json", "").replace("```", "").strip())
    
    print(f"✅ Domain Detected: {domain_info['domain']} (Confidence: {domain_info['confidence']})")
    print(f"   Features: {', '.join(domain_info['key_features'][:3])}")
    
    return domain_info['domain']

def generate_spec_files(url, project_name, domain):
    """Generate comprehensive test specs based on domain"""
    from langchain_google_genai import ChatGoogleGenerativeAI
    from dotenv import load_dotenv
    
    load_dotenv()
    
    print(f"\n📋 Generating {domain} test specification...")
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)
    
    spec_prompt = f"""
Generate a comprehensive test specification for this {domain} application at {url}.

Include critical workflows, edge cases, and domain-specific tests.

Output JSON with structure:
{{
  "critical_workflows": ["workflow1", "workflow2"],
  "test_scenarios": [
    {{
      "name": "scenario",
      "priority": "P0/P1/P2",
      "steps": ["step1", "step2"],
      "expected_result": "result"
    }}
  ],
  "edge_cases": ["case1", "case2"],
  "security_checks": ["check1", "check2"]
}}
"""
    
    resp = llm.invoke(spec_prompt)
    spec = json.loads(resp.content.replace("```json", "").replace("```", "").strip())
    
    # Save spec
    spec_dir = f"projects/{project_name}/specs"
    os.makedirs(spec_dir, exist_ok=True)
    
    with open(f"{spec_dir}/test_spec.json", "w") as f:
        json.dump(spec, f, indent=2)
    
    print(f"✅ Spec saved: {spec_dir}/test_spec.json")
    print(f"   Workflows: {len(spec.get('critical_workflows', []))}")
    print(f"   Scenarios: {len(spec.get('test_scenarios', []))}")
    
    return spec

def main():
    parser = argparse.ArgumentParser(description="🚀 Unified Autonomous Test Framework")
    parser.add_argument("--project", required=True, help="Project name (e.g. saucedemo)")
    parser.add_argument("--url", help="Target Website URL (required for new projects)")
    parser.add_argument("--docs", help="Documentation/Rules for this project")
    parser.add_argument("--goal", help="Specific Test Goal")
    parser.add_argument("--domain", default="auto", help="Domain type (auto/ecommerce/banking/saas)")
    parser.add_argument("--generate-spec", action="store_true", help="Generate comprehensive test spec before execution")
    parser.add_argument("--use-playwright-agents", action="store_true", help="🎭 Use Playwright native Codegen/Trace tools (recommended for production)")
    args = parser.parse_args()

    project_dir = os.path.join("projects", args.project)
    
    # 1. Initialize Project Directory with Standard Structure
    if not os.path.exists(project_dir):
        print(f"📁 Creating new project workspace: {args.project}")
        print("   Using industry-standard test automation structure...")
        
        # Core folders
        os.makedirs(os.path.join(project_dir, "config"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "specs/features"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "specs/test-plans"), exist_ok=True)
        
        # Tests by layer
        os.makedirs(os.path.join(project_dir, "tests/e2e"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "tests/api"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "tests/integration"), exist_ok=True)
        
        # Page Object Model
        os.makedirs(os.path.join(project_dir, "pages"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "components"), exist_ok=True)
        
        # Test infrastructure
        os.makedirs(os.path.join(project_dir, "fixtures"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "utils"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "data"), exist_ok=True)
        
        # Outputs
        os.makedirs(os.path.join(project_dir, "outputs/reports/html"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "outputs/screenshots/passed"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "outputs/screenshots/failed"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "outputs/logs"), exist_ok=True)
        
        # Playwright traces
        os.makedirs(os.path.join(project_dir, "traces/passed"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "traces/failed"), exist_ok=True)
        
        # Knowledge (AI/ML)
        os.makedirs(os.path.join(project_dir, "knowledge/locators"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "knowledge/patterns"), exist_ok=True)
        
        print("   ✅ Standard folder structure created")
        
        # Create self-sufficient project files
        print("   📝 Creating project configuration files...")
        
        # 1. Project README
        readme_content = f"""# {args.project.title()} - Test Automation Project

## 🎯 Quick Start

### **Prerequisites**
```bash
python --version  # Python 3.11+
```

### **Installation**
```bash
# Windows
setup.bat

# Linux/Mac
./setup.sh
```

### **Run Tests**
```bash
# All tests
pytest tests/e2e/ -v

# Specific test
pytest tests/e2e/test_*.py -v --headed

# Generate Allure report
pytest tests/e2e/ --alluredir=outputs/allure-results
allure serve outputs/allure-results
```

### **View Last Test Trace**
```bash
playwright show-trace traces/passed/execution.zip
```

---

## 📁 Project Structure

```
{args.project}/
├── config/             # Environments, test data
├── tests/e2e/          # Test files
├── pages/              # Page objects
├── fixtures/           # Pytest fixtures
└── outputs/reports/    # Test reports
```

---

## ⚙️ Configuration

### **Environments** (`config/environments.json`)
```json
{{
  "dev": {{ "base_url": "https://dev.example.com" }},
  "qa": {{ "base_url": "https://qa.example.com" }}
}}
```

### **Test Data** (`config/test-data.json`)
Edit this file with real credentials (never commit!)

---

## 🚀 CI/CD

GitHub Actions workflow included in `.github/workflows/tests.yml`

---

**Generated by**: Antigravity AI Framework  
**Date**: {args.project}_automation  
**Domain**: {args.domain if hasattr(args, 'domain') else 'unknown'}
"""
        
        with open(os.path.join(project_dir, "README.md"), "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        # 2. requirements.txt
        requirements = """# Test Framework
pytest==8.0.0
pytest-playwright==0.5.0
pytest-xdist==3.5.0
playwright==1.42.0

# Reporting
allure-pytest==2.13.2
pytest-html==4.1.1

# AI/LLM
langchain-google-genai==1.0.10
python-dotenv==1.0.0

# Utilities
pydantic==2.6.0
requests==2.31.0
"""
        
        with open(os.path.join(project_dir, "requirements.txt"), "w") as f:
            f.write(requirements)
        
        # 3. pytest.ini
        pytest_ini = f"""[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
    --color=yes
    --color=yes

markers =
    smoke: Quick smoke tests
    regression: Full regression suite
    security: Security-focused tests
    slow: Tests that take > 1 minute

# Playwright
base-url = {args.url if args.url else "https://example.com"}
headed = False
browser = chromium
slow_mo = 0
"""
        
        with open(os.path.join(project_dir, "pytest.ini"), "w") as f:
            f.write(pytest_ini)
        
        # 4. .env.example
        env_example = f"""# Environment Configuration
# Copy this to .env and fill in real values

# API Keys
GOOGLE_API_KEY=your_gemini_api_key_here

# Test Accounts
TEST_USERNAME=testuser@example.com
TEST_PASSWORD=SecurePass123

# URLs
BASE_URL={args.url if args.url else "https://example.com"}
API_URL=https://api.example.com

# Playwright
HEADLESS=true
SLOWMO=0
"""
        
        with open(os.path.join(project_dir, ".env.example"), "w") as f:
            f.write(env_example)
        
        # 5. setup.bat (Windows)
        setup_bat = """@echo off
echo ========================================
echo Setting up test automation project
echo ========================================

echo.
echo [1/3] Creating virtual environment...
python -m venv venv
call venv\\Scripts\\activate

echo.
echo [2/3] Installing dependencies...
pip install -r requirements.txt

echo.
echo [3/3] Installing Playwright browsers...
playwright install chromium

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Next steps:
echo 1. Copy .env.example to .env
echo 2. Edit config/test-data.json
echo 3. Run: pytest tests/e2e/ -v
echo.
"""
        
        with open(os.path.join(project_dir, "setup.bat"), "w") as f:
            f.write(setup_bat)
        
        # 6. setup.sh (Linux/Mac)
        setup_sh = """#!/bin/bash
echo "========================================"
echo "Setting up test automation project"
echo "========================================"

echo ""
echo "[1/3] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo ""
echo "[2/3] Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "[3/3] Installing Playwright browsers..."
playwright install chromium

echo ""
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env"
echo "2. Edit config/test-data.json"
echo "3. Run: pytest tests/e2e/ -v"
echo ""
"""
        
        with open(os.path.join(project_dir, "setup.sh"), "w") as f:
            f.write(setup_sh)
        
        # Make setup.sh executable (Linux/Mac)
        import stat
        os.chmod(os.path.join(project_dir, "setup.sh"), 
                 os.stat(os.path.join(project_dir, "setup.sh")).st_mode | stat.S_IEXEC)
        
        # 7. .gitignore
        gitignore = """# Virtual Environment
venv/
.venv/
env/

# Environment Variables
.env

# Test Outputs
outputs/
traces/
screenshots/
*.log
__pycache__/
*.pyc
.pytest_cache/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Sensitive Data
config/test-data.json
"""
        
        with open(os.path.join(project_dir, ".gitignore"), "w") as f:
            f.write(gitignore)
        
        # 8. GitHub Actions workflow
        os.makedirs(os.path.join(project_dir, ".github/workflows"), exist_ok=True)
        
        github_workflow = f"""name: {args.project} Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *'  # 2 AM daily

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        playwright install chromium
    
    - name: Run tests
      env:
        TEST_USERNAME: ${{{{ secrets.TEST_USERNAME }}}}
        TEST_PASSWORD: ${{{{ secrets.TEST_PASSWORD }}}}
      run: |
        pytest tests/e2e/ -v \\
          --html=outputs/reports/html/report.html \\
          --alluredir=outputs/allure-results
    
    - name: Upload test results
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: test-results
        path: |
          outputs/reports/
          traces/failed/
    
    - name: Publish Allure Report
      if: always()
      uses: simple-elf/allure-report-action@master
      with:
        allure_results: outputs/allure-results
        allure_history: allure-history
"""
        
        with open(os.path.join(project_dir, ".github/workflows/tests.yml"), "w") as f:
            f.write(github_workflow)
        
        print("   ✅ Self-sufficient project files created")
        print(f"   📦 Project ready at: projects/{args.project}/")
        print(f"   💡 Run 'cd projects/{args.project} && setup.bat' to get started")

    # NEW: Check if using Playwright Native Agents
    if args.use_playwright_agents:
        print("\n🎭 Using Playwright Native Agents Pipeline")
        print("   (Planner → Builder [Codegen] → Executor [Trace] → Healer)")
        
        if not args.url or not args.goal:
            print("❌ Error: --url and --goal required for Playwright agents mode")
            return
        
        from core.playwright_agents import run_playwright_pipeline
        
        # Detect domain if auto
        detected_domain = args.domain
        if args.domain == "auto":
            detected_domain = asyncio.run(detect_and_generate_spec(args.url, args.project))
        
        # Run Playwright-native pipeline
        success = asyncio.run(run_playwright_pipeline(
            project=args.project,
            url=args.url,
            goal=args.goal,
            domain=detected_domain
        ))
        
        print("\n" + "="*70)
        if success:
            print("✅ Playwright Agent Pipeline Complete!")
            print(f"   Test: projects/{args.project}/tests/test_generated.py")
            print(f"   Trace: projects/{args.project}/traces/execution.zip")
            print(f"\n🔍 View trace: playwright show-trace projects/{args.project}/traces/execution.zip")
        else:
            print("⚠️ Test failed. Healing suggestions available.")
        
        return
   
    # ORIGINAL: Custom Explorer/Miner/Refiner Pipeline

    config_path = os.path.join(project_dir, "config.json")
    
    # 2. Domain Detection (if auto)
    detected_domain = args.domain
    if args.url and (args.domain == "auto" or args.generate_spec):
        detected_domain = asyncio.run(detect_and_generate_spec(args.url, args.project))
        
        # Generate comprehensive spec
        if args.generate_spec:
            generate_spec_files(args.url, args.project, detected_domain)
    
    # 3. Manage Config
    if args.url:
        # Create/Update config
        config = {
            "project_name": args.project,
            "target_url": args.url,
            "workflow_description": args.goal or "Standard Exploration",
            "docs": args.docs or "",
            "domain": detected_domain,
            "test_data": {
                "username": "standard_user",
                "password": "secret_sauce",
                "firstName": "John",
                "lastName": "Doe",
                "postalCode": "12345"
            },
            "paths": {
                "trace": f"projects/{args.project}/outputs/trace.json",
                "report": f"projects/{args.project}/outputs/report.md",
                "test": f"projects/{args.project}/tests/e2e/test_main.py",
                "cache": f"projects/{args.project}/knowledge/locator_cache.json"
            }
        }
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        print(f"⚙️ Config updated: {config_path}")
    
    if not os.path.exists(config_path):
        print(f"❌ Error: Project {args.project} exists but has no config.json. Use --url to initialize.")
        return

    # 4. Add docs to Knowledge base
    if args.docs:
        km = KnowledgeBank()
        km.add_manual_docs(args.project, args.docs)

    # 5. Trigger Orchestrator (The Autonomous Agent)
    print(f"\n🤖 Starting Autonomous Pipeline for {args.project}...")
    run_pipeline(config_path)

if __name__ == "__main__":
    main()
