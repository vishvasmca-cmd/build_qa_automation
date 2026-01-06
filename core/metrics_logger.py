import json
import os
import time
import uuid
import contextlib
from datetime import datetime

class MetricsLogger:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MetricsLogger, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self, metrics_path=None):
        if self.initialized: return
        
        self.metrics_path = metrics_path or os.path.join("outputs", "metrics.json")
        os.makedirs(os.path.dirname(self.metrics_path), exist_ok=True)
        
        # Load existing or create new using transaction lock
        with self._lock_context():
            self.data = self._load_locked()
            if not self.data.get("run_id"):
                 self._reset_run_internal()
             
        self.initialized = True


    @contextlib.contextmanager
    def _lock_context(self):
        lock_path = self.metrics_path + ".lock"
        lock_file = None
        try:
            import msvcrt
            lock_file = open(lock_path, "w")
            acquired = False
            for _ in range(200): # 20 seconds
                try:
                    msvcrt.locking(lock_file.fileno(), msvcrt.LK_NBLCK, 1)
                    acquired = True
                    break
                except IOError:
                    time.sleep(0.1)
            
            if not acquired:
                lock_file.close()
                lock_file = None
            
            yield lock_file
            
        except ImportError:
            try:
                import fcntl
                lock_file = open(lock_path, "w")
                fcntl.flock(lock_file, fcntl.LOCK_EX)
                yield lock_file
            except:
                yield None
        finally:
            if lock_file:
                try:
                    import msvcrt
                    msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
                except: pass
                lock_file.close()

    def _load_locked(self):
        if not os.path.exists(self.metrics_path) or os.path.getsize(self.metrics_path) == 0:
            return {}
        try:
            with open(self.metrics_path, "r", encoding='utf-8') as f:
                content = f.read().strip()
                return json.loads(content) if content else {}
        except:
            return {}

    def _save_locked(self):
        os.makedirs(os.path.dirname(self.metrics_path), exist_ok=True)
        temp_path = self.metrics_path + ".tmp"
        with open(temp_path, "w", encoding='utf-8') as f:
            json.dump(self.data, f, indent=2)
        
        if os.path.exists(self.metrics_path):
            os.remove(self.metrics_path)
        os.rename(temp_path, self.metrics_path)

    def log_event(self, agent, action, duration, success=True, cost=0.0, metadata=None):
        with self._lock_context():
            self.data = self._load_locked()
            if not self.data: self._reset_run_internal()
            
            event = {
                "agent": agent,
                "action": action,
                "end_time": time.time(),
                "duration": round(duration, 4),
                "success": success,
                "cost": cost,
                "metadata": metadata or {}
            }
            self.data.setdefault("events", []).append(event)
            self.data.setdefault("summary", {"total_duration": 0, "total_cost": 0, "status": "running"})
            self.data["summary"]["total_cost"] += cost
            self.data["summary"]["total_duration"] += duration
            self._save_locked()

    def log_failure(self, agent, error, context=None):
        with self._lock_context():
            self.data = self._load_locked()
            if not self.data: self._reset_run_internal()
            
            failure = {
                "agent": agent,
                "timestamp": time.time(),
                "error": str(error),
                "context": context or {}
            }
            self.data.setdefault("failures", []).append(failure)
            self._save_locked()

    def final_summary(self, status="completed"):
        with self._lock_context():
            self.data = self._load_locked()
            if not self.data: self._reset_run_internal()
            self.data.setdefault("summary", {})["status"] = status
            self._save_locked()

    def _reset_run_internal(self):
        self.data = {
            "run_id": str(uuid.uuid4()),
            "timestamp": time.time(),
            "summary": {"total_duration": 0, "total_cost": 0, "status": "running"},
            "events": [],
            "failures": []
        }

# Global Accessor
logger = MetricsLogger()
