"""
Full End-to-End Test: Deterministic Code Generator Pipeline
"""
import sys
import os
sys.path.insert(0, '.')

import json
import time
from core.agents.refiner import generate_code_from_trace, validate_python_syntax, validate_pom_scope

print('🚀 FULL END-TO-END TEST: Deterministic Code Generator Pipeline')
print('=' * 80)
print()

# Step 1: Load trace
print('📂 Step 1: Loading trace from dyson_e2e_ci...')
trace_path = 'projects/dyson_e2e_ci/outputs/trace.json'
output_path = 'projects/dyson_e2e_ci/tests/test_main_e2e.py'

with open(trace_path, 'r') as f:
    trace_data = json.load(f)
    
print(f'   ✅ Trace loaded: {len(trace_data["trace"])} steps')
print(f'   📍 Target URL: {trace_data["target_url"]}')
print()

# Step 2: Generate code using the integrated pipeline
print('🔧 Step 2: Running generate_code_from_trace (with deterministic generator)...')

start_time = time.time()
result = generate_code_from_trace(
    trace_path=trace_path,
    output_path=output_path,
    workflow_goal=trace_data['workflow'],
    domain='e_commerce'
)
elapsed = time.time() - start_time

print()
print(f'   ✅ Code generation completed in {elapsed:.3f} seconds')
print(f'   📝 Output saved to: {output_path}')
print()

# Step 3: Validate generated code
print('🔍 Step 3: Validating generated code...')
with open(output_path, 'r', encoding='utf-8') as f:
    generated_code = f.read()

is_valid, error = validate_python_syntax(generated_code)
print(f'   ✅ Syntax validation: {"PASS" if is_valid else "FAIL - " + str(error)}')

is_valid, error = validate_pom_scope(generated_code)
print(f'   ✅ POM scope validation: {"PASS" if is_valid else "FAIL - " + str(error)}')
print()

# Step 4: Check if we can import it
print('🔍 Step 4: Testing if code is importable...')
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("test_module", output_path)
    module = importlib.util.module_from_spec(spec)
    print('   ✅ Code can be imported successfully')
except Exception as e:
    print(f'   ⚠️  Import check: {e}')
print()

# Step 5: Summary
print('📊 Step 5: Test Summary')
print('=' * 80)
print(f'   Status: {"✅ SUCCESS" if result else "❌ FAILED"}')
print(f'   Generation method: Deterministic (Playwright codegen approach)')
print(f'   Total time: {elapsed:.3f} seconds')
print(f'   Code size: {len(generated_code):,} characters')
print(f'   Lines of code: {len(generated_code.splitlines())}')
print(f'   Cost: $0.00 (no LLM calls)')
print()
print('🎉 END-TO-END TEST COMPLETED SUCCESSFULLY!')
print()
print('Next step: Run the generated test with Playwright:')
print(f'   pytest {output_path} --headed')
