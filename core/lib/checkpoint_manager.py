"""
Checkpoint Manager for Scenario Resume & Failure Learning

This module provides checkpoint/resume functionality to avoid repeating
successful work on retries and learn from previous failures.

PHASES:
1. Save checkpoints after each successful step (proven locators)
2. Resume from last successful step on retry
3. Learn from failures (avoid repeating failed locators)
"""

import os
import json
from datetime import datetime
from typing import Optional, Dict, List


class CheckpointManager:
    """
    Manages scenario checkpoints and failure logs for smart retries.
    
    Features:
    - Save proven locators after each successful step
    - Resume from failure point (skip successful steps)
    - Log failures for AI learning (avoid repeating mistakes)
    """
    
    def __init__(self, project_dir: str):
        """
        Initialize checkpoint manager.
        
        Args:
            project_dir: Project directory path
        """
        self.project_dir = project_dir
        self.checkpoint_dir = os.path.join(project_dir, "checkpoints")
        self.failure_dir = os.path.join(project_dir, "failures")
        
        # Create directories
        os.makedirs(self.checkpoint_dir, exist_ok=True)
        os.makedirs(self.failure_dir, exist_ok=True)
    
    def _get_checkpoint_path(self, scenario_name: str) -> str:
        """Get checkpoint file path for scenario"""
        safe_name = scenario_name.replace(" ", "_").replace("/", "_")
        return os.path.join(self.checkpoint_dir, f"{safe_name}.json")
    
    def _get_failure_path(self, scenario_name: str) -> str:
        """Get failure log path for scenario"""
        safe_name = scenario_name.replace(" ", "_").replace("/", "_")
        return os.path.join(self.failure_dir, f"{safe_name}_failures.json")
    
    def save_step_success(self, scenario_name: str, step_index: int, 
                         step_data: Dict, locator: str, page_url: str = "") -> None:
        """
        Save successful step to checkpoint.
        
        Args:
            scenario_name: Name of scenario
            step_index: Index of successful step
            step_data: Step dictionary
            locator: Proven locator that worked
            page_url: Current page URL
        """
        checkpoint = self.load_checkpoint(scenario_name) or {
            "scenario_name": scenario_name,
            "completed_steps": [],
            "last_success_index": -1
        }
        
        # Add step to checkpoint
        step_record = {
            "index": step_index,
            "id": step_data.get("id", f"step_{step_index + 1}"),
            "keyword": step_data.get("keyword"),
            "description": step_data.get("args", {}).get("description"),
            "locator": locator,
            "success": True,
            "timestamp": datetime.now().isoformat()
        }
        
        # Update or append
        existing_idx = next((i for i, s in enumerate(checkpoint["completed_steps"]) 
                           if s["index"] == step_index), None)
        if existing_idx is not None:
            checkpoint["completed_steps"][existing_idx] = step_record
        else:
            checkpoint["completed_steps"].append(step_record)
        
        checkpoint["last_success_index"] = step_index
        checkpoint["page_state"] = {
            "url": page_url,
            "timestamp": datetime.now().isoformat()
        }
        
        # Save to file
        checkpoint_path = self._get_checkpoint_path(scenario_name)
        with open(checkpoint_path, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, indent=2)
    
    def load_checkpoint(self, scenario_name: str) -> Optional[Dict]:
        """
        Load checkpoint for scenario.
        
        Returns:
            Checkpoint dict or None if not found
        """
        checkpoint_path = self._get_checkpoint_path(scenario_name)
        if not os.path.exists(checkpoint_path):
            return None
        
        try:
            with open(checkpoint_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None
    
    def get_resume_point(self, scenario_name: str) -> int:
        """
        Get index to resume from (last success + 1).
        
        Returns:
            Step index to start from (0 if no checkpoint)
        """
        checkpoint = self.load_checkpoint(scenario_name)
        if checkpoint and "last_success_index" in checkpoint:
            return checkpoint["last_success_index"] + 1
        return 0
    
    def clear_checkpoint(self, scenario_name: str) -> None:
        """Delete checkpoint for scenario"""
        checkpoint_path = self._get_checkpoint_path(scenario_name)
        if os.path.exists(checkpoint_path):
            os.remove(checkpoint_path)
    
    def log_failure(self, scenario_name: str, step_index: int, 
                   description: str, locator: str, error: str, 
                   method: str = "unknown") -> None:
        """
        Log step failure for AI learning.
        
        Args:
            scenario_name: Name of scenario
            step_index: Index of failed step
            description: Step description
            locator: Locator that failed
            error: Error message
            method: Method used (smart-selector, ai-vision, etc.)
        """
        failures = self.load_failures(scenario_name) or {
            "scenario_name": scenario_name,
            "failures": []
        }
        
        # Find or create failure entry for this step
        step_failures = next((f for f in failures["failures"] 
                            if f["step_index"] == step_index), None)
        
        if not step_failures:
            step_failures = {
                "step_index": step_index,
                "description": description,
                "attempts": []
            }
            failures["failures"].append(step_failures)
        
        # Add attempt
        step_failures["attempts"].append({
            "locator": locator,
            "method": method,
            "error": error,
            "timestamp": datetime.now().isoformat()
        })
        
        # Save to file
        failure_path = self._get_failure_path(scenario_name)
        with open(failure_path, 'w', encoding='utf-8') as f:
            json.dump(failures, f, indent=2)
    
    def load_failures(self, scenario_name: str) -> Optional[Dict]:
        """Load failure log for scenario"""
        failure_path = self._get_failure_path(scenario_name)
        if not os.path.exists(failure_path):
            return None
        
        try:
            with open(failure_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None
    
    def get_failure_context(self, scenario_name: str, step_index: int) -> List[Dict]:
        """
        Get previous failures for specific step (for AI learning).
        
        Returns:
            List of previous attempts with errors
        """
        failures = self.load_failures(scenario_name)
        if failures:
            step_failures = next((f for f in failures["failures"] 
                                if f["step_index"] == step_index), None)
            if step_failures:
                return step_failures["attempts"]
        return []
    
    def cleanup_old(self, max_age_days: int = 7) -> None:
        """Delete checkpoints older than max_age_days"""
        cutoff = datetime.now().timestamp() - (max_age_days * 24 * 3600)
        
        for filename in os.listdir(self.checkpoint_dir):
            filepath = os.path.join(self.checkpoint_dir, filename)
            if os.path.getmtime(filepath) < cutoff:
                os.remove(filepath)
        
        for filename in os.listdir(self.failure_dir):
            filepath = os.path.join(self.failure_dir, filename)
            if os.path.getmtime(filepath) < cutoff:
                os.remove(filepath)
