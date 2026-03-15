import re
from typing import Dict, Optional

class DomainExpert:
    """
    Analyzes website context and provides Domain Expert personas and heuristics.
    """
    
    DOMAINS = {}

    @staticmethod
    def detect_domain(url: str, page_content: str = "", goal: str = "") -> str:
        """
        Detects the domain based on URL, page text, and User Goal.
        """
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
