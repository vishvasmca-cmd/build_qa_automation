import re
from typing import Dict, Optional

class DomainExpert:
    """
    Analyzes website context and provides Domain Expert personas and heuristics.
    """
    
    DOMAINS = {
        "ecommerce": {
            "keywords": ["cart", "shop", "checkout", "product", "price", "buy", "order", "stock"],
            "persona": "E-commerce Optimization Specialist",
            "heuristics": "Focus on the shopping funnel. CRITICAL: Identify SEARCH BARS (inputs with placeholders like 'Search'), magnifying glass icons, and 'Add to Cart' buttons. Dismiss popups immediately. For product lists, select the FIRST available item."
        },
        "finance": {
            "keywords": ["account", "balance", "transfer", "bank", "loan", "invest", "trading", "stock"],
            "persona": "FinTech Security & UX Auditor",
            "heuristics": "Prioritize security and accuracy. Focus on login forms, account summary tables, and transaction buttons. Ensure data privacy and look for secure logout options."
        },
        "saas": {
            "keywords": ["dashboard", "settings", "profile", "billing", "features", "solutions", "pricing"],
            "persona": "SaaS Product Strategist",
            "heuristics": "Focus on user onboarding and dashboard navigation. Prioritize 'Sign Up', 'Upgrade', and navigation sidebar items."
        },
        "social_media": {
            "keywords": ["feed", "post", "friend", "follow", "comment", "share", "like", "profile"],
            "persona": "Social Media Engagement Expert",
            "heuristics": "Focus on interaction elements: like, share, comment. Prioritize feed navigation and profile settings."
        }
    }

    @staticmethod
    def detect_domain(url: str, page_content: str = "", goal: str = "") -> str:
        """
        Detects the domain based on URL, page text, and User Goal.
        """
        url_lower = (url or "").lower()
        content_lower = (page_content or "").lower()
        goal_lower = (goal or "").lower()
        
        scores = {domain: 0 for domain in DomainExpert.DOMAINS}
        
        for domain, data in DomainExpert.DOMAINS.items():
            # URL Match
            if any(kw in url_lower for kw in data["keywords"]):
                scores[domain] += 2
            
            # Goal Match (High Priority)
            if goal_lower:
                for kw in data["keywords"]:
                    if kw in goal_lower:
                        scores[domain] += 3
            
            # Content Match
            if content_lower:
                for kw in data["keywords"]:
                    if kw in content_lower:
                        scores[domain] += 1
        
        # Get domain with highest score, default to 'general'
        best_domain = max(scores, key=scores.get)
        if scores[best_domain] > 0:
            return best_domain
        return "general"

    @staticmethod
    def get_persona_prompt(domain: str) -> str:
        """
        Returns the persona string for the prompt.
        """
        data = DomainExpert.DOMAINS.get(domain)
        if data:
            return f"Act as a {data['persona']}. {data['heuristics']}"
        return "Act as an expert QA Automation Engineer with deep knowledge of web accessibility and UI patterns."
