import pytest
from unittest.mock import patch
from monitor import DiskMonitor
from monitor.disk_monitor import StorageError


def test_status_healthy(monitor, mock_healthy_disk):
    with patch("shutil.disk_usage", return_value=mock_healthy_disk):
        result = monitor.check_disk_usage("/")
        assert result["status"] == "healthy"
        assert result["usage_pct"] == 50.0
        assert result["total_gb"] == 100.0
        assert result["free_gb"] == 50.0
            
 



def test_status_warning(monitor, mock_warning_disk):
    with patch("shutil.disk_usage", return_value=mock_warning_disk):
        result = monitor.check_disk_usage("/")
        assert result["status"] == "warning"
    

def test_status_critical(monitor, mock_critical_disk):
    with patch("shutil.disk_usage", return_value=mock_critical_disk):
        result = monitor.check_disk_usage("/")
        assert result["status"] == "critical"


def test_resultado(monitor, mock_critical_disk):
    with patch("shutil.disk_usage", return_value=mock_critical_disk):
        result = monitor.check_disk_usage("/")
        assert "path" in result
        assert "total_gb" in result
        assert "used_gb" in result
        assert "free_gb" in result
        assert "usage_pct" in result
        assert "status" in result
        assert "timestamp" in result

        
def test_path_invalido_lanza_error(monitor):
    with pytest.raises(StorageError ) as exc:
        monitor.check_disk_usage("path_que_no_existe")
    assert "path_que_no_existe" in str(exc.value)