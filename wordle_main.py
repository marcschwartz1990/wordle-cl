# When user inputs a guess, each letter is turned into a "column" instance

import random
import time
from termcolor import colored


# CLASSES

class Square:
    def __init__(self, letter, color='white'):
        self.letter = letter
        self.color = color

    def change_color(self, new_color):
        """change instance color from default white to given color"""
        self.color = new_color
        return self.color

    def display_square(self):
        print(self.create_column())

    def create_formatted_square(self):
        """returns a complete column to be used in row class"""
        letter = self.letter
        color = self.color
        formatted_square = colored(f'[{letter}]', color)
        return formatted_square


class Row:
    def __init__(self, squares):
        self.squares = squares

    def create_formatted_row(self):
        row = []
        for square in self.squares:
            row.append(square)
        return ''.join(row)


class Board:
    def __init__(self, rows):
        self.rows = rows

    def create_board(self):
        board = []
        for row in self.rows:
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


def compare_guess_against_answer(guess, answer):
    """Compare user's guess with the answer. Returns new board row"""
    guess_comparison = [x.upper() for x in guess]
    word_comparison = [x.upper() for x in answer]
    row = []
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

    words = import_word_list('wordle-answers-alphabetical.txt')
    valid_guesses = import_word_list('wordle-allowed-guesses.txt')
    current_board = [None for x in range(6)]
    answer = generate_random_word(words)
    letters_remaining = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                         'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
                         ]

    # Start guesses
    for i in range(6):
        guess = validate_user_guess(valid_guesses)
        new_board_row = compare_guess_against_answer(guess, answer)
        unformatted_row = Row(new_board_row)
        formatted_row = unformatted_row.create_formatted_row()
        current_board[i] = formatted_row  # Replace None value with current row
        board = Board(current_board)
        new_board = board.create_board()
        for row in new_board:
            print(row)
        display_remaining_letters(guess, answer, letters_remaining)

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
