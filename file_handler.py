import re
from functools import wraps

COLORS = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "reset": "\033[0m"
}

def color_deco(color: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return f"{COLORS[color]}{result}{COLORS['reset']}"
        return wrapper
    return decorator

class FileHandler:
    def __init__(self, filename: str):
        self.filename = filename

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        if not value.endswith('.txt'):
            raise ValueError("File must be a text file (.txt)")
        self._filename = value

    def read_generator(self):
        try:
            with open(self._filename, 'r') as file:
                for line in file:
                    yield line.strip()
        except FileNotFoundError:
            yield from []

    @color_deco("blue")
    def __str__(self):
        return f"FileHandler for {self._filename}"

    def __add__(self, other):
        content1 = '\n'.join(list(self.read_generator()))
        content2 = '\n'.join(list(other.read_generator()))
        return content1 + '\n' + content2

    @staticmethod
    def concat_files(*files):
        return '\n'.join('\n'.join(list(f.read_generator())) for f in files)

    @classmethod
    def create_from_list(cls, data: list, filename: str):
        with open(filename, 'w') as file:
            file.write('\n'.join(data))
        return cls(filename)

class InventoryFileHandler(FileHandler):
    def __init__(self, filename: str):
        super().__init__(filename)
        self.inventory = self._load_inventory()

    def _load_inventory(self):
        inventory = {}
        for line in self.read_generator():
            if ':' in line:
                item, quantity = line.split(':')
                inventory[item] = int(quantity)
        return inventory

    def __add__(self, other):
        combined = self.inventory.copy()
        for item, quantity in other.inventory.items():
            combined[item] = combined.get(item, 0) + quantity
        return combined

    def save(self):
        with open(self.filename, 'w') as file:
            for item, quantity in self.inventory.items():
                file.write(f"{item}:{quantity}\n")
