import random

secret_number = random.randint(1, 100)
guess_count = 0
is_correct = False

print("--- ยินดีต้อนรับเข้าสู่เกม ทายตัวเลข (1-100) ---")

while not is_correct:
    try:
        guess = int(input("Guess the number: "))
        guess_count += 1

        if guess < 1 or guess > 100:
            print("Please guess between (1-100)!")
            continue

        if guess == secret_number:
            print(f"Correct! The answer is: {secret_number}")
            print(f"You took {guess_count} attempts.")
            is_correct = True
        elif guess < secret_number:
            print("Too low!")
        else:
            print("Too high!")

        if guess_count >= 10 and not is_correct:
            print(f"Game Over! You've reached the limit of 10 attempts.")
            print(f"The correct number was {secret_number}")
            is_correct = True

    except ValueError:
        print("Error: Enter only integers!")