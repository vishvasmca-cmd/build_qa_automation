import json
import os
import re
from collections import defaultdict

class RAGSynthesizer:
    def __init__(self, failure_log="knowledge/failures.json", output_kb="knowledge/rag_knowledge_base.json"):
        self.failure_log = failure_log
        self.output_kb = output_kb
        self.nodes = []

    def harvest_failures(self):
        """
        Reads failures.json and converts actionable failures into RAG nodes.
        """
        if not os.path.exists(self.failure_log):
            print("⚠️ No failure log found to harvest.")
            return

        try:
            with open(self.failure_log, "r") as f:
                failures = json.load(f)
                
            for fail in failures:
                # Basic heuristic: Convert failures into 'failure_fix' nodes
                node = {
                    "node_type": "failure_fix",
                    "domain": fail.get("domain", "general"),
                    "application": fail.get("project", {}).get("url", "unknown"),
                    "scenario": fail.get("workflow_goal", "unknown"),
                    "error_type": fail.get("error_type", "UnknownError"),
                    "knowledge_points": [
                        {
                            "challenge": fail.get("error_summary", ""),
                            "solution": "Check strict mode and visibility before interaction." # Generic fallback, agent refines this
                        }
                    ],
                    "contextual_logic": f"Avoid {fail.get('error_type')} by verifying element state."
                }
                self.nodes.append(node)
                
            print(f"🧠 Harvested {len(self.nodes)} new knowledge nodes from failures.")
            
        except Exception as e:
            print(f"❌ Harvesting failed: {e}")

    def generate_knowledge_graph(self):
        """
        Writes the nodes to the Knowledge Base JSON.
        """
        # Load existing
        existing_nodes = []
        if os.path.exists(self.output_kb):
            try:
                with open(self.output_kb, "r") as f:
                    existing_nodes = json.load(f)
            except: pass
            
        # Merge (simple append for now, de-duplication later)
        # Use a simple set of hashes to avoid exact duplicates
        seen = set()
        for n in existing_nodes:
            s_dump = json.dumps(n, sort_keys=True)
            seen.add(s_dump)
            
        new_count = 0
        for n in self.nodes:
            s_dump = json.dumps(n, sort_keys=True)
            if s_dump not in seen:
                existing_nodes.append(n)
                seen.add(s_dump)
                new_count += 1
                
        # Save
        os.makedirs(os.path.dirname(self.output_kb), exist_ok=True)
        with open(self.output_kb, "w") as f:
            json.dump(existing_nodes, f, indent=2)
            
        print(f"💾 Knowledge Graph Saved. Total Nodes: {len(existing_nodes)} (+{new_count} new)")
