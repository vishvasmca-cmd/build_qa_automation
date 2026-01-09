import json
import os
import shutil

def generate_projects(targets_file, output_dir="projects"):
    if not os.path.exists(targets_file):
        print(f"Error: {targets_file} not found.")
        return

    with open(targets_file, "r") as f:
        targets = json.load(f)

    # We only want 20
    targets = targets[:20]

    os.makedirs(output_dir, exist_ok=True)

    for target in targets:
        project_name = target["project"]
        url = target["url"]
        goal = target["goal"]
        domain = target.get("domain", "general")
        
        project_path = os.path.join(output_dir, project_name)
        os.makedirs(project_path, exist_ok=True)
        os.makedirs(os.path.join(project_path, "outputs"), exist_ok=True)
        os.makedirs(os.path.join(project_path, "tests"), exist_ok=True)
        os.makedirs(os.path.join(project_path, "specs"), exist_ok=True)

        config = {
            "project_name": project_name,
            "target_url": url,
            "workflow_description": goal,
            "domain": domain,
            "paths": {
                "test": f"projects/{project_name}/tests/test_main.py",
                "report": f"projects/{project_name}/outputs/report.md"
            }
        }

        config_path = os.path.join(project_path, "config.json")
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Generated project: {project_name}")

if __name__ == "__main__":
    generate_projects("config/verification_targets.json")
