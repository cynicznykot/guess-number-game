import random


# --- 1. Auxiliary Functions ---


def greet():
    print("=" * 50)
    print("🎯 Welcome to the game 'Guess the number'!")
    print("=" * 50)


def get_number(propt):
    while True:
        try:
            return int(input(propt))
        except ValueError:
            print("❌ Error! Please enter a NUMBER!")


def get_range():
    while True:
        start_user_step = get_number("🔢 Please enter any number for start step: ")
        end_user_step = get_number("🔢 Please enter any number for end step: ")
        if start_user_step == 6 and end_user_step == 7:
            print("😄 Six-seven.. Are you kidding? Please let's be serious!")
            continue
        if start_user_step < end_user_step:
            secret_number = random.randint(start_user_step, end_user_step)
            return start_user_step, end_user_step, secret_number
        print("Start must be less than end!")


def check_guess(user_guess, secret_number, start_user_step, end_user_step):
    if user_guess < start_user_step or user_guess > end_user_step:
        return False, f"Number must be from {start_user_step} to {end_user_step}"
    if user_guess == secret_number:
        return True, f"🎉🏆⭐ CONGRATULATION! You guessed the number {secret_number}!"
    elif user_guess < secret_number:
        return False, f"📈 The number is HIGHER! Try again!"
    else:
        return False, f"📉 The number is LOWER! Try again!"


# --- 2. Game logic ---


def play_game():
    start_user_step, end_user_step, secret_number = get_range()
    attempts = 0

    print(f"❓ I guessed from {start_user_step} to {end_user_step}!")

    while True:
        user_guess = get_number("💭 Your guess: ")
        is_correct, message = check_guess(user_guess, secret_number, start_user_step, end_user_step)

        if message == f"Number must be from {start_user_step} to {end_user_step}!":
            print(message)
            continue

        attempts += 1
        print(message)

        if is_correct:
            print(f"🔍 Your Attempts: {attempts}")
            break


def play_again():
    answer = input("🎮 Do you want to play again? (y/n): ").lower()
    return answer in ['yes', 'y', 'да', 'д']


# --- 3. Main func ---

def main():
    greet()
    while True:
        play_game()
        if not play_again():
            print(f"Thank you for playing. Goodbye! 👋")
            break


# --- 4. Entry point ---

if __name__ == "__main__":
    main()
