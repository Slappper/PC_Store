import pytest
from file_handler import FileHandler, InventoryFileHandler
from pc_store import PCStore

def test_file_handler(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("Line1\nLine2\nLine3")
    fh = FileHandler(str(file_path))
    assert list(fh.read_generator()) == ["Line1", "Line2", "Line3"]
    assert str(fh) == f"\033[34mFileHandler for {file_path}\033[0m"
    fh2 = FileHandler(str(file_path))
    combined = fh + fh2
    assert combined == "Line1\nLine2\nLine3\nLine1\nLine2\nLine3"
    combined = FileHandler.concat_files(fh, fh2)
    assert combined == "Line1\nLine2\nLine3\nLine1\nLine2\nLine3"

def test_inventory_file_handler(tmp_path):
    file_path = tmp_path / "inventory.txt"
    file_path.write_text("Ryzen 5600X:10\nRTX 3060:5")
    ifh = InventoryFileHandler(str(file_path))
    assert ifh.inventory == {"Ryzen 5600X": 10, "RTX 3060": 5}
    ifh2 = InventoryFileHandler(str(file_path))
    combined = ifh + ifh2
    assert combined == {"Ryzen 5600X": 20, "RTX 3060": 10}

def test_pcstore_validation():
    assert PCStore.validate_cpu("Ryzen 5600X") is not None
    assert PCStore.validate_cpu("Core i5-12400K") is not None
    assert PCStore.validate_cpu("Ryzen5600X") is None
    assert PCStore.validate_cpu("Core i5 12400") is None
    assert PCStore.validate_gpu("RTX 3060") is not None
    assert PCStore.validate_gpu("RX 6800 XT") is not None
    assert PCStore.validate_gpu("RTX3060") is None
    assert PCStore.validate_gpu("RX6800XT") is None

def test_pcstore_operations(tmp_path):
    file_path = tmp_path / "inventory.txt"
    file_path.write_text("Ryzen 5600X:10\nRTX 3060:5")
    store = PCStore(str(file_path))
    cpus = store.display_cpus()
    assert "Ryzen 5600X" in cpus
    gpus = store.display_gpus()
    assert "RTX 3060" in gpus
    assert store.sell_component("RTX 3060") == "Sold one RTX 3060"
    assert store.inventory["RTX 3060"] == 4
    assert store.sell_component("RX 6800") == "RX 6800 not found in inventory"
    assert store.check_quantity("Ryzen 5600X") == 10
