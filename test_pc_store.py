import pytest
from file_handler import FileHandler, InventoryFileHandler
from pc_store import PCStore

# --------------------------
# FileHandler Tests
# --------------------------
def test_file_handler_read(tmp_path):
    """Test file reading via generator"""
    file_path = tmp_path / "test.txt"
    file_path.write_text("Line1\nLine2\nLine3")
    fh = FileHandler(str(file_path))
    assert list(fh.read_generator()) == ["Line1", "Line2", "Line3"]

def test_file_handler_str_representation(tmp_path):
    """Test string representation includes filename"""
    file_path = tmp_path / "test.txt"
    fh = FileHandler(str(file_path))
    assert str(file_path) in str(fh)

def test_file_concat(tmp_path):
    """Test file concatenation with __add__"""
    file_path = tmp_path / "test.txt"
    file_path.write_text("Line1")
    fh1 = FileHandler(str(file_path))
    fh2 = FileHandler(str(file_path))
    assert fh1 + fh2 == "Line1\nLine1"

# --------------------------
# InventoryFileHandler Tests
# --------------------------
def test_inventory_loading(tmp_path):
    """Test inventory loads quantities correctly"""
    file_path = tmp_path / "inventory.txt"
    file_path.write_text("Ryzen 5600X:10\nRTX 3060:5")
    ifh = InventoryFileHandler(str(file_path))
    assert ifh.inventory == {"Ryzen 5600X": 10, "RTX 3060": 5}

def test_inventory_merge(tmp_path):
    """Test inventory merging sums quantities"""
    file_path = tmp_path / "inventory.txt"
    file_path.write_text("Ryzen 5600X:10")
    ifh1 = InventoryFileHandler(str(file_path))
    ifh2 = InventoryFileHandler(str(file_path))
    combined = ifh1 + ifh2
    assert combined["Ryzen 5600X"] == 20

# --------------------------
# PCStore Validation Tests
# --------------------------
@pytest.mark.parametrize("cpu,expected", [
    ("Ryzen 5600X", True),
    ("Core i5-12400", True),
    ("Ryzen5600X", False),
    ("Invalid", False)
])
def test_cpu_validation(cpu, expected):
    """Test CPU name validation patterns"""
    result = PCStore.validate_cpu(cpu)
    assert (result is not None) == expected

@pytest.mark.parametrize("gpu,expected", [
    ("RTX 3060", True),
    ("RX 6800 XT", True),
    ("RTX3060", False),
    ("Invalid", False)
])
def test_gpu_validation(gpu, expected):
    """Test GPU name validation patterns"""
    result = PCStore.validate_gpu(gpu)
    assert (result is not None) == expected

# --------------------------
# PCStore Operation Tests
# --------------------------
def test_component_display(tmp_path):
    """Test inventory filtering for CPUs/GPUs"""
    file_path = tmp_path / "inventory.txt"
    file_path.write_text("Ryzen 5600X:10\nRTX 3060:5")
    store = PCStore(str(file_path))
    assert "Ryzen 5600X" in store.display_cpus()
    assert "RTX 3060" in store.display_gpus()

def test_sell_component(tmp_path, monkeypatch):
    """Test selling reduces inventory"""
    file_path = tmp_path / "inventory.txt"
    file_path.write_text("RTX 3060:5")
    store = PCStore(str(file_path))
    
    # Mock user input for quantity
    monkeypatch.setattr('builtins.input', lambda _: "1")
    
    result = store.sell_component("RTX 3060")
    assert result == "Sold 1 RTX 3060"
    assert store.inventory["RTX 3060"] == 4
    
    # Test selling non-existent component - matches actual implementation
    result = store.sell_component("Missing")
    assert "Component not found" in result
    assert "Please check the list above" in result
