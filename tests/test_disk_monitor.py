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


# Los 3 casos límite como tuplas (total, used, free)
BOUNDARY_CASES = [
    (100*(1024**3), 79*(1024**3), 21*(1024**3), "healthy"),   # 79%
    (100*(1024**3), 80*(1024**3), 20*(1024**3), "warning"),   # 80% exacto
    (100*(1024**3), 95*(1024**3),  5*(1024**3), "critical"),  # 95% exacto
]

@pytest.mark.parametrize("total, used, free, expected_status", BOUNDARY_CASES)
def test_boundary_thresholds(monitor, total, used, free, expected_status):
    with patch("shutil.disk_usage", return_value=(total, used, free)):
        result = monitor.check_disk_usage("/")
        assert result["status"] == expected_status
