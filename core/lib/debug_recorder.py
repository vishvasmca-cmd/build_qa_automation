import os
import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional

class DebugRecorder:
    """
    Records detailed execution steps, AI decisions, and screenshots
    to generate an interactive HTML debug report.
    """
    def __init__(self, session_id: str, output_dir: str):
        self.session_id = session_id
        self.output_dir = os.path.abspath(output_dir)
        self.steps = []
        self.start_time = time.time()
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        self.report_path = os.path.join(self.output_dir, f"debug_report_{session_id}.html")

    def record_step(self, step_name: str, status: str, details: Dict[str, Any], screenshot: str = None):
        """
        Record a single execution step.
        """
        step_data = {
            "timestamp": datetime.now().isoformat(),
            "elapsed": round(time.time() - self.start_time, 2),
            "step": step_name,
            "status": status,  # "running", "passed", "failed", "info"
            "details": details, # Dict containing logs, locators, AI reasoning
            "screenshot": screenshot # Base64 string
        }
        self.steps.append(step_data)
        self._flush_report()

    def record_ai_decision(self, step_name: str, prompt: str, response: Dict, candidates: List[Dict] = None):
        """
        Record an AI decision (Explorer/Planner/Smart Locator).
        """
        self.record_step(
            step_name=step_name,
            status="info",
            details={
                "type": "ai_decision",
                "prompt_summary": prompt[:500] + "..." if len(prompt) > 500 else prompt,
                "response": response,
                "candidates": candidates or []
            }
        )

    def _flush_report(self):
        """
        Generate/Update the HTML report.
        """
        html = self._generate_html()
        with open(self.report_path, "w", encoding="utf-8") as f:
            f.write(html)

    def _generate_html(self) -> str:
        """
        Generates a standalone HTML report with embedded data.
        """
        # Serialize steps to JSON for JS to consume
        steps_json = json.dumps(self.steps)
        
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Debug Report: {self.session_id}</title>
    <style>
        :root {{ --bg: #0f172a; --card: #1e293b; --text: #e2e8f0; --accent: #3b82f6; --success: #22c55e; --fail: #ef4444; }}
        body {{ font-family: system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 20px; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 1px solid #334155; padding-bottom: 20px; }}
        .timeline {{ max-width: 1000px; margin: 0 auto; }}
        .step-card {{ background: var(--card); border-radius: 8px; padding: 16px; margin-bottom: 16px; border-left: 4px solid var(--accent); }}
        .step-card.passed {{ border-left-color: var(--success); }}
        .step-card.failed {{ border-left-color: var(--fail); }}
        .step-header {{ display: flex; justify-content: space-between; margin-bottom: 10px; font-weight: bold; }}
        .step-details {{ font-family: monospace; background: #0f172a; padding: 10px; border-radius: 4px; overflow-x: auto; white-space: pre-wrap; font-size: 0.9em; }}
        .screenshot {{ margin-top: 10px; border-radius: 4px; border: 1px solid #334155; max-width: 100%; }}
        .json-tree {{ color: #94a3b8; }}
        .badge {{ padding: 2px 6px; border-radius: 4px; font-size: 0.8em; background: #334155; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🐞 Debug Report: {self.session_id}</h1>
        <div>Total Steps: {len(self.steps)} | Duration: {round(time.time() - self.start_time, 2)}s</div>
    </div>
    
    <div class="timeline" id="timeline">
        <!-- Steps will be rendered here by JS -->
    </div>

    <script>
        const steps = {steps_json};
        const container = document.getElementById('timeline');

        steps.forEach((step, index) => {{
            const card = document.createElement('div');
            card.className = `step-card ${{step.status}}`;
            
            let detailsHtml = '';
            
            if (step.details.type === 'ai_decision') {{
                detailsHtml = `
                    <div style="margin-bottom: 5px; color: #60a5fa;">🧠 AI Decision Logic</div>
                    <div class="json-tree">${{JSON.stringify(step.details.response, null, 2)}}</div>
                    ${{step.details.candidates && step.details.candidates.length > 0 ? 
                        `<div style="margin-top: 5px; color: #a3e635;">🏆 Top Candidates:</div>
                         <div class="json-tree">${{JSON.stringify(step.details.candidates, null, 2)}}</div>` : ''}}
                `;
            }} else {{
                detailsHtml = `<div class="json-tree">${{typeof step.details === 'string' ? step.details : JSON.stringify(step.details, null, 2)}}</div>`;
            }}

            const screenshotHtml = step.screenshot ? 
                `<img src="data:image/jpeg;base64,${{step.screenshot}}" class="screenshot" alt="Step Screenshot" />` : '';

            card.innerHTML = `
                <div class="step-header">
                    <span>#${{index + 1}} ${{step.step}}</span>
                    <span class="badge">${{step.elapsed}}s</span>
                </div>
                <div class="step-details">${{detailsHtml}}</div>
                ${{screenshotHtml}}
            `;
            
            container.appendChild(card);
        }});
    </script>
</body>
</html>
"""
