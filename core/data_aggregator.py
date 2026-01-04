import os
import json
import glob

class KnowledgeAggregator:
    def __init__(self, project_root="."):
        self.project_root = project_root
        self.dataset_dir = os.path.join(project_root, "knowledge", "datasets")
        os.makedirs(self.dataset_dir, exist_ok=True)
        
        # Load Knowledge Bank for enrichment
        self.kb_path = os.path.join(project_root, "knowledge", "learned_patterns_v2.json")
        self.kb_data = {}
        if os.path.exists(self.kb_path):
            with open(self.kb_path, "r") as f:
                self.kb_data = json.load(f)

    def aggregate_traces(self):
        """
        Scans all project traces and compiles them into ML-ready datasets.
        """
        print("🧠 Aggregating Knowledge for Predictive Models...")
        
        action_dataset = []
        locator_dataset = []
        
        # Find all trace.json files
        trace_files = glob.glob(os.path.join(self.project_root, "projects", "*", "outputs", "trace.json"))
        
        for trace_file in trace_files:
            try:
                with open(trace_file, "r") as f:
                    data = json.load(f)
                    
                domain_info = data.get("domain_info", {})
                workflow_goal = data.get("workflow", "Unknown Goal")
                trace_steps = data.get("trace", [])
                
                # Iterate through steps to create State-Action pairs
                for i, step in enumerate(trace_steps):
                    # We need 'success' to be true to learn from it
                    if not step.get("success", False):
                        continue
                        
                    # 1. Next Action Prediction Data
                    # Context: Goal + Current Page + Previous Action (if any)
                    prev_action = trace_steps[i-1]["action"] if i > 0 else "start"
                    
                    # Heuristic: If we have a page summary in domain_info, use it
                    # otherwise use basic URL/PageName
                    page_summary = domain_info.get(step["url"], {}).get("page_name", "Unknown Page")
                    
                    action_sample = {
                        "input": {
                            "goal": workflow_goal,
                            "current_page": page_summary,
                            "previous_action": prev_action,
                            "url": step["url"]
                        },
                        "output": {
                            "action": step["action"],
                            "reasoning": step.get("decision_reason", "")
                        }
                    }
                    action_dataset.append(action_sample)
                    
                    # 2. Locator Prediction Data
                    # If action involved an element interaction
                    if step["action"] in ["click", "fill"] and step.get("locator_used"):
                        target_id = step.get("target")
                        
                        # Enrich with Stability Score from Knowledge Bank
                        # Domain -> Page -> Locator
                        domain_key = step["url"].replace("https://", "").split("/")[0] # Simple domain parse
                        stability_score = 0
                        
                        # Try to find stability score
                        if domain_key in self.kb_data.get("sites", {}):
                            site_data = self.kb_data["sites"][domain_key]
                            # Search pages
                            for p_name, locs in site_data.items():
                                for loc in locs:
                                    if loc["playwright"] == step["locator_used"]:
                                        stability_score = loc.get("stability", 0)
                                        break
                        
                        locator_sample = {
                            "input": {
                                "goal": workflow_goal,
                                "page_context": page_summary,
                                "element_context": step.get("reasoning", ""), # What we wanted to do
                                "target_description": step.get("decision_reason", "")
                            },
                            "output": {
                                "locator": step["locator_used"],
                                "stability_score": stability_score
                            }
                        }
                        locator_dataset.append(locator_sample)
                        
            except Exception as e:
                print(f"⚠️ Error processing {trace_file}: {e}")
                
        # Save Datasets
        self._save_jsonl("next_action_prediction.jsonl", action_dataset)
        self._save_jsonl("locator_prediction.jsonl", locator_dataset)
        
        print(f"✅ Aggregated {len(action_dataset)} Action samples and {len(locator_dataset)} Locator samples.")

    def _save_jsonl(self, filename, data):
        path = os.path.join(self.dataset_dir, filename)
        with open(path, "w") as f:
            for entry in data:
                f.write(json.dumps(entry) + "\n")
        print(f"💾 Saved {path}")

if __name__ == "__main__":
    aggregator = KnowledgeAggregator()
    aggregator.aggregate_traces()
