import os
import sys
import shutil
import re
import json

def export_project(project_name, output_dir, workspace_root=None):
    """
    Exports a project from the workspace into a standalone directory.
    """
    if not workspace_root:
        workspace_root = os.getcwd()
    
    project_source = os.path.join(workspace_root, "projects", project_name)
    if not os.path.exists(project_source):
        print(f"❌ Project '{project_name}' not found in projects directory.")
        return False
    
    # 1. Create structure
    if os.path.exists(output_dir):
        print(f"⚠️ Removing existing directory: {output_dir}")
        shutil.rmtree(output_dir)
        
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "lib"), exist_ok=True)
    # Legacy directories - no longer needed for trace-based execution
    # os.makedirs(os.path.join(output_dir, "tests"), exist_ok=True)
    # os.makedirs(os.path.join(output_dir, "pages"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "outputs"), exist_ok=True)
    
    print(f"🚀 Exporting '{project_name}' to '{output_dir}'...")
    
    # 2. Copy trace.json (primary artifact)
    trace_src = os.path.join(project_source, "outputs", "trace.json")
    if os.path.exists(trace_src):
        shutil.copy(trace_src, os.path.join(output_dir, "outputs", "trace.json"))
        print("✅ Copied trace.json")
    
    # 3. Copy element templates (for visual locator)
    templates_src = os.path.join(project_source, "outputs", "element_templates")
    if os.path.exists(templates_src):
        shutil.copytree(templates_src, os.path.join(output_dir, "outputs", "element_templates"))
        print("✅ Copied visual templates")
    
    # Legacy: Pages and Tests are deprecated
    # # 3. Copy Pages
    # pages_src = os.path.join(project_source, "pages")
    # if os.path.exists(pages_src):
    #     ...
    
    # # 4. Copy and Patch Tests
    # tests_src = os.path.join(project_source, "tests")
    # if os.path.exists(tests_src):
    #     ...

    # 5. Generate requirements.txt
    requirements = [
        "pytest==8.0.0",
        "playwright==1.41.0",
        "pytest-playwright==0.4.3",
        "termcolor==2.4.0",
        "python-dotenv==1.0.1"
    ]
    with open(os.path.join(output_dir, "requirements.txt"), "w") as f:
        f.write("\n".join(requirements))
    print("✅ Generated requirements.txt")

    # 6. Generate README.md
    readme = f"""# Standalone Project: {project_name}

This project was exported from the Antigravity Automation Framework.

## Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\\Scripts\\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install Playwright browsers:
   ```bash
   playwright install
   ```

## Running Tests
Run all tests:
```bash
pytest tests/
```

Run with HTML report:
```bash
pytest tests/ --template=html --output=report.html
```
"""
    with open(os.path.join(output_dir, "README.md"), "w") as f:
        f.write(readme)
    print("✅ Generated README.md")

    # 7. Copy .env if present
    env_src = os.path.join(workspace_root, ".env")
    if os.path.exists(env_src):
        shutil.copy(env_src, os.path.join(output_dir, ".env"))
        print("✅ Copied .env")

    print(f"\n✨ Export successful! Your standalone project is ready at: {output_dir}")
    return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Export an Antigravity project as standalone.")
    parser.add_argument("--name", required=True, help="Name of the project to export")
    parser.add_argument("--output", required=True, help="Output directory for the export")
    args = parser.parse_args()
    
    export_project(args.name, args.output)
