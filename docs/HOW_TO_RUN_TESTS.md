# 🚀 Running Tests - Complete Guide

## 📍 **Where You Are**

After running:
```bash
python trigger_agent.py projects/my_bank/config.json
```

You have a project in: `projects/my_bank/`

---

## 🎯 **Quick Start - Run Tests Immediately**

### **Option 1: From Parent Directory** (Easiest)
```bash
# You're here: inner-event/
pytest projects/my_bank/tests/test_main.py -v
```

### **Option 2: From Project Directory**
```bash
cd projects/my_bank
pytest tests/test_main.py -v
```

---

## 🔧 **Setup First Time**

If you are setting up the environment from scratch (e.g., after cloning `inner-event`):

### **Install Dependencies**
```bash
pip install -r requirements.txt
playwright install
```

---

## 🧪 **All Ways to Run Tests**

### **1. Basic Run**
```bash
pytest projects/my_bank/tests/test_main.py -v
```

### **2. With Browser Visible** (See what's happening)
```bash
pytest projects/my_bank/tests/test_main.py -v --headed
```

### **3. Slow Motion** (Debugging)
```bash
pytest projects/my_bank/tests/test_main.py -v --headed --slowmo=1000
```

### **4. Stop on First Failure**
```bash
pytest projects/my_bank/tests/test_main.py -v -x
```

### **5. Rerun Failed Tests**
```bash
pytest projects/my_bank/tests/test_main.py -v --lf
```

### **6. With Tracing** (Full Playwright trace)
```bash
pytest projects/my_bank/tests/test_main.py -v --tracing=on
```

---

## 🎬 **View Test Trace** (Debug Tool)

After test runs, view the Playwright trace:

```bash
# View specific trace
playwright show-trace projects/my_bank/outputs/trace.zip
```

**What you see**:
- 🎬 Action timeline
- 📸 Screenshots at each step
- 🌐 Network requests
- 🔍 DOM snapshots
- 📊 Console logs
- 🐛 Errors with stack traces

---

## ⚙️ **Configuration**

Tests are configured via `projects/my_bank/config.json`.
The generic agent uses this config to generate the test code.

---

## 📊 **Viewing Results**

### **1. HTML Report**
```bash
# Open in browser
explorer projects\my_bank\outputs\report.md
```
*(Note: Default reporting generates Markdown/JSON. HTML reports require `pytest-html`)*

### **2. Console Output**
```bash
# Verbose output
pytest projects/my_bank/tests/test_main.py -v
```

---

## 🐛 **Debugging Tips**

### **1. Pause Test Execution**
Add `page.pause()` to the test code:
```python
def test_autonomous_flow(browser):
    # ...
    page.pause()  # Browser pauses, shows inspector
```

### **2. Step Through Test**
```bash
# Run with debugger
pytest projects/my_bank/tests/test_main.py -v --pdb
```

### **3. Verbose Logging**
```bash
pytest projects/my_bank/tests/test_main.py -v --log-cli-level=DEBUG
```

---

## 📞 **Quick Reference**

| Command | Purpose |
|---------|---------|
| `pytest projects/{proj}/tests/test_main.py -v` | Run tests |
| `pytest ... -v --headed` | Show browser |
| `pytest ... -v -x` | Stop on first failure |
| `pytest ... -v --lf` | Rerun last failed |
| `playwright show-trace ...` | Debug failures |

---

**🎉 You're ready to run tests! Start with `pytest projects/{name}/tests/test_main.py -v --headed` to see it in action.**
