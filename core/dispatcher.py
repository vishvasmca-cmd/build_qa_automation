"""
Platform Dispatcher (Agent Router)
Detects the target platform (Shopify, WordPress, specialized frameworks)
and routes the request to the appropriate strategy or specialized agent.
"""
import requests
from urllib.parse import urlparse
from termcolor import colored

class Dispatcher:
    def __init__(self):
        # Maps platform signatures to specialized prompt enhancements
        self.platform_strategies = {
            "shopify": {
                "name": "Shopify eCommerce",
                "rules": [
                    "Use id='AddToCart' or name='add' for cart buttons",
                    "Expect /cart or /checkout URLs",
                    "Product grids usually use .grid-product or .product-card"
                ]
            },
            "wordpress": {
                "name": "WordPress Site",
                "rules": [
                    "Check for typical WP classes like .wp-block-button",
                    "Forms often use standard WP identifiers",
                    "Might have heavy caching/overlays"
                ]
            },
            "react": {
                "name": "React Application",
                "rules": [
                    "Wait for stability is CRITICAL due to hydration",
                    "Don't rely on random IDs (often minified)",
                    "Use get_by_role heavily"
                ]
            }
        }

    def detect_platform(self, url):
        """
        Analyzes the target URL to detect the underlying platform.
        Returns a strategy dict or None.
        """
        print(colored(f"📡 Dispatcher Analyzing: {url}...", "cyan"))
        try:
            domain = urlparse(url).netloc
            # simple header/body check (lightweight)
            # In a real scenario, use Wappalyzer logic or deeper inspection
            # For now, we simulate detection based on known domains/patterns or quick request
            
            # Simple heuristic: Request page and check meta/headers
            try:
                resp = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
                content = resp.text.lower()
                headers = resp.headers
                
                if "shopify" in content or "myshopify" in domain:
                    return self.platform_strategies["shopify"]
                
                if "wp-content" in content or "wordpress" in content:
                    return self.platform_strategies["wordpress"]
                
                if "react" in content or "next" in content or "_next" in content:
                     return self.platform_strategies["react"]
                     
            except:
                pass # Fallback to generic

            return None
            
        except Exception as e:
            print(colored(f"⚠️ Dispatcher Check Failed: {e}", "yellow"))
            return None

    def get_specialized_context(self, url):
        """Returns string of specialized rules for the system prompt."""
        strategy = self.detect_platform(url)
        if strategy:
            print(colored(f"🎯 Platform Detected: {strategy['name']}", "green", attrs=["bold"]))
            rules_str = "\n".join([f"- {r}" for r in strategy["rules"]])
            return f"\n**PLATFORM SPECIFIC STRATEGY ({strategy['name']})**:\n{rules_str}\n"
        
        return ""
