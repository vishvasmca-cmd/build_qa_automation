
import os
import json

targets = [
    {
        "project_name": "verify_stress_demoblaze",
        "target_url": "https://www.demoblaze.com/",
        "domain": "demoblaze_com",
        "max_depth": 3,
        "max_steps": 25,
        "mode": "deep_exploration"
    },
    {
        "project_name": "verify_stress_parabank",
        "target_url": "https://parabank.parasoft.com/parabank/index.htm",
        "domain": "parabank_com",
        "max_depth": 3,
        "max_steps": 25,
        "mode": "deep_exploration"
    },
    {
        "project_name": "verify_stress_orangehrm",
        "target_url": "https://opensource-demo.orangehrmlive.com/",
        "domain": "orangehrm_com",
        "max_depth": 3,
        "max_steps": 25,
        "mode": "deep_exploration"
    }
]

base_dir = "projects"
for t in targets:
    p_dir = os.path.join(base_dir, t["project_name"])
    os.makedirs(p_dir, exist_ok=True)
    
    config_path = os.path.join(p_dir, "config.json")
    with open(config_path, "w") as f:
        json.dump(t, f, indent=4)
    print(f"Created {config_path}")
