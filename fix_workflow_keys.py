import json
import os

# Hardcoded absolute path using forward slashes (safe)
path = "c:/Users/vishv/.gemini/antigravity/playground/inner-event/projects/ci_automation_exercise/workflow.json"
path = os.path.normpath(path)

print(f"Target: {path}")

if not os.path.exists(path):
    print("Does not exist!")
    try:
        parent = os.path.dirname(path)
        if os.path.exists(parent):
            print(f"Listing {parent}:")
            print(os.listdir(parent))
        else:
            print(f"Parent {parent} does not exist.")
    except Exception as e:
        print(e)
    exit(1)

with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

count = 0
for scenario in data.get("scenarios", []):
    for step in scenario.get("steps", []):
        if "arguments" in step:
            step["args"] = step.pop("arguments")
            count += 1
        if "locators" not in step:
            step["locators"] = []

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"Fixed {count} steps!")
