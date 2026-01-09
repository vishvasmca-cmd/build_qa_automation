import json
import os
import re

class RAGRetriever:
    def __init__(self, kb_path="knowledge/rag_knowledge_base.json"):
        self.kb_path = kb_path
        self.kb = []
        self._load_kb()

    def _load_kb(self):
        if os.path.exists(self.kb_path):
            try:
                with open(self.kb_path, "r") as f:
                    self.kb = json.load(f)
            except Exception as e:
                print(f"⚠️ Failed to load Knowledge Base: {e}")

    def retrieve(self, url=None, domain=None, limit=5):
        """
        Retrieve relevant knowledge nodes based on URL or Domain.
        Returns a list of dicts (nodes).
        """
        results = []
        
        # Priority 1: Exact URL Match
        if url:
            results.extend([
                n for n in self.kb 
                if n.get("application") == url
            ])

        # Priority 2: Domain Match
        if domain:
            results.extend([
                n for n in self.kb 
                if n.get("domain") == domain and n not in results
            ])
            
        # Priority 3: General Patterns (if results are scarce)
        if len(results) < limit:
            results.extend([
                n for n in self.kb 
                if n.get("node_type") == "pattern" and n not in results
            ])
            
        return results[:limit]

    def format_for_prompt(self, nodes):
        """
        Formats retrieved nodes into a string for the prompt.
        """
        if not nodes:
            return "No relevant past knowledge found."
        
        formatted = ""
        for i, node in enumerate(nodes):
            formatted += f"{i+1}. [{node.get('type', 'INFO')}] {node.get('content')}\n"
        return formatted
