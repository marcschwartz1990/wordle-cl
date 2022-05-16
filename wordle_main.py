# When user inputs a guess, each letter is turned into a "column" instance

import random
import time
from termcolor import colored


# CLASSES

# I think I would design this a bit differently. I would create a wrapper class for the entire game, and use methods to perform actions.
#
# class WordleGame:
#     def create_row():
#         ...
#     def create_board():
#         ...
#     def run_game():
#         ...
#     the rest of the functions from 'MESSAGES' would live in here too 



# i don't love calling these things 'Squares' but i don't really have a better suggestion right now...
# i also think this entire class can just be:

# def colorize_square(letter, color='white'):
    # return colored(f'[{letter}]', color)

class Square:
    def __init__(self, letter, color='white'):
        self.letter = letter
        self.color = color

    # not used
    def change_color(self, new_color):
        """change instance color from default white to given color"""
        self.color = new_color
        return self.color

    def display_square(self):
        # doesn't look like this exists
        print(self.create_column())

    def create_formatted_square(self):
        """returns a complete column to be used in row class"""
        # one-liner:
        # return colored(f'[{self.letter}]', self.color)
        letter = self.letter
        color = self.color
        formatted_square = colored(f'[{letter}]', color)
        return formatted_square


# this class can just be one method create_row() on the main game class, no real benefit of using a class here.
class Row:
    def __init__(self, squares):
        self.squares = squares

    def create_formatted_row(self):
        # one liner here:
        # return ''.join([s for s in self.squares])
        row = []
        for square in self.squares:
            row.append(square)
        return ''.join(row)


# same here, just create_board() method
class Board:
    def __init__(self, rows):
        self.rows = rows

    def create_board(self):
        board = []
        for row in self.rows:
            # just `if row:` (don't need `is None`)
            if row is None:
                board.append('[ ][ ][ ][ ][ ]')
            else:
                board.append(row)
        return board


# FUNCTIONS


# MESSAGES
def display_welcome_message():
    print('Welcome to Wordle CL!\n')
    time.sleep(2)
    print('Created by Marc Schwartz\n')
    time.sleep(2)


def display_instructions():
    green_w = colored('[W]', 'green')
    yellow_i = colored('[I]', 'yellow')
    print('INSTRUCTIONS:\n'
          'Guess the WORDLE in 6 tries.\n'
          'Each guess must be a valid 5-letter word.\n'
          'After each guess, the board will display how close your guess was to the word.\n\n'
          'EXAMPLES:\n'
          f'{green_w}[E][A][R][Y]\n'
          'The letter "W" is in the word in the correct spot.\n\n'
          f'[P]{yellow_i}[L][L][S]\n'
          'The letter "I" is in the word in the wrong spot.\n\n'
          '[V][A][G][U][E]\n'
          'No color means the letters are not in the word.\n')
    while True:
        next_step = input('Type "c" to continue: ')
        if next_step == 'c':
            break
        else:
            print('Invalid input.')


def display_remaining_letters(guess, word, letters_remaining):
    for letter in guess:
        if letter.upper() not in word.upper() and letter.upper() in letters_remaining:
            letters_remaining.remove(f'{letter.upper()}')
    # you're using the name of the function as a variable inside it
    display_remaining_letters = ' '.join(letters_remaining)
    num_of_letters_remaining = len(letters_remaining)
    print(f'\nLetters Remaining ({num_of_letters_remaining}): {display_remaining_letters}')


# WORD LIST
def import_word_list(source_list):
    """imports word list from source_list and stores it in a python list"""
    with open(source_list, 'r') as file:
        all_text = file.read()
        words = [x for x in all_text.split()]
    return words


# VALIDATE USER INPUT
# this is a little misleading, as it does more than just validate the guess... it also prompts the user to input a guess.
# what i would do is move the while loop and `input` logic outside of this function and have this only be responsible for validation.
# this could be a good opportunity to explore custom Exceptions. Maybe this function could return True if valid, otherwise raise an Exception.
# you could have some new exception classes like:

