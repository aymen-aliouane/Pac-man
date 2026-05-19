FLAKE8 = .venv/bin/flake8
MYPY = .venv/bin/mypy

install:
	uv sync

run:
	UV_SKIP_WHEEL_FILENAME_CHECK=1 uv run python3 main.py config.json

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
 
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
 
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
 
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.eggs" -exec rm -rf {} +

lint: 
	$(FLAKE8) . --exclude=.venv
	$(MYPY) . --warn-return-any
	--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs
	--check-untyped-defs

lint-strict:
	$(FLAKE8) . --exclude=.venv
	$(MYPY) . --strict