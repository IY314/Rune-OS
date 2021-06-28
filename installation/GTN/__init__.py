import random
import sys
from system import homepage
from system import utils


def launch():
    home()


def loop(low, high, max_guesses):
    guesses = max_guesses
    number = random.randint(low, high)
    while True:
        print(f'Guess a number between {str(low)} and {str(high)}. You have {str(guesses)} guesses.')
        try:
            guess = int(input('>'))
        except ValueError:
            print('Invalid answer.')
            continue
        if guess == number:
            print(f'You guessed the number in {str(max_guesses - guesses + 1)} guesses!')
            return home()
        elif guess > number:
            if guesses > 5: print('Try lower.')
        else:
            if guesses > 5: print('Try higher.')
        guesses -= 1
        if guesses == 0:
            print('You ran out of guesses. Better luck next time...')
            return home()


def home():
    def easy():
        return loop(0, 10, 7)

    def medium():
        return loop(0, 50, 15)

    def hard():
        return loop(0, 100, 30)

    def run():
        while True:
            utils.make_choice_box('Guess the Number',
                ('choose EASY', easy),
                ('choose MEDIUM', medium),
                ('choose HARD', hard),
                anything_else=('quit', homepage.launch)
            )

    utils.make_choice_box()
    prompt = 'Enter 1 to play Guess the Number.\nEnter anything else to exit.'
    print(prompt)
    action = input('>')
    if action == '1':
        while True:
            prompt2 = 'Enter 1 to choose EASY\nEnter 2 to choose MEDIUM\nEnter 3 to choose HARD'
            print(prompt2)
            diff = input('>')
            if diff == '1':
                return loop(0, 10, 7)
            elif diff == '2':
                return loop(0, 50, 15)
            elif diff == '3':
                return loop(0, 100, 30)
            elif diff == '':
                from system import homepage
                homepage.launch()
            else:
                print('Invalid answer.')
                continue
    else:
        from system import homepage
        homepage.launch()
