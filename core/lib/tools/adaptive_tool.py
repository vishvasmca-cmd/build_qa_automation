"""
Adaptive Tool Base Class
Enables tools to learn site-specific patterns and generate custom methods dynamically.
"""

import os
import json
import hashlib
import asyncio
from typing import Dict, Any, Optional
from pathlib import Path
from playwright.async_api import Page
from termcolor import colored


class AdaptiveTool:
    """
    Base class that enables tools to:
    1. Detect repeated failures
    2. Learn from successful patterns
    3. Generate site-specific methods dynamically
    4. Store learned patterns for future use
    """
    
    def __init__(self, tool_name: str):
        self.tool_name = tool_name
        self.failure_tracker = {}  # domain -> failure_count
        self.learned_patterns = {}  # domain -> method
        self.knowledge_base_path = Path("knowledge/sites")
        
        # Load existing learned patterns on init
        self._load_learned_patterns()
    
    def get_domain(self, url: str) -> str:
        """Extract domain from URL"""
        from urllib.parse import urlparse
        return urlparse(url).netloc
    
    def _load_learned_patterns(self):
        """Load all learned patterns from knowledge base"""
        if not self.knowledge_base_path.exists():
            return
        
        for site_dir in self.knowledge_base_path.iterdir():
            if not site_dir.is_dir():
                continue
            
            pattern_file = site_dir / f"{self.tool_name}_pattern.json"
            if pattern_file.exists():
                try:
                    with open(pattern_file, 'r') as f:
                        pattern_data = json.load(f)
                        domain = site_dir.name
                        self.learned_patterns[domain] = pattern_data
                        print(colored(f"📚 Loaded learned pattern for {domain} ({self.tool_name})", "cyan"))
                except Exception as e:
                    print(colored(f"⚠️ Failed to load pattern for {site_dir.name}: {e}", "yellow"))
    
    async def track_failure(self, page: Page, error: str, context: Dict[str, Any]):
        """
        Track a failure and trigger learning if threshold is reached.
        
        Args:
            page: Playwright page
            error: Error message
            context: Execution context (what was attempted)
        """
        domain = self.get_domain(page.url)
        
        # Initialize or increment failure count
        if domain not in self.failure_tracker:
            self.failure_tracker[domain] = []
        
        self.failure_tracker[domain].append({
            "error": error,
            "context": context,
            "url": page.url,
            "timestamp": asyncio.get_event_loop().time()
        })
        
        failure_count = len(self.failure_tracker[domain])
        
        # TRIGGER LEARNING after 3 failures
        if failure_count >= 3:
            print(colored(f"\n🧠 LEARNING MODE ACTIVATED: {failure_count} failures on {domain}", "magenta", attrs=["bold"]))
            await self._trigger_learning(page, domain)
    
    async def _trigger_learning(self, page: Page, domain: str):
        """
        Analyze failures and generate a site-specific pattern.
        This will be implemented by child classes.
        """
        print(colored(f"⚡ Analyzing failure patterns for {domain}...", "yellow"))
        
        # Get recent failures
        failures = self.failure_tracker[domain][-3:]
        
        # Extract common patterns
        pattern_data = {
            "domain": domain,
            "tool": self.tool_name,
            "failures": failures,
            "analysis": "Pattern analysis would go here",
            "custom_method": None
        }
        
        # Save pattern for review
        self._save_pattern(domain, pattern_data)
        
        print(colored(f"💾 Failure pattern saved to knowledge/sites/{domain}/{self.tool_name}_pattern.json", "cyan"))
        
        # 🔥 AUTO-LLM CODE GENERATION (Now ENABLED!)
        print(colored(f"🤖 Attempting to generate custom method via LLM...", "magenta"))
        
        try:
            from .pattern_generator import PatternGenerator
            generator = PatternGenerator()
            
            # Generate code using LLM
            code = await generator.generate_custom_method(
                self.tool_name,
                domain,
                failures,
                success_trace=None  # Could be enhanced with successful traces
            )
            
            # Save the generated method
            generator.save_generated_method(domain, self.tool_name, code)
            
            print(colored(f"✅ Custom method generated and saved!", "green", attrs=["bold"]))
            print(colored(f"   📁 Location: knowledge/sites/{domain}/{self.tool_name}_custom.py", "cyan"))
            print(colored(f"   🔄 Will be auto-loaded on next run!", "cyan"))
            
        except Exception as e:
            print(colored(f"⚠️ LLM generation failed: {e}", "yellow"))
            print(colored(f"   Pattern still saved for manual review", "yellow"))
            # Don't crash - the pattern is still saved for manual implementation

    
    def _save_pattern(self, domain: str, pattern_data: Dict[str, Any]):
        """Save learned pattern to knowledge base"""
        site_dir = self.knowledge_base_path / domain
        site_dir.mkdir(parents=True, exist_ok=True)
        
        pattern_file = site_dir / f"{self.tool_name}_pattern.json"
        with open(pattern_file, 'w') as f:
            json.dump(pattern_data, f, indent=2)
    
    def has_custom_pattern(self, domain: str) -> bool:
        """Check if a custom pattern exists for this domain"""
        return domain in self.learned_patterns
    
    def get_custom_pattern(self, domain: str) -> Optional[Dict[str, Any]]:
        """Get custom pattern for domain if it exists"""
        return self.learned_patterns.get(domain)
    
    async def execute_with_pattern(self, page: Page, pattern: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        Execute using a learned pattern.
        This should be overridden by child classes.
        """
        raise NotImplementedError("Subclass must implement execute_with_pattern")
    
    def reset_failures(self, domain: str):
        """Reset failure tracking for a domain (call after successful execution)"""
        if domain in self.failure_tracker:
            del self.failure_tracker[domain]
