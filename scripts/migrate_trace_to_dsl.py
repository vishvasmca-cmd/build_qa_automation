import sys
import os
import json
from core.lib.dsl_generator import DSLGenerator
from core.dsl.cli import main as compiler_main

def migrate_trace(trace_path: str, output_dir: str):
    """
    Migrate a legacy trace to DSL + Python
    """
    print(f"🔄 Migrating Trace: {trace_path}")
    
    # 1. Load Trace
    with open(trace_path, 'r', encoding='utf-8') as f:
        trace_data = json.load(f)
        
    project_name = os.path.basename(os.path.dirname(os.path.dirname(trace_path)))
    test_name = f"migrated_{project_name}"
    
    # 2. Generate DSL
    generator = DSLGenerator()
    dsl_model = generator.generate_dsl(trace_data, test_name=test_name)
    
    # 3. Save YAML
    yaml_path = os.path.join(output_dir, f"{test_name}.yaml")
    generator.save_to_yaml(dsl_model, yaml_path)
    print(f"✨ Generated DSL: {yaml_path}")
    
    # 4. Compile to Python
    py_path = os.path.join(output_dir, f"test_{test_name}.py")
    print(f"🔨 Compiling to Python: {py_path}")
    
    # Invoke CLI programmatically
    sys.argv = ["cli.py", "compile", yaml_path, "--output", py_path]
    compiler_main()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python migrate_trace_to_dsl.py <trace_path> <output_dir>")
        sys.exit(1)
        
    migrate_trace(sys.argv[1], sys.argv[2])
