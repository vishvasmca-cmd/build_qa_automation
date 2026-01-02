# 🎭 **NEW: Playwright Native Agents Mode**

## Overview

Instead of custom Explorer/Miner/Refiner, leverage **Playwright's built-in tools**:
- ✅ **Codegen**: Records actions as you perform them
- ✅ **Trace Viewer**: Visual timeline debugging
- ✅ **Inspector**: Interactive element selector

---

## Architecture

```
Planner Agent
    ↓ Creates test strategy from goal + domain
Builder Agent  
    ↓ Uses Playwright Codegen to record OR generates programmatically
Executor Agent
    ↓ Runs with full tracing (screenshots, snapshots, network)
Healer Agent
    ↓ Analyzes failures → Suggests fixes via LLM
```

---

## Usage

### **Enable Playwright Agents Mode**
```bash
python run.py \
  --project my_test \
  --url "https://example.com" \
  --goal "Login and checkout" \
  --domain auto \
  --use-playwright-agents
```

**What happens**:
1. **Planner** creates step-by-step test plan
2. **Builder** generates Playwright test code
3. **Executor** runs test with full trace recording
4. **Healer** (if fails) suggests alternative locators
5. **Trace Viewer** opens for visual debugging

---

## Benefits Over Custom Mode

| Feature | Custom Mode | Playwright Agents |
|---------|-------------|------------------|
| Code Generation | LLM-based | Playwright Codegen ✅ |
| Debugging | Screenshots only | Full trace timeline ✅ |
| Locator Healing | Custom logic | Playwright Inspector ✅ |
| Manual Recording | Not supported | Codegen UI ✅ |
| Network Logs | Not captured | Full HAR export ✅ |
| Time-travel Debug | No | Trace Viewer ✅ |

---

## Outputs

```
projects/my_test/
├── test_plan.json              # LLM-generated strategy
├── tests/
│   └── test_generated.py       # Playwright Codegen output
└── traces/
    └── execution.zip           # Full trace (open with `playwright show-trace`)
```

---

## Trace Viewer

**Open trace**:
```bash
playwright show-trace projects/my_test/traces/execution.zip
```

**Features**:
- 🎬 Action timeline
- 📸 Screenshot at each step
- 🌐 Network requests/responses
- 🔍 DOM snapshots
- 📊 Performance metrics
- 🐛 Console logs

---

## Example: RCN Production Test

```bash
python run.py \
  --project rcn_prod \
  --url "https://my.rcn.com/" \
  --goal "Login and view billing" \
  --domain isp_telecom \
  --use-playwright-agents
```

**Output**:
```
🎭 Using Playwright Native Agents Pipeline
   (Planner → Builder [Codegen] → Executor [Trace] → Healer)

[Step 1/4] 📋 Planning...
✅ Plan saved: projects/rcn_prod/test_plan.json

[Step 2/4] 🏗️ Building Test...
✅ Test generated: projects/rcn_prod/tests/test_generated.py

[Step 3/4] 🧪 Executing Test...
✅ Test passed!

✅ Playwright Agent Pipeline Complete!
   Test: projects/rcn_prod/tests/test_generated.py
   Trace: projects/rcn_prod/traces/execution.zip

🔍 View trace: playwright show-trace projects/rcn_prod/traces/execution.zip
```

---

## When to Use Each Mode

### **Use Playwright Agents** (--use-playwright-agents)
✅ Production sites with complex UI  
✅ Need visual debugging  
✅ Manual test recording  
✅ Network/performance analysis  
✅ Stable, maintained by Microsoft  

### **Use Custom Mode** (default)
✅ Training/learning across many sites  
✅ Knowledge Bank accumulation  
✅ Autonomous exploration  
✅ Research/experimentation  

---

## Healer Agent Example

**If test fails**:
```json
{
  "issue": "Locator '#login-button' not found",
  "root_cause": "Element ID changes dynamically",
  "suggested_fix": "Use get_by_role('button', name='Login')",
  "alternative_selectors": [
    "page.get_by_text('Login')",
    "page.locator('[data-test=\"login\"]')",
    "page.locator('button:has-text(\"Login\")')"
  ]
}
```

**Apply fix manually or let Healer auto-retry with alternatives.**

---

## Integration with Knowledge Bank

Even in Playwright mode, learnings are stored:
```yaml
# knowledge/sites/my.rcn.com/meta.yaml
domain: isp_telecom
stable_locators:
  login_button:
    selector: get_by_role("button", name="Sign In")
    method: playwright_codegen
    stability: 10
```

---

## Next Steps

1. **Try both modes** on your site
2. **Compare** trace quality vs custom reports
3. **Choose** based on project needs
4. **Mix**: Use Playwright for critical flows, Custom for exploration

---

**Recommendation**: For production testing (RCN, banking, etc.), use `--use-playwright-agents` for reliability and debugging power.
