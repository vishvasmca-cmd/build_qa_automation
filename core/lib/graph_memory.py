
import json
import os
import time
from typing import Dict, List, Optional

class GraphMemory:
    """
    Manages the 'Mental Map' of the application for Deep Explorer.
    Stores States (Nodes) and Transitions (Edges).
    """
    def __init__(self, project_root: str, domain: str):
        self.project_root = project_root
        self.domain = domain
        self.file_path = os.path.join(project_root, "knowledge", "site_maps", f"{domain}_graph.json")
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        self.nodes: Dict[str, dict] = {}  # state_hash -> {url, title, elements, visited_count}
        self.edges: List[dict] = []       # {from_hash, to_hash, action, timestamp}
        self.frontier: List[str] = []     # List of state_hashes to explore
        
        self.load()

    def add_state(self, state_hash: str, url: str, title: str, elements: List[dict]) -> bool:
        """Register a new state node. Returns True if new."""
        if state_hash not in self.nodes:
            self.nodes[state_hash] = {
                "url": url,
                "title": title,
                "elements": elements, # Potential actions
                "first_seen": time.time(),
                "visited_count": 0,
                "explored_actions": set() # IDs of elements clicked from here
            }
            if state_hash not in self.frontier:
                self.frontier.append(state_hash)
            return True
        return False

    def record_transition(self, from_hash: str, to_hash: str, action_details: dict):
        """Record an edge (action result)."""
        self.edges.append({
            "from": from_hash,
            "to": to_hash,
            "action": action_details,
            "timestamp": time.time()
        })
        
        # Mark action as explored in the source node
        if from_hash in self.nodes:
            target_id = action_details.get("target_id")
            if target_id:
                # Convert to string to ensure set consistency
                self.nodes[from_hash]["explored_actions"].update([str(target_id)])

    def get_unexplored_actions(self, state_hash: str) -> List[dict]:
        """Returns list of interactive elements in this state that haven't been clicked."""
        if state_hash not in self.nodes:
            return []
            
        node = self.nodes[state_hash]
        explored = node.get("explored_actions", set())
        
        # Filter elements
        candidates = []
        for el in node.get("elements", []):
            eid = str(el.get("elementId"))
            if eid not in explored:
                candidates.append(el)
        
        return candidates

    def mark_visited(self, state_hash: str):
        if state_hash in self.nodes:
            self.nodes[state_hash]["visited_count"] += 1

    def save(self):
        """Persist graph to JSON."""
        # Convert sets to lists for JSON
        serializable_nodes = {}
        for k, v in self.nodes.items():
            serializable_nodes[k] = v.copy()
            serializable_nodes[k]["explored_actions"] = list(v["explored_actions"])
            
        data = {
            "domain": self.domain,
            "updated": time.time(),
            "nodes": serializable_nodes,
            "edges": self.edges,
            "frontier": self.frontier
        }
        
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print(f"[DEBUG] Graph saved to: {self.file_path}")
        except Exception as e:
            print(f"Failed to save graph memory: {e}")

    def load(self):
        """Load graph from JSON."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.edges = data.get("edges", [])
                    self.frontier = data.get("frontier", [])
                    
                    # Restore nodes and convert lists back to sets
                    raw_nodes = data.get("nodes", {})
                    for k, v in raw_nodes.items():
                        v["explored_actions"] = set(v.get("explored_actions", []))
                        self.nodes[k] = v
            except Exception as e:
                print(f"Failed to load graph memory: {e}")

