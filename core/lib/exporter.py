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
    os.makedirs(os.path.join(output_dir, "tests"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "pages"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "outputs", "screenshots"), exist_ok=True)
    
    print(f"🚀 Exporting '{project_name}' to '{output_dir}'...")
    
    # 2. Copy Helpers
    helpers_src = os.path.join(workspace_root, "core", "lib", "templates", "helpers.py")
    if os.path.exists(helpers_src):
        shutil.copy(helpers_src, os.path.join(output_dir, "lib", "helpers.py"))
        print("✅ Copied helpers.py")
    
    # 3. Copy Pages
    pages_src = os.path.join(project_source, "pages")
    if os.path.exists(pages_src):
        for item in os.listdir(pages_src):
            s = os.path.join(pages_src, item)
            d = os.path.join(output_dir, "pages", item)
            if os.path.isdir(s):
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)
        print("✅ Copied page objects")

    # 4. Copy and Patch Tests
    tests_src = os.path.join(project_source, "tests")
    if os.path.exists(tests_src):
        for item in os.listdir(tests_src):
            if item.endswith(".py"):
                with open(os.path.join(tests_src, item), "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Patch dynamic path discovery block
                # This regex targets the block starting with # Dynamic path discovery and ending before class definitions
                dynamic_path_pattern = re.compile(r"# Dynamic path discovery:.*?(?=class|def)", re.DOTALL)
                content = dynamic_path_pattern.sub(
                    "# Standalone path initialization\n"
                    "sys.path.append(os.path.join(os.path.dirname(__file__), '..'))\n"
                    "from lib.helpers import take_screenshot\n\n", 
                    content
                )
                
                # Cleanup: Remove original helper imports if they survived
                content = content.replace("from helpers import take_screenshot", "")
                # Remove duplicate sys/os imports if any
                lines = content.splitlines()
                # Simple deduplication for common imports at top
                new_lines = []
                seen_imports = set()
                for line in lines:
                    if line.strip() in ["import sys", "import os", "import pytest", "import re"]:
                        if line.strip() not in seen_imports:
                            new_lines.append(line)
                            seen_imports.add(line.strip())
                    else:
                        new_lines.append(line)
                content = "\n".join(new_lines)
                
                with open(os.path.join(output_dir, "tests", item), "w", encoding="utf-8") as f:
                    f.write(content)
        print("✅ Patched and copied tests")

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
