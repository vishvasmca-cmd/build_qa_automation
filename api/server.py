
import os
import sys
import json
import uuid
import subprocess
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

app = FastAPI(title="Antigravity Agent API")

# CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanRequest(BaseModel):
    url: str
    goal: str
    email: Optional[str] = None
    project_name: Optional[str] = None

# In-memory status store
# structure: {execution_id: {"status": "running"|"completed"|"failed", "log_file": path, "report_file": path}}
execution_store = {}

def run_agent_worker(execution_id: str, config_path: str, log_path: str):
    """Worker thread to run the agent as a subprocess and capture logs"""
    execution_store[execution_id]["status"] = "running"
    
    try:
        with open(log_path, "w", encoding="utf-8") as logs:
            # Call trigger_agent.py as a subprocess to ensure clean environment and log capture
            process = subprocess.Popen(
                [sys.executable, "trigger_agent.py", config_path],
                cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
                stdout=logs,
                stderr=subprocess.STDOUT,
                text=True
            )
            process.wait()
            
            if process.returncode == 0:
                 execution_store[execution_id]["status"] = "completed"
            else:
                 execution_store[execution_id]["status"] = "failed"
                 logs.write(f"\nAPI: Process exited with code {process.returncode}")
                 
    except Exception as e:
        execution_store[execution_id]["status"] = "failed"
        with open(log_path, "a", encoding="utf-8") as logs:
            logs.write(f"\nAPI CRITICAL ERROR: {str(e)}\n")

@app.post("/scan")
async def start_scan(request: ScanRequest, background_tasks: BackgroundTasks):
    # Generate ID
    execution_id = f"scan_{uuid.uuid4().hex[:8]}"
    project_slug = request.project_name or execution_id
    
    # Setup Paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    project_dir = os.path.join(base_dir, "projects", project_slug)
    os.makedirs(project_dir, exist_ok=True)
    
    # Create Config
    config = {
        "project_name": project_slug,
        "target_url": request.url,
        "workflow_description": request.goal,
        "domain": "general",
        "paths": {
            "test": f"projects/{project_slug}/tests/test_main.py",
            "report": f"projects/{project_slug}/outputs/report.md" 
        }
    }
    
    config_path = os.path.join(project_dir, "config.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
        
    log_path = os.path.join(project_dir, "agent.log")
    
    # Init execution record
    execution_store[execution_id] = {
        "status": "pending",
        "log_path": log_path,
        "project_dir": project_dir,
        "report_path": os.path.join(project_dir, "outputs", "report.md") # Note: trigger_agent defaults to md or html depending on implementation, orchestrator usually creates report.html too
    }
    
    # Launch Background Task
    background_tasks.add_task(run_agent_worker, execution_id, config_path, log_path)
    
    return {
        "execution_id": execution_id,
        "status_url": f"/scan/{execution_id}"
    }

@app.get("/scan/{execution_id}")
async def get_scan_status(execution_id: str):
    if execution_id not in execution_store:
        raise HTTPException(status_code=404, detail="Scan not found")
        
    record = execution_store[execution_id]
    
    # Read logs (tail last 50 lines)
    logs = []
    if os.path.exists(record["log_path"]):
        try:
            with open(record["log_path"], "r", encoding="utf-8") as f:
                # Simple tail
                full_logs = f.readlines()
                logs = full_logs[-50:]
        except:
            logs = ["Reading logs..."]
            
    return {
        "status": record["status"],
        "logs": [l.strip("\n") for l in logs],
        "report_url": f"/reports/{execution_id}/content"
    }

@app.get("/reports/{execution_id}/content")
async def get_report_content(execution_id: str):
    if execution_id not in execution_store:
        raise HTTPException(status_code=404, detail="Scan not found")
        
    record = execution_store[execution_id]
    
    # Try MD first, then HTML
    report_md = record["report_path"]
    report_html = report_md.replace(".md", ".html")
    
    if os.path.exists(report_html):
        return FileResponse(report_html)
    elif os.path.exists(report_md):
        return FileResponse(report_md)
    else:
        return {"content": "Report generation in progress..."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
