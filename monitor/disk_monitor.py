"""
disk_monitor.py
---------------
Monitors disk usage on Unix/Linux systems.
Checks space availability and classifies health status.
"""

import shutil
import time
import os

class StorageError(Exception):
    """Raised when disk read operation fails."""
    pass

class DiskMonitor:

    WARNING_THRESHOLD = 80   # % usage → warning
    CRITICAL_THRESHOLD = 95  # % usage → critical

    def __init__(self):
        self._history = []

    def check_disk_usage(self, path: str) -> dict:
        """
        Check disk usage for a given path.

        Args:
            path: Directory path to check (e.g. '/' or 'C:\\')

        Returns:
            dict with usage stats and health status
        """

        try:
            total, used, free = shutil.disk_usage(path)
        except OSError as e:
            raise StorageError(f"Failed to read disk usage for {path}: {e}")
        
        if not os.path.exists(path):
            raise ValueError(f"Path does not exist: {path}")

        total, used, free = shutil.disk_usage(path)

        usage_pct = round((used / total) * 100, 2)

        if usage_pct >= self.CRITICAL_THRESHOLD:
            status = "critical"
        elif usage_pct >= self.WARNING_THRESHOLD:
            status = "warning"
        else:
            status = "healthy"

        result = {
            "path": path,
            "total_gb": round(total / (1024**3), 2),
            "used_gb": round(used / (1024**3), 2),
            "free_gb": round(free / (1024**3), 2),
            "usage_pct": usage_pct,
            "status": status,
            "timestamp": time.time(),
        }

        self._history.append(result)
        return result

    def get_history(self) -> list:
        """Return all previous check results."""
        return self._history

    def clear_history(self):
        """Clear check history."""
        self._history.clear()   