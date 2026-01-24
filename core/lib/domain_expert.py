import re
from typing import Dict, Optional

class DomainExpert:
    """
    Analyzes website context and provides Domain Expert personas and heuristics.
    """
    
    DOMAINS = {
        "ecommerce": {
            "keywords": ["cart", "shop", "checkout", "product", "price", "buy", "order", "catalog", "shipping", "inventory", "store", "sale", "deals"],
            "persona": "Senior SDET focusing on e-commerce flow automation and conversion funnel reliability",
            "heuristics": "Focus on the complete shopping funnel (Search -> Product Selection -> Add to Cart -> Checkout). CRITICAL: Identify SEARCH BARS and 'Add to Cart' buttons. Avoid looking for financial portfolios unless explicitly in the goal. FORBIDDEN: Do not suggest transfers or loans unless prompted."
        },
        "finance": {
            "keywords": ["account", "balance", "transfer", "bank", "loan", "invest", "trading", "transaction", "payment", "credit card", "debit card", "statement", "portfolio", "acme", "wealth", "recent transactions", "amount", "status", "category"],
            "persona": "Senior SDET focusing on high-accuracy FinTech automation and transactional integrity",
            "heuristics": "Focus on secure functional flows (e.g., Login -> Statement View -> Funds Transfer -> Payment Verification). Prioritize transaction tables, balance displays, and financial dashboards. DO NOT suggest e-commerce 'Add to Cart' or 'Shopping' flows for banking applications. This is a dashboard for MANAGING MONEY, not buying products."
        },
        "saas": {
            "keywords": ["dashboard", "settings", "profile", "billing", "features", "solutions", "pricing", "integration", "workspace", "admin", "console", "subscription", "users", "api"],
            "persona": "Senior SDET focusing on SaaS platform stability and multi-tenant functional coverage",
            "heuristics": "Focus on user onboarding flows, dashboard state transitions, and workspace configuration. Prioritize navigation sidebar items, 'Upgrade' triggers, and profile settings."
        },
        "social_media": {
            "keywords": ["feed", "post", "friend", "follow", "comment", "share", "like", "profile", "message", "notification", "status", "timeline", "story", "hashtag"],
            "persona": "Senior SDET focusing on social interaction reliability and real-time engagement automation",
            "heuristics": "Focus on interactive engagement elements: like, share, comment, and direct messaging. Prioritize feed scrolling behavior and notification handling."
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
