import re
from typing import Dict, Optional

class DomainExpert:
    """
    Analyzes website context and provides Domain Expert personas and heuristics.
    """
    
    DOMAINS = {
        "ecommerce": {
            "keywords": ["cart", "shop", "checkout", "product", "price", "buy", "order", "stock"],
            "persona": "Senior SDET focusing on e-commerce flow automation and conversion funnel reliability",
            "heuristics": "Focus on the complete shopping funnel (Search -> Product Selection -> Add to Cart -> Checkout). CRITICAL: Identify SEARCH BARS, magnifying glass icons, and 'Add to Cart' buttons as primary automation targets. Dismiss popups that block the flow. For product lists, default to selecting the FIRST available item for consistent automation."
        },
        "finance": {
            "keywords": ["account", "balance", "transfer", "bank", "loan", "invest", "trading", "stock"],
            "persona": "Senior SDET focusing on exploring application to understand functional flow and automating FinTech scenarios",
            "heuristics": "Focus on the end-to-end functional flow (e.g., Account Creation, Login, Funds Transfer, Loan Application). Prioritize identifying stable locators and interactive elements for automation. Ensure core banking features are accessible and functional."
        },
        "saas": {
            "keywords": ["dashboard", "settings", "profile", "billing", "features", "solutions", "pricing"],
            "persona": "Senior SDET focusing on SaaS platform stability and functional coverage",
            "heuristics": "Focus on user onboarding flows and dashboard state transitions. Prioritize 'Sign Up', 'Upgrade', and navigation sidebar items as critical automation paths."
        },
        "social_media": {
            "keywords": ["feed", "post", "friend", "follow", "comment", "share", "like", "profile"],
            "persona": "Senior SDET focusing on social interaction and feed reliability",
            "heuristics": "Focus on interactive engagement elements: like, share, comment. Prioritize feed scrolling behavior and profile settings automation."
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
        return "Act as Senior SDET focusing on exploring the application to understand functional flow and identifying critical paths for end-to-end automation."
