"""
Guess the Number Game.

A console-based game where the player guesses a randomly generated number
within a user-defined range. The game provides hints and temperature feedback.
"""

import random
import time
from typing import Optional, Tuple


# ======================================================================================
# 1. HELPER FUNCTIONS (standalone)
# ======================================================================================


def get_number(prompt: str) -> int:
    """
    Get a valid integer from the user.

    Continuously prompts the user until a valid integer is entered.
    Handles ValueError exceptions and displays an error message.

    Args:
        prompt (str): The message to display to the user.

    Returns:
        int: A valid integer entered by the user.
    """
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("❌ Please enter a NUMBER!")


# ======================================================================================
# 2. MAIN GAME CLASS
# ======================================================================================


class GuessNumberGame:

    """
    A class representing the "Guess the Number" game.

    The player must guess a random number within a specified range.
    After each attempt, the game provides a hint whether the guessed
    number is higher of lower than the secret number.

    Attributes:
        min_number (int): Minimum number in the range (inclusive).
        max_number (int): Maximum number in the range (inclusive).
        secret_number (int): The number randomly chosen by the computer.
        attempts (int): The number of attempts made by the player.
        max_attempts (Optional[int]): The maximum number of attempts allowed.
    """

    def __init__(self, min_number: int, max_number: int, max_attempts: Optional[int] = None) -> None:
        """
        Initialize the game with specified parameters.

        Args:
            min_number (int): Lower bound of the number range (inclusive).
            max_number (int): Upper bound of the number range (inclusive).
            max_attempts (Optional[int]): Maximum allowed attempts (None for unlimited).

        Raises:
            ValueError: If min_number >= max_number or range is too small.
        """

        # Validate the number range
        if min_number >= max_number:
            raise ValueError("The minimum number must be less than the maximum number.")
        if max_number - min_number < 1:
            raise ValueError("Range must contain at least one number.")

        self.min_number = min_number
        self.max_number = max_number
        self.max_attempts = max_attempts
        # Generate a random secret number within the specified range
        self.secret_number = random.randint(min_number, max_number)
        self.attempts = 0

    def guess(self, number: int) -> str:
        """
        Process the player's guess and return feedback.

        Args:
            number (int): The number guessed by the player.

        Raises:
            ValueError: If the number is outside the valid range.
        """

        # Validate that the guess is within the allowed range
        if not (self.min_number <= number <= self.max_number):
            raise ValueError(f"The number must be between {self.min_number} and "
                             f"{self.max_number}")

        self.attempts += 1

        # Check if the player has exceeded the maximum attempts
        if self.max_attempts and self.attempts > self.max_attempts:
            return f"Maximum attempts exceeded! The secret number was {self.secret_number}."

        # Compare the guess with the secret number
        if number == self.secret_number:
            return "🎉🏆⭐ CONGRATULATION! You guessed the number!"
        elif number < self.secret_number:
            return f"📈 The number is HIGHER! Try again!"
        else:
            return f"📉 The number is LOWER! Try again!"

    def get_temperature(self, user_guess: int) -> str:
        """
        Calculate how close the guess is to the secret number.

        Args:
            user_guess (int): The number guessed by the player.

        Returns:
            str: A temperature-based feedback message.
        """

        distance = abs(user_guess - self.secret_number)
        max_distance = self.max_number - self.min_number

        # Avoid division by zero if range is 0
        if max_distance == 0:
            return "🔥 You're right on target!"

        percent = (distance / max_distance) * 100

        if percent <= 5:
            return f"🔥 Very hot! You almost guessed it!"
        elif percent <= 15:
            return f"☀️ Hot! You're close!"
        elif percent <= 30:
            return f"🌤️ Warm. Keep up the good work!"
        elif percent <= 60:
            return "🌥️ Cool. You're getting there."
        else:
            return f"❄️ Cold. You're far away."

    def is_game_over(self) -> bool:
        """
        Check if the game has finished.

        Returns:
            bool: True if the game is over, False otherwise.
        """

        if self.max_attempts:
            return self.attempts >= self.max_attempts
        return False

    def reset(self) -> None:
        """Reset the game with a new random secret number."""
        self.secret_number = random.randint(self.min_number, self.max_number)
        self.attempts = 0

    def get_stats(self) -> dict:
        """
        Retrieve current game statistics.

        Returns:
            dict: Dictionary containing game statistics.
        """
        return {
            'attempts': self.attempts,
            'max_attempts': self.max_attempts,
            'range': f"{self.min_number} to {self.max_number}",
            'is_finished': self.is_game_over(),
        }




    def get_range():
        """
        Get a valid range from the user.

        Prompts for start and end values, validates them and generates
        a random secret number within the range.
        """
        while True:
            start_user_step = get_number("🖥️ Please enter any number for start step: ")

            end_user_step = get_number("🖥️ Please enter any number for end step: ")

            # Easter meme egg: 6-7 joke
            if start_user_step == 6 and end_user_step == 7:
                print("😄 Six-seven.. Are you kidding? Please let's be serious!")
                continue
            if start_user_step < end_user_step:
                secret_number = random.randint(start_user_step, end_user_step)
                return start_user_step, end_user_step, secret_number

            print("❌ Start must be less than end!")


# ===================================================================================
# 2. GAME LOGIC FUNCTIONS
# ===================================================================================


    def play_game():
        """
        Run a single game session.

        Handles the main game loop: range setup, guessing, attempt tracking,
        and providing feedback. The game continues until the player guesses
        the secret number.
        """

        start_user_step, end_user_step, secret_number = get_range()
        attempts = 0

        print(f"🤔 I guessed from {start_user_step} to {end_user_step}!")

        while True:
            user_guess = get_number("📝 Your guess: ")
            is_correct, message = check_guess(user_guess, secret_number, start_user_step, end_user_step)

            # Handle out-of-range guesses without counting attempts
            if message == f"🤯 Number must be from {start_user_step} to {end_user_step}!":
                print(message)
                continue

            attempts += 1

            if is_correct:
                print(message)
                print(f"📊 Your Attempts: {attempts}")
                break

            temp = get_temperature(secret_number, user_guess, start_user_step, end_user_step)
            print(message)
            print(temp)


    def play_again():
        """
        Ask the player if they want to play again.
        """
        user_answer = input("🎮 Do you want to play again? (y/n): ").lower()
        return user_answer in ['yes', 'y', 'да', 'д']


# ===============================================================================================
# 3. MAIN FUNC
# ===============================================================================================


    def main():
        """
        Main game controller.

        Greets the player and runs the game loop. After each game,
        asks if the player wants to play again.
        """
        greet()

        while True:
            play_game()

            if not play_again():
                print(f"Thank you for playing. Goodbye! 👋")
                break

