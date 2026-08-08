"""
Entry point for the "Guess the Number" game.
"""

from src.game import GameController


def main() -> None:
    """Run the game."""
    controller = GameController()
    controller.run()


if __name__ == "__main__":
    main()
