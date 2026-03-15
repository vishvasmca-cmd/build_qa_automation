# 🎯 QUICK START - Run Your First Test Now!

## ✨ **Your Framework is Ready!**

Generate production-grade test automation in one command.

---

## 🚀 **1. Generate New Project**

Use the standard naming convention: `WEBAPPNAME_playwright_automation`

```bash
python run.py \
  --project parabank_playwright_automation \
  --url "https://parabank.parasoft.com/parabank/" \
  --goal "Register and login" \
  --domain banking
```

**Wait 1-2 minutes** for the AI to explore and generate code.
You'll map see: `✅ Pipeline SUCCESS!`

---

## 🏃 **2. Run the Test**

The test is automatically placed in `tests/e2e/`:

```bash
# Run with browser visible
pytest projects/parabank_playwright_automation/tests/e2e/ -v --headed
```

---

## 📁 **What You Get**

A fully self-contained project:

```
projects/parabank_playwright_automation/
├── tests/e2e/test_main.py       ✅ Executable Test
├── config/                      ✅ Environment Data
├── outputs/report.html          ✅ HTML Report
├── README.md                    ✅ Documentation
├── requirements.txt             ✅ Dependencies
├── setup.bat                    ✅ 1-Click Setup
└── pytest.ini                   ✅ Configuration
```

---

## 🤝 **Sharing**

Zip the folder and send it to anyone! They just run:
1. `setup.bat`
2. `pytest tests/e2e/`

---

**Example Commands**:

| Site | Command |
|------|---------|
| **Banking** | `python run.py --project bank_playwright_automation ...` |
| **Shop** | `python run.py --project shop_playwright_automation ...` |
| **SaaS** | `python run.py --project saas_playwright_automation ...` |

---

**🎉 Happy Testing!**
