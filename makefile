PYTHON = python3
UV = UV_SKIP_WHEEL_FILENAME_CHECK=1 uv run
FLAKE8 = $(UV) flake8
MYPY = $(UV) mypy

install:
	UV_SKIP_WHEEL_FILENAME_CHECK=1 uv sync

run:
	$(UV) $(PYTHON) main.py config.json || true

debug:
	$(PYTHON) -m pdb main.py config.json

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d \( -name "__pycache__" -o -name ".mypy_cache" -o -name ".pytest_cache" -o -name "build" -o -name "dist" -o -name "*.egg-info" -o -name "*.eggs" \) -exec rm -rf {} +

lint:
	$(FLAKE8) .
	$(MYPY) . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(FLAKE8) .
	$(MYPY) . --strict

.PHONY: install run debug clean lint lint-strict