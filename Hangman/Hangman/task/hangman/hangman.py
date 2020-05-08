# Write your code here
import random


def make_hint(secret, guessed):
    hint = ""
    for c in secret:
        hint += c if c in guessed else '-'
    return hint



def play():
    words = ['python', 'java', 'kotlin', 'javascript']
    secret = random.choice(words)
    guessed = set()
    tried = set()
    lives = 8

    while lives > 0:
        hint = make_hint(secret, guessed)
        print()
        print(hint)

        if set(secret) == guessed:
            print("You guessed the word!")
            break

        guess = input("Input a letter: ")

        if len(guess) != 1:
            print('You should print a single letter')
        elif not guess.isalpha() or not guess.islower():
            print('It is not an ASCII lowercase letter')
        elif guess in tried:
            print('You already typed this letter')
        else:
            tried.add(guess)
            if guess in secret:
                guessed.add(guess)
            else:
                print('No such letter in the word')
                lives -= 1

    print('You survived!' if lives > 0 else 'You are hanged!')



print('H A N G M A N')

while True:
    opt = input('Type "play" to play the game, "exit" to quit: ')
    if opt == 'play':
        play()
    elif opt == "exit":
        break

