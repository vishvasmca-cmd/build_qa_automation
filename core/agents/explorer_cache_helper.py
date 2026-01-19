    async def _get_cached_or_mine_elements(self, page: Page, description: str = "element mining") -> Dict:
        """
        Get elements from cache if fresh, otherwise mine and cache.
        
        FALLBACK: On any cache error, falls back to fresh mining
        
        Returns:
            {"elements": [...], "screenshot": "base64..."}
        """
        if not self.enable_element_cache:
            # Feature disabled, always mine fresh
            from core.agents.miner import analyze_page
            return await analyze_page(page, page.url, description)
        
        url = page.url
        now = time.time()
        
        try:
            # Check cache
            if url in self.element_cache:
                cached = self.element_cache[url]
                age = now - cached["timestamp"]
                
                # Validate freshness
                if age < self.cache_ttl:
                    self.log(f"    ⚡ Cache HIT (age: {age:.1f}s)", "cyan")
                    self.metrics.record_cache_event("hit")
                    return {
                        "elements": cached["elements"],
                        "screenshot": cached["screenshot"]
                    }
                else:
                    self.log(f"    ⏰ Cache STALE (age: {age:.1f}s > {self.cache_ttl}s)", "yellow")
                    self.metrics.record_cache_event("invalidation")
            
            # Cache miss or stale - mine fresh
            self.log(f"    🔍 Cache MISS - Mining fresh elements", "cyan")
            self.metrics.record_cache_event("miss")
            
            from core.agents.miner import analyze_page
            mindmap = await analyze_page(page, page.url, description)
            
            # Update cache
            self.element_cache[url] = {
                "timestamp": now,
                "elements": mindmap.get("elements", []),
                "screenshot": mindmap.get("screenshot")
            }
            
            return mindmap
            
        except Exception as e:
            # FALLBACK: On any cache error, mine fresh
            self.log(f"    ⚠️ Cache error: {e}. Mining fresh...", "yellow")
            from core.agents.miner import analyze_page
            return await analyze_page(page, page.url, description)
    
    def _invalidate_cache(self, url: str = None):
        """Invalidate element cache for specific URL or all URLs"""
        if url:
            if url in self.element_cache:
                del self.element_cache[url]
                self.log(f"    🗑️ Invalidated cache for {url}", "grey")
        else:
            self.element_cache.clear()
            self.log(f"    🗑️ Cleared entire element cache", "grey")
