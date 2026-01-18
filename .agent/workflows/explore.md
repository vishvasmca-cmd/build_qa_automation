---
description: Running robust multi-scenario exploration and mining
---
Use this workflow to perform deep, autonomous testing of a website using the latest iterative exploration and self-healing agents.

1. **Initialize Project Directory** (if not already done):
```bash
mkdir projects/your_project_name
```

2. **Run Deep Exploration**:
Run the orchestrator with the `--deep` flag to trigger `DeepExplorerAgent`. This will:
- Run **Discovery** to build a sitemap.
- Run **Planning** to generate multiple end-to-end scenarios.
- Run **Exploration** using the iterative loop with self-healing and smart step IDs.

// turbo
```bash
python orchestrator.py --project projects/your_project_name --goal "Your high-level testing goal" --base_url https://example.com --deep --headed --force
```

3. **Monitor Progress**:
- Check `{project_dir}/deep_explorer_debug.log` for multi-scenario status.
- Check `{project_dir}/explorer_debug.log` for step-by-step AI suggestions and self-healing logs.

4. **Verify Results**:
- Review `{project_dir}/workflow.json` for discovered locators.
- Review `{project_dir}/execution.json` for final pass/fail status.

5. **Troubleshooting**:
- If the browser closes unexpectedly, the agent will catch the error and log "🛑 Browser connection lost". You can re-run with `--force` to resume/restart.
- If the agent gets stuck, check the `Loop detected` warnings in the log.
