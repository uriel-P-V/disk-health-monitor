import pytest
from unittest.mock import patch
from monitor import DiskMonitor


@pytest.fixture
def monitor():
    """Fresh DiskMonitor instance for each test."""
    m = DiskMonitor()
    yield m
    m.clear_history()


@pytest.fixture
def mock_healthy_disk():
    """Simulates a disk at 50% usage."""
    total = 100 * (1024**3)   # 100 GB
    used  =  50 * (1024**3)   #  50 GB
    free  =  50 * (1024**3)   #  50 GB
    return (total, used, free)


@pytest.fixture
def mock_warning_disk():
    """Simulates a disk at 85% usage."""
    total = 100 * (1024**3)
    used  =  85 * (1024**3)
    free  =  15 * (1024**3)
    return (total, used, free)


@pytest.fixture
def mock_critical_disk():
    """Simulates a disk at 96% usage."""
    total = 100 * (1024**3)
    used  =  96 * (1024**3)
    free  =   4 * (1024**3)
    return (total, used, free)