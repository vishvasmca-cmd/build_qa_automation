
import json
import os
import sys

# HTML Template with Chart.js
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Agent Performance Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; background: #f4f6f8; }
        .container { max-width: 1200px; margin: 0 auto; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }
        .row { display: flex; gap: 20px; }
        .col { flex: 1; }
        h1 { color: #2c3e50; }
        h2 { color: #34495e; font-size: 1.2rem; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #eee; }
        th { background: #f8f9fa; }
        .status-success { color: green; font-weight: bold; }
        .status-failed { color: red; font-weight: bold; }
        .metric-value { font-size: 2rem; font-weight: bold; color: #2980b9; }
        .metric-label { color: #7f8c8d; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Agent Performance Dashboard</h1>
        
        <!-- Key Metrics -->
        <div class="row">
            <div class="card col">
                <div class="metric-value" id="runStatus">-</div>
                <div class="metric-label">Overall Result</div>
            </div>
            <div class="card col">
                <div class="metric-value" id="totalDuration">0s</div>
                <div class="metric-label">Total Duration</div>
            </div>
            <div class="card col">
                <div class="metric-value" id="totalCost">$0.00</div>
                <div class="metric-label">Estimated Cost</div>
            </div>
            <div class="card col">
                <div class="metric-value" id="agentCount">0</div>
                <div class="metric-label">Active Agents</div>
            </div>
        </div>

        <!-- Charts Row 1: Time & Activity -->
        <div class="row">
            <div class="card col">
                <h2>Time per Agent (Seconds)</h2>
                <canvas id="timeChart"></canvas>
            </div>
            <div class="card col">
                <h2>Activity Distribution</h2>
                <canvas id="costChart"></canvas>
            </div>
        </div>

        <!-- Charts Row 2: Failure Analytics -->
        <div class="row" id="failureAnalyticsRow" style="display:none;">
            <div class="card col">
                <h2 style="color:#e74c3c">Failures per Agent</h2>
                <canvas id="failureChart"></canvas>
            </div>
            <div class="card col">
                <h2 style="color:#e67e22">Failure Root Causes</h2>
                <ul id="rootCausesList" style="list-style-type: none; padding: 0;"></ul>
            </div>
        </div>

        <!-- Logs -->
        <div class="card">
            <h2>Execution Log</h2>
            <table id="logTable">
                <thead><tr><th>Agent</th><th>Action</th><th>Duration</th><th>Cost</th><th>Status</th></tr></thead>
                <tbody></tbody>
            </table>
        </div>

        <!-- Failures Section (Visible if any) -->
        <div id="failureCard" class="card" style="display:none; border-left: 5px solid red;">
            <h2 style="color:red">⚠️ Failure Detailed Report</h2>
            <table id="failureTable">
                <thead><tr><th>Agent</th><th>Error</th><th>Context</th><th>Status of Fix</th></tr></thead>
                <tbody></tbody>
            </table>
        </div>
    </div>

    <script>
        const data = __DATA__; // Injected Python Data

        // 1. Populate Metrics
        document.getElementById('totalDuration').innerText = data.summary.total_duration.toFixed(2) + "s";
        document.getElementById('totalCost').innerText = "$" + data.summary.total_cost.toFixed(4);
        
        // 1.5 Determine Status from Executor or Failures
        const statusEl = document.getElementById('runStatus');
        const executorEvent = data.events.find(e => e.agent === "Executor");
        const hasFailures = data.failures.length > 0;

        if (executorEvent && executorEvent.success) {
            statusEl.innerText = "✅ PASSED";
            statusEl.className = "metric-value status-success";
        } else if (hasFailures || (executorEvent && !executorEvent.success)) {
            statusEl.innerText = "❌ FAILED";
            statusEl.className = "metric-value status-failed";
        } else {
            statusEl.innerText = "IN PROGRESS";
            statusEl.style.color = "#f39c12";
        }
        
        // 2. Process Chart Data
        const agentStats = {};
        const failureStats = {};
        
        data.events.forEach(e => {
            if (!agentStats[e.agent]) agentStats[e.agent] = { duration: 0, count: 0 };
            agentStats[e.agent].duration += e.duration;
            agentStats[e.agent].count += 1;
        });

        data.failures.forEach(f => {
            if (!failureStats[f.agent]) failureStats[f.agent] = 0;
            failureStats[f.agent] += 1;
        });

        const labels = Object.keys(agentStats);
        const durations = labels.map(l => agentStats[l].duration);
        const counts = labels.map(l => agentStats[l].count);
        
        const failureLabels = Object.keys(failureStats);
        const failureCounts = failureLabels.map(l => failureStats[l]);

        document.getElementById('agentCount').innerText = labels.length;

        // 3. Render Charts
        new Chart(document.getElementById('timeChart'), {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Total Duration (s)',
                    data: durations,
                    backgroundColor: '#3498db'
                }]
            }
        });

        new Chart(document.getElementById('costChart'), {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: counts,
                    backgroundColor: ['#e74c3c', '#2ecc71', '#f1c40f', '#9b59b6', '#34495e']
                }]
            }
        });

        if (hasFailures) {
            document.getElementById('failureAnalyticsRow').style.display = 'flex';
            new Chart(document.getElementById('failureChart'), {
                type: 'bar',
                data: {
                    labels: failureLabels,
                    datasets: [{
                        label: 'Failure Count',
                        data: failureCounts,
                        backgroundColor: '#e74c3c'
                    }]
                }
            });

            // Populate Root Causes
            const rcList = document.getElementById('rootCausesList');
            const uniqueCauses = [...new Set(data.failures.map(f => f.error))];
            uniqueCauses.slice(0, 5).forEach(cause => {
                const li = document.createElement('li');
                li.style.marginBottom = '10px';
                li.innerHTML = `<span style="color:#e74c3c; font-weight:bold;">•</span> ${cause.substring(0, 100)}${cause.length > 100 ? '...' : ''}`;
                rcList.appendChild(li);
            });
        }

        // 4. Populate Tables
        const tbody = document.querySelector('#logTable tbody');
        data.events.forEach(e => {
            const row = `<tr>
                <td>${e.agent}</td>
                <td>${e.action}</td>
                <td>${e.duration.toFixed(2)}s</td>
                <td>$${e.cost}</td>
                <td class="${e.success ? 'status-success' : 'status-failed'}">${e.success ? 'OK' : 'FAIL'}</td>
            </tr>`;
            tbody.innerHTML += row;
        });

        if (hasFailures) {
            document.getElementById('failureCard').style.display = 'block';
            const fbody = document.querySelector('#failureTable tbody');
            data.failures.forEach(f => {
                // Improved Fix Status Logic
                let fixStatus = '<span style="color:#e74c3c">Failed</span>';
                
                // Check if any subsequent event from SAME agent was successful
                const subsequentSuccess = data.events.some(e => 
                    e.agent === f.agent && 
                    e.end_time > f.timestamp && 
                    e.success === true
                );

                if (subsequentSuccess) {
                    fixStatus = '<span style="color:green; font-weight:bold;">Fixed (Retry)</span>';
                } else if (executorEvent && executorEvent.success) {
                    fixStatus = '<span style="color:green; font-weight:bold;">Self-Healed</span>';
                } else {
                    fixStatus = '<span style="color:#f39c12">Pending / Fatal</span>';
                }

                const row = `<tr>
                    <td>${f.agent}</td>
                    <td style="color:red">${f.error}</td>
                    <td>${JSON.stringify(f.context)}</td>
                    <td>${fixStatus}</td>
                </tr>`;
                fbody.innerHTML += row;
            });
        }
    </script>
</body>
</html>
"""

def generate_dashboard(metrics_path=None, output_path=None):
    metrics_path = metrics_path or os.path.join("outputs", "metrics.json")
    output_path = output_path or os.path.join("outputs", "dashboard.html")
    
    if not os.path.exists(metrics_path):
        print(f"❌ Metrics file not found: {metrics_path}")
        return

    with open(metrics_path, "r") as f:
        data = json.load(f)

    html = DASHBOARD_TEMPLATE.replace("__DATA__", json.dumps(data))
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
        
    print(f"✅ Dashboard generated: {output_path}")

if __name__ == "__main__":
    import sys
    metrics_path = sys.argv[1] if len(sys.argv) > 1 else None
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    generate_dashboard(metrics_path, output_path)
