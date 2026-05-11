install:
	uv sync

run:
	python3 game.py

clean:
	rm -rf __pycache__
