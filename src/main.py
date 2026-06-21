import random


def main():
    """ Main function game """

    # Greeting
    print("=" * 50)
    print("🎯 Welcome to the game 'Guess the number'!")
    print("=" * 50)

    # Setting the range with error handling
    while True:
        try:
            start_user_step = int(input("Please enter any number for start step: "))
            break
        except ValueError:
            print("❌ Error! Please enter a NUMBER for start step!")

    while True:
        try:
            end_user_step = int(input("Please enter any number for end step: "))
            break
        except ValueError:
            print("❌ Error! Please enter a NUMBER for end step!")

    if start_user_step >= end_user_step:
        print("❌ Error! The start number is higher than the end number!")
        return

    # Guess the number
    random_num = random.randint(start_user_step, end_user_step)
    print(f"🔢 I guessed the number from {start_user_step} to {end_user_step}!")

    # Number of attempts
    attempts = 0

    # Input validation
    while True:
        user_guess = int(input("Please enter your guess: "))

        attempts += 1

        if user_guess == random_num:
            print(f"🎉 CONGRATULATION! You guessed the number {random_num}!")
            print(f"📊 Your attempts: {attempts}!")
            break

        elif user_guess < random_num:
            print(f"📈 The number is HIGHER! Try again!")
        else:
            print(f"📉 The number is LOWER! Try again!")

if __name__ == "__main__":
    main()

# Repeating the game
while True:
    play_again = input("Do you want to play again? (y/n): ").lower()
    if play_again in ['yes', 'y', 'да', 'д']:
            main()
    else:
        print("👋 Thank you for playing! Goodbye!")
        break


