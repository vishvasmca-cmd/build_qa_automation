# Antigravity: The Open-Source Autonomous QA Platform 🚀

**Control Your AI. Own Your Code. No Vendor Lock-In.**

Antigravity is the first **Transparent AI** testing platform. Unlike closed-source "black box" tools (Testsigma, Testim) that trap your data, Antigravity uses a **Deterministic + LLM Hybrid** approach to generate **standard, type-safe Playwright code** that you own.

---

## ⚡ Why Antigravity?

| Feature | 🛡️ Antigravity | 📦 Testsigma / Testim | 🎭 Playwright Codegen |
|---------|----------------|-----------------------|-----------------------|
| **AI Transparency** | ✅ **Full Control** (Inspect/Edit Rules) | ❌ Black Box (Hidden Logic) | ❌ N/A |
| **Code Ownership** | ✅ **Standard Python/Pytest** | ❌ Proprietary Format | ✅ Standard Code |
| **Self-Healing** | ✅ **Learns from Failures** | ✅ Yes | ❌ No |
| **Cost** | ✅ **10x Cheaper** (Hybrid AI) | ❌ High SaaS Fees | ✅ Free |
| **Migration** | ✅ **Import Existing Tests** | ❌ Start from Scratch | ❌ start from Scratch |

---

## 🛠️ The "Permanent Fix": Antigravity DSL

We don't guess. We compile.
Our **Type-Safe DSL** separates your *Intent* from *Implementation*.

### Input: `login.yaml` (Human Readable)
```yaml
test_name: corporate_login
base_url: https://app.acme.com

steps:
  - action: fill
    locator: username   # 🪄 Inference: Becomes [name='username']
    value: admin

  - action: fill
    locator: password
    value: secret_key

  - action: click
    locator: submit
    wait_for: visible

  - action: assert
    type: url_contains
    value: dashboard
```

### Output: `test_login.py` (Production Grade)
```python
# 🔒 Type-Safe, Validated, Standard Code
from playwright.sync_api import Page, expect
import re

def test_corporate_login(page: Page):
    page.goto('https://app.acme.com')
    page.locator("[name='username']").fill('admin')
    page.locator("[name='password']").fill('secret_key')
    page.locator("button[type='submit']").click()
    expect(page).to_have_url(re.compile('dashboard'))
```

---

## 🏗️ Architecture

```mermaid
graph TD
    A[Intent (DSL/YAML)] -->|Parse & Validate| B(AST Builder)
    B -->|Inference Engine| C{Heuristics}
    C -->|Output| D[Python/Playwright Code]
    E[Execution Engine] -->|Run| D
    E -->|Failure?| F[Feedback Agent]
    F -->|Learn Pattern| G[Knowledge Bank]
    G -->|Optimize| C
```

1.  **Parser**: Validates YAML against strict Schema.
2.  **Inference Engine**: Resolves semantic names (`username`) to robust locators.
3.  **AST Builder**: Compiles valid Python code (no syntax errors, ever).
4.  **Feedback Loop**: Failures update the **Knowledge Bank**, making the Inference Engine smarter.

---

## 🚀 Quick Start

### 1. Compile a Test
```bash
python -m core.dsl.cli compile tests/dsl/sample_orangehrm.yaml
```

### 2. Run the Test
```bash
python -m pytest tests/dsl/generated_test_orangehrm.py
```

### 3. Watch it Learn
If a test fails due to a popup, the **Explorer Agent** fixes it and saves the rule to `knowledge/sites/example.com/rules.md`. Next time, it proactively handles it!

---

## 🤝 Contributing
Open source and community driven.
- **Core**: `core/engine` (The Brain)
- **DSL**: `core/dsl` ( The Compiler)
- **Knowledge**: `knowledge/` (Shared Learnings)
