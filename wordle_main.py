import random
import time
from termcolor import colored


class GuessLengthException(Exception):
    """Raise if len(guess) != 5."""
    pass


class InvalidWordException(Exception):
    """Raises if word not in possible_guesses."""
    pass


class WordleGame:
    squares = []
    rows = [None] * 6
    player_name = None

    def create_row(self):
        """Formats each letter from user's guess and returns a combined displayable row"""
        return ''.join([s for s in self.squares])

    def display_board(self):
        for row in self.rows:
            if row is not None:
                print(row)
            else:
                print('[ ][ ][ ][ ][ ]')

    def run_game(self):

        answer = random.choice(possible_answers)
        letters_remaining = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                             'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
                             ]

        self.display_welcome_message()
        self.display_instructions()
        self.player_name = input('Enter your name: ')

        for i in range(6):
            print(answer)
            while True:
                guess = input('Enter a 5-letter word: ').lower()
                try:
                    validate_user_guess(guess)
                    break
                except GuessLengthException:
                    print('Word must be 5 letters')
                except InvalidWordException:
                    print('Invalid guess')

            for letter in generate_row(guess, answer):
                self.squares.append(letter)

            self.rows[i] = self.create_row()
            self.display_board()
            display_remaining_letters(guess, answer, letters_remaining)
            self.reset_squares()

            if guess == answer:
                break

        if guess == answer:
            print(f'\nCongratulations! You guessed the word: {colored(answer.upper(), "green")}')
        else:
            print(
                f'\nThe correct word was: {colored(answer.upper(), "green")}\n\nSorry, you failed to guess in 6 tries.')
        print('GAME OVER')

    def record_stats(self):
        with open('wordle-stats.txt', 'a') as f:
            f.write(f'\n{self.player_name} played this game.')

    def reset_squares(self):
        self.squares = []

    def reset_rows(self):
        self.rows = [None] * 6

    def display_welcome_message(self):
        print('Welcome to Wordle CL!\n')
        time.sleep(2)
        print('Created by Marc Schwartz\n')
        time.sleep(2)

    def display_instructions(self):
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


def main():
    game = WordleGame()
    while True:
        game.run_game()
        game.record_stats()
        if replay_prompt() is False:
            break
        game.reset_squares()
        game.reset_rows()
    print('\n\nThank you for playing!\n')


def replay_prompt():
    prompt = input('\nWould you like to play again? (y/n):').lower()
    if prompt == 'y':
        return True
    return False


def import_word_list(source_list):
    """imports word list from source_list and stores it in a python list"""
    with open(source_list, 'r') as file:
        all_text = file.read()
        words = [x for x in all_text.split()]
    return words


def colorize_square(letter, color='white'):
    return colored(f'[{letter}]', color)


def generate_row(guess, answer):
    """Compare user's guess with the answer. Returns new board row"""
    row = []
    guess_letters = [x for x in guess]
    answer_letters = [x for x in answer]
    comparison = zip(guess_letters, answer_letters)
    for letter in comparison:
        if letter[0] == letter[1]:
            row.append(colorize_square(letter[0].upper(), 'green')) # Where should I put .upper()?

        elif letter[0] != letter[1] and letter[0] in answer_letters:
            row.append(colorize_square(letter[0].upper(), 'yellow'))

        elif letter[0] not in answer_letters:
            row.append(colorize_square(letter[0].upper()))

    return row


def validate_user_guess(user_guess):
    if len(user_guess) != 5:
        raise GuessLengthException
    elif user_guess not in possible_guesses:
        raise InvalidWordException
    return True


def display_remaining_letters(user_guess, answer, letters_remaining):
    for char in user_guess:
        if char not in answer and char.upper() in letters_remaining:
            letters_remaining.remove(f'{char.upper()}')
    remaining_letters = ' '.join(letters_remaining)
    num_of_letters_remaining = len(letters_remaining)
    print(f'\nLetters Remaining ({num_of_letters_remaining}): {remaining_letters}')


if __name__ == '__main__':
    possible_answers = import_word_list('wordle-answers-alphabetical.txt')
    possible_guesses = import_word_list('wordle-allowed-guesses.txt')
    main()