# class GuessLengthException(Exception):
#   pass

# class InvalidWordException(Exception):
#   pass

# then the calling function could handle the exception:
# try:
#     is_valid_guess = validate_user_guess(word_list) # this fn returns True, or raises an Exception
# except GuessLengthException:
#     print('Word must be 5 letters')
# except InvalidWordException:
#     print('Invalid guess')
def validate_user_guess(word_list):
    """Validates the user's guess. Checks for correct length and checks it against the supplied word list"""
    while True:
        user_guess = input('\nEnter a 5-Letter Word: ')
        if len(user_guess) == 5 and user_guess.lower() in word_list:
            return user_guess
        else:
            if len(user_guess) != 5:
                print('Word must be exactly 5 letters.')
            if user_guess.lower() not in word_list and len(user_guess) == 5:
                print('Word not found.')


def check_for_solution(guess, word):
    if guess == word:
        return True

# naming: colorize_row? generate_row? something that makes it obvious that a row is being returned
def compare_guess_against_answer(guess, answer):
    """Compare user's guess with the answer. Returns new board row"""
    # if you know your answer list is in lower, why use upper?
    guess_comparison = [x.upper() for x in guess]
    word_comparison = [x.upper() for x in answer]
    row = []
    # instead of using range, check out `zip` to iterate through both lists simultaneously
    for i in range(5):
        # Check for correct letter in correct position
        if guess_comparison[i] == word_comparison[i]:
            letter = Square(guess_comparison[i], 'green')
            row.append(letter.create_formatted_square())

        # Check for correct letter in wrong position
        elif guess_comparison[i] != word_comparison[i] and guess_comparison[i] in word_comparison:
            letter = Square(guess_comparison[i], 'yellow')
            row.append(letter.create_formatted_square())

        # Check for wrong letter
        elif guess_comparison[i] not in word_comparison:
            letter = Square(guess_comparison[i])
            row.append(letter.create_formatted_square())

    return row


# GAMEPLAY
def generate_random_word(word_list):
    """Generate random word from words list to be chosen word for the game"""
    return random.choice(word_list)


# MAIN FUNCTION
def main():
    display_welcome_message()
    display_instructions()

    # these should be global
    words = import_word_list('wordle-answers-alphabetical.txt')
    valid_guesses = import_word_list('wordle-allowed-guesses.txt')

    # this stuff would live as attributes of your Game class
    current_board = [None for x in range(6)]
    answer = generate_random_word(words)
    # check out `string.ascii_uppercase`
    letters_remaining = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                         'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
                         ]

    # Start guesses
    # this loop would be your 'main' or 'run' function in the Game class
    for i in range(6):
        # there should be no reason to have to pass `valid_guesses` here since it's static; just define it globally
        guess = validate_user_guess(valid_guesses)
        # this naming is confusing, I would never expect 'compare_guess_against_answer' to return a row
        new_board_row = compare_guess_against_answer(guess, answer)
        unformatted_row = Row(new_board_row)
        formatted_row = unformatted_row.create_formatted_row()
        current_board[i] = formatted_row  # Replace None value with current row
        board = Board(current_board)
        new_board = board.create_board()
        for row in new_board:
            print(row)
        display_remaining_letters(guess, answer, letters_remaining)

        # just one line this: 
        # if (check_for_solution()):
        #    break
        solution = check_for_solution(guess, answer)
        if solution == True:
            break

    # Decide whether puzzle is solved or not
    # LOOK INTO THIS LINE. IS IT NECESSARY?
    green_answer = colored(f'{answer}', 'green')
    if guess == answer:
        print(f'\nCongratulations! You guessed the word: {green_answer.upper()}')
    else:
        print(f'\nThe correct word was: {green_answer.upper()}\n\nSorry, you failed to guess in 6 tries.')


def replay_prompt():
    prompt = input('\nWould you like to play again? (y/n):')
    if prompt == 'y':
        main()
        replay_prompt()
    else:
        print('\n\nThank you for playing!\n')


# RUN PROGRAM
main()
replay_prompt()
