import os
import yaml

class FrameworkStrategyLoader:
    """
    Loads domain-specific testing strategies from the knowledge base.
    """
    
    def __init__(self, base_path=None):
        if base_path is None:
            # Default to 'knowledge/strategies' relative to project root
            # Assuming this file is in 'core/', so project root is '..'
            self.base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'knowledge', 'strategies')
        else:
            self.base_path = base_path

    def detect_domain(self, url: str) -> str:
        """
        Detects the domain key based on the URL.
        Returns 'generic' if no match found.
        """
        url_lower = url.lower()
        
        # Mappings: keyword -> domain_file_name (without .yaml)
        mappings = {
            'demoblaze': 'ecommerce',
            'amazon': 'ecommerce',
            'shop': 'ecommerce',
            'store': 'ecommerce',
            'cart': 'ecommerce',
            'parabank': 'banking',
            'bank': 'banking',
            'finance': 'banking',
            'katalon-demo-cura': 'healthcare',
            'med': 'healthcare',
            'health': 'healthcare',
            'hospital': 'healthcare'
        }
        
        for keyword, domain in mappings.items():
            if keyword in url_lower:
                return domain
                
        return 'generic'

    def load_strategy(self, domain: str = 'generic') -> str:
        """
        Loads the strategy context for the given domain.
        Returns a formatted string ready for LLM injection.
        """
        context = []
        
        # 1. Load General Test Types (Smoke vs Regression)
        try:
            with open(os.path.join(self.base_path, 'test_types.yaml'), 'r') as f:
                types_data = yaml.safe_load(f)
                context.append("## GLOBAL TESTING STRATEGY (Smoke vs Regression)")
                for type_name, details in types_data.get('test_types', {}).items():
                    context.append(f"### {type_name.upper()}")
                    context.append(f"Definition: {details.get('definition')}")
                    context.append(f"Goal: {details.get('goal', 'N/A')}")
                    context.append("Scope:")
                    for item in details.get('scope', []):
                        context.append(f"  - {item}")
        except FileNotFoundError:
            print("⚠️ Warning: test_types.yaml not found.")

        # 2. Load Domain Specific Playbook
        domain_file = os.path.join(self.base_path, 'domains', f'{domain}.yaml')
        if os.path.exists(domain_file):
            with open(domain_file, 'r') as f:
                domain_data = yaml.safe_load(f)
                context.append(f"\n## DOMAIN PLAYBOOK: {domain_data.get('domain', domain).upper()}")
                context.append(f"Description: {domain_data.get('description', '')}")
                context.append("\n### RECOMMENDED TEST MODULES:")
                
                for module in domain_data.get('modules', []):
                    context.append(f"\n#### Module: {module['name']} (Criticality: {module.get('criticality', 'Unknown')})")
                    
                    smoke = module.get('smoke_candidates', [])
                    if smoke:
                        context.append("  [SMOKE CANDIDATES] (Must Verify):")
                        for s in smoke:
                            context.append(f"  - {s}")
                            
                    regression = module.get('regression_candidates', [])
                    if regression:
                        context.append("  [REGRESSION CANDIDATES] (Variations/Edges):")
                        for r in regression:
                            context.append(f"  - {r}")
        else:
            context.append(f"\n## DOMAIN PLAYBOOK: GENERIC")
            context.append("No specific domain playbook found. Use general best practices for web applications.")

        return "\n".join(context)
