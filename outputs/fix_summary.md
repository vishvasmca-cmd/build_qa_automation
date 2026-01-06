# Critical Bug Fixes - January 6, 2026

## Overview
Fixed 3 critical bugs identified from analyzing 183 failures in `knowledge/failures.json`:

---

## 1. ✅ Fixed: NoneType .lower() Error (24 Failures)

**Bug**: `'NoneType' object has no attribute 'lower'` in planning phase

**Root Cause**: `spec_synthesizer.py::generate_master_plan()` was calling `.lower()` on `goal` and `testing_type` parameters without null checks.

**Fix Location**: `core/spec_synthesizer.py` lines 87-93

**Changes**:
```python
# Added defensive null checks
goal = goal or ""
testing_type = testing_type or "smoke"
```

**Impact**: Will eliminate 24 planning phase failures

---

## 2. ✅ Fixed: Unicode Encoding Error (2 Failures + Potential Future Issues)

**Bug**: `UnicodeEncodeError: 'charmap' codec can't encode characters` when printing emojis on Windows

**Root Cause**: Emoji characters (📸, ⚠️) in print statements causing Windows cp1252 encoding errors

**Fix Location**: `core/templates/helpers.py` lines 151-159

**Changes**:
```python
# Replaced emoji print statements with ASCII-safe alternatives
print(f'[SCREENSHOT] Saved: {path}')  # was: print(f'📸 Saved: {path}')
print(f'[WARNING] Screenshot failed: {str(e)}')  # was: print(f'⚠️ Screenshot failed: {e}')
```

**Impact**: Prevents Windows encoding crashes during screenshot operations

---

## 3. 🔍 Remaining Issues to Address

### High Priority:
- **Code Generation Quality** (61 failures): "Failed to generate valid code after 3 refinement loops"
  - Recommendation: Improve prompts in `refiner.py` and add more examples to the LLM
  
- **Explorer Stability** (35 crashes): "Explorer Crashed (Non-zero exit code)"
  - Recommendation: Enhanced error handling and retry logic already in place, but may need debugging specific crash scenarios

### Medium Priority:
- **Code Review Rejections** (11 failures): Quality gate rejecting generated code
  - May improve naturally once code generation quality improves
  
- **Test Execution Failures** (27 failures): Various test runtime errors
  - Includes timeout errors, assertion failures, and incorrect locator syntax
  - These should decrease once better code is generated

---

## Testing Recommendations

1. **Immediate**: Run a batch test to verify the NoneType fix works
2. **Short-term**: Monitor failure rates over next few runs to confirm reductions
3. **Ongoing**: Continue analyzing `knowledge/failures.json` for emerging patterns

---

## Metrics to Monitor

Track these in upcoming runs:
- **Planning phase failures**: Should drop from 24 → ~0
- **Execution UnicodeEncodeError**: Should drop from 2 → 0
- **Overall failure rate**: Currently 183 total, target reduction by ~15% (26 failures)

---

## Next Steps

1. ✅ Commit these fixes
2. 🔄 Run batch stress test to validate
3. 📊 Compare before/after failure metrics
4. 🎯 Tackle code generation quality issues (the biggest remaining problem)
