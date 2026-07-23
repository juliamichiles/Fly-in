PYTHON      = python3
VENV        = .venv
ACTIVATE    = . $(VENV)/bin/activate
MAIN        = main.py

# ---- Environment --- #
venv:
	$(PYTHON) -m venv $(VENV)
	@echo "Virtual environment created in $(VENV)"
	@echo "Run 'source $(VENV)/bin/activate' to activate it"

# ------ Install ----- #
install:
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "[Warning] You are not inside a virtual environment!"; \
		echo "Create one with: make venv"; \
		echo "Activate one with: source $(VENV)/bin/activate"; \
		exit 1; \
	fi
	pip install -r requirements.txt

# --- Run / Debug ---- #
run:
	$(PYTHON) $(MAIN)

debug:
	$(PYTHON) -m pdb $(MAIN)

# ----- Cleaning ----- #
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache

# ------ Linting ----- #
lint:
	flake8 .
	mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
