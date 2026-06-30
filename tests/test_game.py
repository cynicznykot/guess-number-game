"""
Unit tests fo the "Guess the Number" game.

Tests cover all core game functions including input validation,
guess checking, temperature calculation and game flow control.
"""


import pytest
from unittest.mock import patch
from src.game import (
    check_guess,
    get_temperature,
    get_number,
    get_range,
    play_again,
    greet
)


# =================================================================================================
# 1. CHECK GUESS TESTS
# =================================================================================================


def test_check_guess_correct():
    """
    Test correct guess detection.

    When the player guesses the exact secret number, the function should
    return True and include a congratulatory message.
    """
    is_correct, message = check_guess(user_guess=50, secret_number=50, start_user_step=1, end_user_step=100)
    assert is_correct is True
    assert "CONGRATULATION" in message


def test_check_guess_lower():
    """
    Test guess that is lower than the secret number.

    The function should return False and include the number is higher.
    """
    is_correct, message = check_guess(user_guess=30, secret_number=50, start_user_step=1, end_user_step=100)
    assert is_correct is False
    assert "HIGHER" in message


def test_check_guess_out_of_range():
    """
    Test guess that is outside the valid number range.

    The function should reject guesses below the minimum or above the maximum.
    """
    is_correct, message = check_guess(user_guess=150, secret_number=50, start_user_step=1, end_user_step=100)
    assert is_correct is False
    assert "must be from" in message


# ==================================================================================================
# 2. TEMPERATURE TESTS
# ==================================================================================================


def test_temperature_very_hot():
    """
    Test "Very hot" temperature level (≤ 5% of range).

    When the guess is extremely cose to the secret number,
    the feedback should indicate "Very hot".
    """
    temp = get_temperature(50, 48, 1, 100)
    assert "Very hot" in temp


def test_temperature_hot():
    """
    Test "Hot" temperature level (5-15% of range).

    When the guess is close to the secret number,
    the feedback should indicate "Hot".
    """
    temp = get_temperature(secret_number=50, user_guess=40, start_user_step=1, end_user_step=100)
    assert "Hot" in temp


def test_temperature_warm():
    """
    Test "Warm" temperature level (15-30% of range).

    When the guess is moderately close to the secret number,
    the feedback should indicate "Warm".
    """
    temp = get_temperature(secret_number=50, user_guess=25, start_user_step=1, end_user_step=100)
    assert "Warm" in temp


def test_temperature_cold():
    """
    Test "Cold" temperature level (> 60% of range).

    When the guess is far from the secret number,
    the feedback should indicate "Cold" or "Cool".
    """
    temp = get_temperature(secret_number=50, user_guess=1, start_user_step=1, end_user_step=100)
    assert "Cold" in temp or "Cool" in temp


# ==================================================================================================
# 3. NUMBER INPUT TESTS
# ==================================================================================================


def test_get_number_valid():
    """Test valid number range input.

    The function should accept a valid range and generate
    a secret number within that range.
    """
    with patch('builtins.input', return_value='42'):
        result = get_number("Enter: ")
        assert result == 42


def test_get_number_invalid_then_valid():
    """Test invalid range followed by valid range.

    When the start is greater than the end, the function should reject
    the input and prompt again.
    """
    with patch('builtins.input', side_effect=['abc', '42']):
        result = get_number("Enter: ")
        assert result == 42


# =================================================================================================
# 4. RANGE INPUT TESTS
# =================================================================================================


def test_get_range_valid():
    """Test valid number range input.

    The finction should accept a valid range and generate
    a secret number within that range.
    """
    with patch('builtins.input', side_effect=['1', '100']):
        start, end, secret = get_range()
        assert start == 1
        assert end == 100
        assert 1 <= secret <= 100


def test_get_range_invalid_then_valid():
    """Test invalid range followed by valid range.

    When the start is greater than the end, the function should reject
    the input and prompt again."""
    with patch('builtins.input', side_effect=['100', '1', '1', '100']):
        start, end, secret = get_range()
        assert start == 1
        assert end == 100


# =================================================================================================
# 5. PLAY AGAIN TESTS
# =================================================================================================


def test_play_again_yes():
    """Test positive response to "play again" prompt.

    The function should return True for 'y', 'yes', 'да', 'д'.
    """
    with patch('builtins.input', return_value='y'):
        assert play_again() is True


def test_play_again_no():
    """Test negative response to "play again" prompt.

    The function should return False for 'n' or 'no'."""
    with patch('builtins.input', return_value='n'):
        assert play_again() is False


# =================================================================================================
# 6. GREETING TEST
# =================================================================================================


def test_greet_output(capsys):
    """Test the welcome message output.

    The greet function should display a message containing "Welcome".
    """
    greet()
    captured = capsys.readouterr()
    assert "Welcome" in captured.out


# =================================================================================================
# 7. ADDITIONAL TESTS
# =================================================================================================


def test_temperature_boundary():
    """Test the boundary between "Hot" and "Warm" temperature levels.

        At exactly 15% distance, the function could return either
        "Hot" or "Warm" temperature level."""
    temp = get_temperature(secret_number=50, user_guess=35, start_user_step=1, end_user_step=100)  # Exactly 15% distance
    assert "Hot" in temp or "Warm" in temp