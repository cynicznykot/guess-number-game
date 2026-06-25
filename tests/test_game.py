import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from main import check_guess, get_temperature, compare_with_previous

# Tests
def test_correct_guess():
    result, message = check_guess(50, 50, 1, 100)
    assert result == True


def test_guess_too_low():
    result, message = check_guess(30, 50, 1, 100)
    assert result == False


def test_guess_too_high():
    result, message = check_guess(70, 50, 1, 100)
    assert result == False


def test_guess_out_of_range_low():
    result, message = check_guess(0, 50, 1, 100)
    assert result == False


def test_guess_out_of_range_high():
    result, message = check_guess(101, 50, 1, 100)
    assert result == False


def test_temperature_very_hot():
    temp = get_temperature(50, 45, 1, 100)
    assert "Very hot" in temp


def test_temperature_hot():
    temp = get_temperature(50, 30, 1, 100)
    assert "Hot" in temp


def test_temperature_warm():
    temp = get_temperature(50, 10, 1, 100)
    assert "Warm" in temp


def test_temperature_cold():
    temp = get_temperature(50, 120, 1, 100)
    assert "Cold" in temp


def test_compare_with_previous():
    assert "getting closer" in compare_with_previous(10, 5)
    assert "moving away" in compare_with_previous(5, 10)
    assert "same distance" in compare_with_previous(7, 7)

if __name__ == "__main__":
    tests = [
        test_correct_guess,
        test_guess_too_low,
        test_guess_too_high,
        test_guess_out_of_range_low,
        test_guess_out_of_range_high,
        test_temperature_very_hot,
        test_temperature_hot,
        test_temperature_warm,
        test_temperature_cold,
        test_compare_with_previous,
    ]

    passed = 0
    for test in tests:
        try:
            test()
            print(f"✅ {test.__name__} - OK")
            passed += 1
        except AssertionError:
            print(f"❌ {test.__name__} - FAILED")

    print(f"\n{'=' * 50}")
    print(f"✅ {passed}/{len(tests)} тестов пройдено")
    print(f"{'=' * 50}")