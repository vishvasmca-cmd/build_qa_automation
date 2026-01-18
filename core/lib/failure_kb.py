import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class FailureKnowledgeBase:
    """
    Tracks and persists failure patterns and successful healing mappings.
    Used for auditing and to avoid redundant AI healing calls.
    """
    def __init__(self, kb_path: str = "core/knowledge/failure_kb.json"):
        self.kb_path = kb_path
        os.makedirs(os.path.dirname(self.kb_path), exist_ok=True)
        self.data = self._load_kb()

    def _load_kb(self) -> Dict:
        if os.path.exists(self.kb_path):
            try:
                with open(self.kb_path, 'r') as f:
                    return json.load(f)
            except Exception:
                return {"failures": [], "healing_map": {}}
        return {"failures": [], "healing_map": {}}

    def _save_kb(self):
        with open(self.kb_path, 'w') as f:
            json.dump(self.data, f, indent=2)

    def record_failure(self, site: str, step_id: int, step_desc: str, error: str, screenshot_path: Optional[str] = None):
        """Records a raw failure event for auditing."""
        failure_event = {
            "timestamp": datetime.now().isoformat(),
            "site": site,
            "step_id": step_id,
            "step_description": step_desc,
            "error": error,
            "screenshot": screenshot_path
        }
        if "failures" not in self.data:
            self.data["failures"] = []
        self.data["failures"].append(failure_event)
        self._save_kb()

    def record_healing(self, site: str, broken_locator: str, healed_locator: str, error_type: str):
        """Maps a broken locator to a healed one for a specific site."""
        if "healing_map" not in self.data:
            self.data["healing_map"] = {}
        
        if site not in self.data["healing_map"]:
            self.data["healing_map"][site] = {}
            
        self.data["healing_map"][site][broken_locator] = {
            "healed_to": healed_locator,
            "error_type": error_type,
            "last_verified": datetime.now().isoformat(),
            "success_count": self.data["healing_map"][site].get(broken_locator, {}).get("success_count", 0) + 1
        }
        self._save_kb()

    def get_known_fix(self, site: str, broken_locator: str) -> Optional[str]:
        """Returns a previously successful healed locator if available."""
        site_map = self.data.get("healing_map", {}).get(site, {})
        fix_info = site_map.get(broken_locator)
        if fix_info:
            return fix_info.get("healed_to")
        return None

    def get_audit_summary(self) -> Dict:
        """Returns stats for the Security Auditor or Summary phase."""
        return {
            "total_failures": len(self.data.get("failures", [])),
            "total_healed_elements": len(self.data.get("healing_map", {})),
            "sites_affected": list(self.data.get("healing_map", {}).keys())
        }
