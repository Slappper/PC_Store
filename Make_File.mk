# Makefile
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

setup:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) pc_store.py

test:
	$(PYTHON) -m pytest pc_store.py -v

clean:
	rm -rf __pycache__ .pytest_cache
	rm -f inventory.txt

.PHONY: setup run test clean