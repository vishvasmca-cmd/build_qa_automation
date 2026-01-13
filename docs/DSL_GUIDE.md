# Antigravity DSL Guide

## Why a DSL?
Writing raw Playwright/Selenium code is fragile.
- **Fragile Logic**: `if ... else` spaghetti code.
- **Hard to Read**: Non-engineers can't review Python code.
- **Maintenance**: Changing a locator might require regex-replacing 50 files.

The **Antigravity DSL** solves this by separating **Intent** (YAML) from **Implementation** (Python).

## The "Permanent Fix"
We use **AST (Abstract Syntax Tree)** generation. We don't just "paste strings together". We compile your strict YAML into valid, type-safe Python code. If your YAML is invalid, the compiler stops you *before* generating broken tests.

---

## Quick Start
Create a file `my_test.yaml`:

```yaml
test_name: login_flow
base_url: https://example.com

steps:
  # 1. Semantic Locators (Inference)
  - action: fill
    locator: username  # Automatically becomes [name='username']
    value: admin

  - action: fill
    locator: password
    value: secret123

  # 2. Strict Actions
  - action: click
    locator: submit
    wait_for: visible

  # 3. Robust Assertions
  - action: assert
    type: url_contains
    value: dashboard
```

Run the compiler:

```bash
python -m core.dsl.cli compile my_test.yaml --output test_login.py
```

It generates perfect Python:

```python
def test_login_flow(page: Page):
    page.goto('https://example.com')
    page.locator("[name='username']").fill('admin')
    # ...
    expect(page).to_have_url(re.compile('dashboard'))
```

---

## Capabilities

### 1. Locator Inference
Don't waste time inspecting elements. Just use semantic names:
- `username` -> `[name='username']`, `[id='user-name']`, etc.
- `password` -> `[name='password']`, `[type='password']`
- `submit` -> `button[type='submit']`
- `search` -> `[name='q']`, `[name='search']`

### 2. Available Actions

| Action | params | Description |
|--------|--------|-------------|
| `login` | `username`, `password` | automated login macro |
| `navigate` | `url` | `page.goto(url)` |
| `click` | `locator` | Click an element |
| `fill` | `locator`, `value` | Fill input text |
| `assert` | `type`, `value` | Verify state (`url_contains`, `text_visible`) |

---

## Architecture
1. **Parser**: Validates YAML against Pydantic schema.
2. **Inference Engine**: Resolves `username` to locators.
3. **AST Builder**: Constructs Python `ast` nodes (Import, FunctionDef, Call).
4. **Unparser**: Writes formatted Python code.
