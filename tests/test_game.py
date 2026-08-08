"""
Unit tests for the 'Guess the Number' game.
"""

import pytest
from src.game import GuessNumberGame, get_number


# ======================================================================================
# TESTS FOR GuessNumberGame CLASS
# ======================================================================================


class TestGuessNumberGame:
    """Test suite for the GuessNumberGame class."""

    def test_game_initialization_default(self):
        """Test that the game initializes correctly with default parameters."""

        game = GuessNumberGame(1, 10)
        assert game.min_number == 1
        assert game.max_number == 10
        assert 1 <= game.secret_number <= 10
        assert game.attempts == 0
        assert game.max_attempts is None

    def test_game_initialization_with_max_attempts(self):
        """Test that the game initializes correctly with max_attempts."""

        game = GuessNumberGame(1, 10, max_attempts=5)
        assert game.min_number == 1
        assert game.max_number == 10
        assert game.max_attempts == 5
        assert game.attempts == 0

    def test_game_initialization_invalid_range(self):
        """Test that the game raises ValueError for invalid ranges."""

        # Minimum number greater than maximum
        with pytest.raises(ValueError, match="The minimum number must be less than"):
            GuessNumberGame(10, 1)

        # Equal numbers (empty range)
        with pytest.raises(ValueError, match="The minimum number must be less than"):
            GuessNumberGame(5, 5)

    def test_guess_correct(self, monkeypatch):
        """Test that the game correctly identifies a correct guess."""

        # Mock random.randint to always return 5
        import random
        monkeypatch.setattr(random, 'randint', lambda a, b: 5)

        game = GuessNumberGame(1, 10)
        result = game.guess(5)
        assert "🎉🏆⭐ CONGRATULATION!" in result
        assert game.attempts == 1

    def test_guess_too_low(self):
        """Test that the game correctly identifies a low guess."""

        game = GuessNumberGame(1, 10)
        # Since secret number is random, we need to guess a number we know is lower
        # We'll use a spy or mock approach, or just test the logic
        # For deterministic testing, we can patch random.randint
        import random
        original_randint = random.randint
        random.randint = lambda a, b: 5  # Force secret number to be 5

        game = GuessNumberGame(1, 10)
        result = game.guess(3)
        assert "📈 The number is HIGHER!" in result
        assert game.attempts == 1

        # Restore original randint
        random.randint = original_randint

    def test_guess_too_high(self):
        """Test that the game correctly identifies a high guess."""

        import random
        original_randint = random.randint
        random.randint = lambda a, b: 5  # Force secret number to be 5

        game = GuessNumberGame(1, 10)
        result = game.guess(7)
        assert "📉 The number is LOWER!" in result
        assert game.attempts == 1

        random.randint = original_randint

    def test_guess_out_of_range(self):
        """Test that the game rejects guesses outside the valid range."""

        game = GuessNumberGame(1, 10)
        with pytest.raises(ValueError, match="The number must be between"):
            game.guess(15)
        with pytest.raises(ValueError, match="The number must be between"):
            game.guess(0)
        assert game.attempts == 0  # Attempts should not increment for invalid guesses

    def test_max_attempts_limit(self):
        """Test that the game correctly enforces the maximum attempts limit."""

        import random
        original_randint = random.randint
        random.randint = lambda a, b: 10  # Force secret number to be 10

        game = GuessNumberGame(1, 10, max_attempts=3)
        # Make 3 incorrect guesses
        result = game.guess(1)  # Guess 1 (too low)
        result = game.guess(2)  # Guess 2 (too low)
        result = game.guess(3)  # Guess 3 (too low)

        # The next guess should trigger the attempts limit message
        result = game.guess(4)
        assert "Maximum attempts exceeded" in result
        assert game.attempts == 4

        random.randint = original_randint

    def test_is_game_over(self):
        """Test that is_game_over correctly identifies game state."""

        # Without max_attempts, game should never be over
        game = GuessNumberGame(1, 10)
        assert not game.is_game_over()
        game.guess(5)
        assert not game.is_game_over()

        # With max_attempts
        import random
        original_randint = random.randint
        random.randint = lambda a, b: 10

        game = GuessNumberGame(1, 10, max_attempts=2)
        assert not game.is_game_over()
        game.guess(1)  # Incorrect guess
        assert not game.is_game_over()
        game.guess(2)  # Second incorrect guess - should trigger game over
        assert game.is_game_over()

        random.randint = original_randint

    def test_reset(self):
        """Test that the game resets correctly with a new secret number."""

        game = GuessNumberGame(1, 10)
        old_secret = game.secret_number
        game.attempts = 5

        game.reset()

        assert game.attempts == 0
        # Secret number might be the same by chance, but we check it's within range
        assert 1 <= game.secret_number <= 10

    def test_get_stats(self):
        """Test that the game returns correct statistics."""

        import random
        original_randint = random.randint
        random.randint = lambda a, b: 5

        game = GuessNumberGame(1, 10, max_attempts=5)
        game.guess(3)
        game.guess(4)

        stats = game.get_stats()
        assert stats['attempts'] == 2
        assert stats['max_attempts'] == 5
        assert stats['range'] == "1 to 10"
        assert not stats['is_finished']

        random.randint = original_randint

    def test_temperature_very_hot(self):
        """Test temperature feedback when guess is very close (<=5%)."""

        game = GuessNumberGame(1, 100)
        game.secret_number = 50  # Force secret number

        temp = game.get_temperature(49)  # Distance = 1, max_distance = 99, percent ≈ 1%
        assert "🔥 Very hot!" in temp

    def test_temperature_hot(self):
        """Test temperature feedback when guess is close (<=15%)."""

        game = GuessNumberGame(1, 100)
        game.secret_number = 50

        temp = game.get_temperature(43)  # Distance = 7, max_distance = 99, percent ≈ 7%
        assert "☀️ Hot!" in temp

    def test_temperature_warm(self):
        """Test temperature feedback when guess is moderately close (<=30%)."""

        game = GuessNumberGame(1, 100)
        game.secret_number = 50

        temp = game.get_temperature(35)  # Distance = 15, max_distance = 99, percent ≈ 15%
        assert "🌤️ Warm." in temp

    def test_temperature_cool(self):
        """Test temperature feedback when guess is far (<=60%)."""

        game = GuessNumberGame(1, 100)
        game.secret_number = 50

        temp = game.get_temperature(20)  # Distance = 30, max_distance = 99, percent ≈ 30%
        assert "🌥️ Cool." in temp

    def test_temperature_cold(self):
        """Test temperature feedback when guess is very far (>60%)."""
        
        game = GuessNumberGame(1, 100)
        game.secret_number = 95

        temp = game.get_temperature(1)  # distance = 94, max_distance = 99, percent ≈ 95%
        assert "❄️ Cold." in temp


# ======================================================================================
# TESTS FOR HELPER FUNCTIONS
# ======================================================================================


class TestHelperFunctions:
    """Test suite for helper functions."""

    def test_get_number_valid_input(self, monkeypatch):
        """Test that get_number returns valid integer input."""
        monkeypatch.setattr('builtins.input', lambda _: "42")
        result = get_number("Enter a number: ")
        assert result == 42

    def test_get_number_invalid_input_then_valid(self, monkeypatch):
        """Test that get_number handles invalid input and retries."""

        inputs = iter(["abc", "42"])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        result = get_number("Enter a number: ")
        assert result == 42


# ======================================================================================
# TESTS FOR GAMECONTROLLER (Integration tests)
# ======================================================================================


class TestGameController:
    """Test suite for the GameController class."""

    def test_game_controller_initialization(self):
        """Test that GameController initializes correctly."""
        from src.game import GameController
        controller = GameController()
        assert controller.game is None