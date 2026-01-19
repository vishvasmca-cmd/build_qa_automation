"""
Performance Metrics Tracking Module

Tracks agent performance metrics to quantify optimization impacts:
- Phase timings (discovery, exploration, total)
- Element resolution methods (smart vs AI)
- AI performance (call count, latency, batch efficiency)
- Cache effectiveness
- Retry/loop statistics
"""

import time
import json
import os
from typing import Dict
from contextlib import contextmanager


class PerformanceMetrics:
    """Track and report comprehensive agent performance metrics."""
    
    def __init__(self):
        # Phase timings
        self.phase_timings = {
            "discovery": 0.0,
            "planning": 0.0,
            "exploration": 0.0,
            "total": 0.0
        }
        
        # Element resolution
        self.element_mining = {
            "total_attempts": 0,
            "smart_successes": 0,
            "ai_fallbacks": 0,
            "deterministic_successes": 0
        }
        
        # AI metrics
        self.ai_metrics = {
            "total_calls": 0,
            "batch_calls": 0,
            "sequential_calls": 0,
            "total_latency_ms": 0.0
        }
        
        # Cache metrics
        self.cache_metrics = {
            "hits": 0,
            "misses": 0,
            "invalidations": 0
        }
        
        # Retry metrics
        self.retry_metrics = {
            "mining_retries": 0,
            "loop_detections": 0,
            "state_revisits": 0
        }
        
        self._phase_start_times = {}
    
    @contextmanager
    def time_phase(self, phase_name: str):
        """Context manager to time a phase."""
        start = time.time()
        try:
            yield
        finally:
            duration = time.time() - start
            self.phase_timings[phase_name] = duration
    
    def record_element_resolution(self, method: str):
        """
        Record how an element was resolved.
        method: "smart", "ai", or "deterministic"
        """
        self.element_mining["total_attempts"] += 1
        if method == "smart":
            self.element_mining["smart_successes"] += 1
        elif method == "ai":
            self.element_mining["ai_fallbacks"] += 1
        elif method == "deterministic":
            self.element_mining["deterministic_successes"] += 1
    
    def record_ai_call(self, is_batch: bool = False, latency_ms: float = 0):
        """Record an AI vision call."""
        self.ai_metrics["total_calls"] += 1
        if is_batch:
            self.ai_metrics["batch_calls"] += 1
        else:
            self.ai_metrics["sequential_calls"] += 1
        if latency_ms > 0:
            self.ai_metrics["total_latency_ms"] += latency_ms
    
    def record_cache_event(self, event_type: str):
        """event_type: 'hit', 'miss', or 'invalidation'"""
        if event_type in ["hit", "miss", "invalidation"]:
            key = f"{event_type}s" if event_type != "invalidation" else "invalidations"
            self.cache_metrics[key] += 1
    
    def record_retry(self, retry_type: str):
        """retry_type: 'mining', 'loop', or 'revisit'"""
        if retry_type == "mining":
            self.retry_metrics["mining_retries"] += 1
        elif retry_type == "loop":
            self.retry_metrics["loop_detections"] += 1
        elif retry_type == "revisit":
            self.retry_metrics["state_revisits"] += 1
    
    def get_summary(self) -> Dict:
        """Generate summary statistics."""
        total_attempts = self.element_mining["total_attempts"]
        smart_rate = (self.element_mining["smart_successes"] / total_attempts * 100) if total_attempts > 0 else 0
        
        cache_total = self.cache_metrics["hits"] + self.cache_metrics["misses"]
        cache_hit_rate = (self.cache_metrics["hits"] / cache_total * 100) if cache_total > 0 else 0
        
        avg_ai_latency = (self.ai_metrics["total_latency_ms"] / self.ai_metrics["total_calls"]) if self.ai_metrics["total_calls"] > 0 else 0
        
        return {
            "phase_timings": self.phase_timings,
            "element_resolution": {
                **self.element_mining,
                "smart_selector_rate": f"{smart_rate:.1f}%"
            },
            "ai_performance": {
                **self.ai_metrics,
                "avg_latency_ms": f"{avg_ai_latency:.1f}"
            },
            "cache_performance": {
                **self.cache_metrics,
                "hit_rate": f"{cache_hit_rate:.1f}%"
            },
            "retry_metrics": self.retry_metrics
        }
    
    def print_summary(self):
        """Print formatted summary to console."""
        summary = self.get_summary()
        print("\n" + "=" * 60)
        print("📊 PERFORMANCE METRICS")
        print("=" * 60)
        
        print("\n⏱️  Phase Timings:")
        for phase, duration in summary["phase_timings"].items():
            if duration > 0:
                print(f"   {phase.capitalize()}: {duration:.2f}s")
        
        print("\n🎯 Element Resolution:")
        print(f"   Total Attempts: {summary['element_resolution']['total_attempts']}")
        print(f"   Smart Selectors: {summary['element_resolution']['smart_successes']} ({summary['element_resolution']['smart_selector_rate']})")
        print(f"   AI Fallbacks: {summary['element_resolution']['ai_fallbacks']}")
        print(f"   Deterministic: {summary['element_resolution']['deterministic_successes']}")
        
        print("\n🤖 AI Performance:")
        print(f"   Total Calls: {summary['ai_performance']['total_calls']}")
        if summary['ai_performance']['total_calls'] > 0:
            print(f"   Batch Calls: {summary['ai_performance']['batch_calls']}")
            print(f"   Sequential: {summary['ai_performance']['sequential_calls']}")
            print(f"   Avg Latency: {summary['ai_performance']['avg_latency_ms']}ms")
        
        print("\n💾 Cache Performance:")
        print(f"   Hits: {summary['cache_performance']['hits']}")
        print(f"   Misses: {summary['cache_performance']['misses']}")
        print(f"   Hit Rate: {summary['cache_performance']['hit_rate']}")
        
        print("\n🔄 Retry Metrics:")
        print(f"   Mining Retries: {summary['retry_metrics']['mining_retries']}")
        print(f"   Loop Detections: {summary['retry_metrics']['loop_detections']}")
        print(f"   State Revisits: {summary['retry_metrics']['state_revisits']}")
        
        print("=" * 60 + "\n")
    
    def save(self, output_dir: str, filename: str = "performance_metrics.json") -> str:
        """Save metrics to JSON file."""
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.get_summary(), f, indent=2)
        
        return filepath
