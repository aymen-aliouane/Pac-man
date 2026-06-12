from game import GameEngine
import sys


def main() -> None:
    """
    Main function to start the game.
    """
    if len(sys.argv) != 2:
        print("Usage: uv run python3 game.py <config_file>")
        sys.exit(1)
    try:
        game = GameEngine(file_path=sys.argv[1])
        game.run()
    except FileNotFoundError as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
