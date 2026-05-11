install:
	uv sync

run:
	python3 game.py

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
 
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
 
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
 
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.eggs" -exec rm -rf {} +
