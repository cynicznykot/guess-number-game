import random


def main():
    """ Main function game """

    # Greeting
    print("=" * 50)
    print("🎯 Welcome to the game 'Guess the number'!")
    print("=" * 50)

    # Setting the range
    start_user_num = int(input("Please enter any number for start step: "))
    end_user_num = int(input("Please enter any number for end step: "))

    secret_num = random.randint(start_user_num, end_user_num)
    print(f"🔢 I guessed the number from {start_user_num} to {end_user_num}!")

    # Number of attempts
    attempts = 0

    # Input validation
    while True:
        user_guess = int(input("Please enter your guess: "))

        attempts += 1

        if user_guess == secret_num:
            print(f"🎉 CONGRATULATION! You guessed the number {secret_num}!")
            print(f"📊 Your attempts: {attempts}!")
            break

        elif user_guess < secret_num:
            print(f"📈 The number is HIGHER! Try again!")
        else:
            print(f"📉 The number is LOWER! Try again!")

if __name__ == "__main__":
    main()


