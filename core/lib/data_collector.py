import os
import json
import time
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

class DataCollector:
    """
    Captures 'Experience Replay' tuples (State, Action, Reward, NextState)
    to train self-learning models (RL & Behavior Cloning).
    """
    def __init__(self, project_dir: str):
        self.project_dir = project_dir
        self.dataset_dir = os.path.join(project_dir, "datasets")
        os.makedirs(self.dataset_dir, exist_ok=True)
        self.dataset_path = os.path.join(self.dataset_dir, "autonomy_dataset.jsonl")
        
    def capture_experience(self, 
                           goal: str,
                           url: str,
                           state: Dict[str, Any],
                           action_details: Dict[str, Any],
                           outcome: Dict[str, Any]) -> float:
        """
        Records a single interaction step and calculates its reward.
        
        Returns:
            reward_score (float): The calculated reward for this action.
        """
        
        # 1. Calculate Reward Signal
        reward = self._calculate_reward(action_details, outcome)
        
        # 2. Construct Experience Record
        record = {
            "example_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "inputs": {
                "goal": goal,
                "url": url,
                "domain": self._extract_domain(url),
                "state": state  # Minified DOM / Screenshot hash
            },
            "outputs": {
                "action_type": action_details.get("keyword"),
                "target_selector": action_details.get("selector"),
                "value": action_details.get("value"),
                "reasoning": action_details.get("description", "")
            },
            "feedback": {
                "success": outcome.get("success", False),
                "error": outcome.get("error"),
                "reward_score": reward,
                "latency_ms": outcome.get("latency_ms", 0)
            }
        }
        
        # 3. Append to Dataset (JSONL)
        try:
            with open(self.dataset_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")
        except Exception as e:
            print(f"⚠️ Failed to save experience: {e}")
            
        return reward

    def _calculate_reward(self, action: Dict, outcome: Dict) -> float:
        """
        Dense Reward Function for RL.
        """
        if not outcome.get("success", False):
            # Penalize failures
            if "Stuck" in str(outcome.get("error", "")):
                return -2.0  # Heavy penalty for loops
            return -1.0
            
        reward = 1.0  # Base survival reward
        
        # Bonus: Speed
        latency = outcome.get("latency_ms", 1000)
        if latency < 2000: reward += 0.5
        
        # Bonus: Stability (Used Memory or robust selector)
        source = action.get("source", "unknown")
        if source == "memory":
            reward += 1.0
        elif source == "smart_locator":
            reward += 0.5
        elif source == "ai_vision":
            reward -= 0.1  # Slight cost for expensive vision
            
        # Bonus: Healing
        if action.get("is_healed"):
            reward += 2.0  # Big reward for recovering from failure
            
        return reward

    def _extract_domain(self, url: str) -> str:
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc
        except:
            return "unknown"
