"""
Navigation Efficiency Metrics Logger
Tracks path optimization metrics for analysis and monitoring.
"""
import json
import os
from typing import Dict, List, Optional
from datetime import datetime


class NavigationMetrics:
    """Track and log navigation efficiency metrics"""
    
    def __init__(self, project_name: str, scenario_name: str):
        self.project_name = project_name
        self.scenario_name = scenario_name
        self.metrics = {
            "project": project_name,
            "scenario": scenario_name,
            "timestamp": datetime.now().isoformat(),
            "total_steps": 0,
            "optimized_steps": 0,
            "duplicate_steps_removed": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "circular_paths_detected": 0,
            "states_visited": 0,
            "unique_states": 0,
            "path_efficiency": 0.0,
            "redundancy_rate": 0.0,
            "cache_hit_rate": 0.0
        }
    
    def record_exploration(self, total_steps: int, optimized_steps: int, 
                          states_visited: int, unique_states: int):
        """
        Record exploration completion metrics.
        
        Args:
            total_steps: Total steps generated during exploration
            optimized_steps: Steps after optimization
            states_visited: Total state visits (including duplicates)
            unique_states: Number of unique states explored
        """
        self.metrics["total_steps"] = total_steps
        self.metrics["optimized_steps"] = optimized_steps
        self.metrics["duplicate_steps_removed"] = total_steps - optimized_steps
        self.metrics["states_visited"] = states_visited
        self.metrics["unique_states"] = unique_states
        
        # Calculate derived metrics
        if total_steps > 0:
            self.metrics["path_efficiency"] = round(
                (optimized_steps / total_steps) * 100, 2
            )
            self.metrics["redundancy_rate"] = round(
                ((total_steps - optimized_steps) / total_steps) * 100, 2
            )
        
        if states_visited > 0:
            self.metrics["state_revisit_rate"] = round(
                ((states_visited - unique_states) / states_visited) * 100, 2
            )
    
    def record_cache_stats(self, cache_hits: int, cache_misses: int):
        """
        Record LLM cache statistics.
        
        Args:
            cache_hits: Number of cache hits
            cache_misses: Number of cache misses
        """
        self.metrics["cache_hits"] = cache_hits
        self.metrics["cache_misses"] = cache_misses
        
        total_calls = cache_hits + cache_misses
        if total_calls > 0:
            self.metrics["cache_hit_rate"] = round(
                (cache_hits / total_calls) * 100, 2
            )
    
    def record_circular_navigation(self, count: int):
        """
        Record number of circular navigation paths detected and prevented.
        
        Args:
            count: Number of circular paths detected
        """
        self.metrics["circular_paths_detected"] = count
    
    def save(self, output_dir: str = "outputs"):
        """
        Save metrics to JSON file.
        
        Args:
            output_dir: Directory to save metrics
        """
        os.makedirs(output_dir, exist_ok=True)
        
        metrics_file = os.path.join(
            output_dir, 
            f"navigation_metrics_{self.project_name}_{self.scenario_name}.json"
        )
        
        with open(metrics_file, 'w', encoding='utf-8') as f:
            json.dump(self.metrics, f, indent=2)
        
        # Also append to aggregate metrics log
        aggregate_file = os.path.join(output_dir, "navigation_metrics_all.jsonl")
        with open(aggregate_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(self.metrics) + "\n")
        
        return metrics_file
    
    def to_dict(self) -> Dict:
        """Return metrics as dictionary"""
        return self.metrics.copy()
    
    def print_summary(self):
        """Print formatted metrics summary to console"""
        print("\n" + "="*60)
        print(f"📊 Navigation Metrics: {self.scenario_name}")
        print("="*60)
        print(f"Total Steps Generated:    {self.metrics['total_steps']}")
        print(f"Optimized Steps:          {self.metrics['optimized_steps']}")
        print(f"Duplicate Steps Removed:  {self.metrics['duplicate_steps_removed']}")
        print(f"Path Efficiency:          {self.metrics['path_efficiency']}%")
        print(f"Redundancy Rate:          {self.metrics['redundancy_rate']}%")
        print("-"*60)
        print(f"Cache Hits:               {self.metrics['cache_hits']}")
        print(f"Cache Misses:             {self.metrics['cache_misses']}")
        print(f"Cache Hit Rate:           {self.metrics.get('cache_hit_rate', 0)}%")
        print("-"*60)
        print(f"States Visited:           {self.metrics['states_visited']}")
        print(f"Unique States:            {self.metrics['unique_states']}")
        print(f"Circular Paths Blocked:   {self.metrics['circular_paths_detected']}")
        print("="*60 + "\n")
