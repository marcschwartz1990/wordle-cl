import random
import string
import time
import sqlite3
from termcolor import colored
from exceptions import *
from database import Database


db = Database('players.db')


class WordleGame:

    def __init__(self):
        self.squares = []
        self.rows = [None] * 6
        self.player_name = None
        self.guesses = 6
        self.letters_remaining = set(string.ascii_lowercase)

    def create_row(self):
        """Formats each letter from user's guess and returns a combined displayable row"""
        return ''.join([s for s in self.squares])

    def display_board(self):
        for row in self.rows:
            if row:
                print(row)
            else:
                print('[ ][ ][ ][ ][ ]')

    def reset_squares(self):
        self.squares = []

    def reset_rows(self):
        self.rows = [None] * 6

    def adjust_remaining_letters(self, user_guess, answer):
        for char in user_guess:
            if char not in answer and char in self.letters_remaining:
                self.letters_remaining.remove(char)

    def display_remaining_letters(self):
        print(f'\nLetters Remaining ({len(self.letters_remaining)}): {" ".join(sorted(self.letters_remaining)).upper()}')

    def easy_mode(self):
        """Set number of allowed guesses to 8"""
        self.rows = [None] * 8
        self.guesses = 8

    def difficult_mode(self):
        """Set number of allowed guesses to 4"""
        self.rows = [None] * 4
        self.guesses = 4

    # DATABASE FUNCTIONS

    def insert_player(self):
        try:
            db.cursor.execute("INSERT INTO players VALUES (:username, :games_played)",
                              {'username': self.player_name, 'games_played': 0})
            db.conn.commit()
        except sqlite3.IntegrityError:
            print('\nplayer already in database\n')

    def increment_games_played(self):
        db.cursor.execute(
            """UPDATE players SET games_played = games_played + 1 
            WHERE username = :username""",
            {'username': self.player_name})
        db.conn.commit()

    def run_game(self):
        create_table_players = """CREATE TABLE players (
                    username TEXT,
                    games_played INTEGER,
                    UNIQUE(username)
                    )"""
        db.execute_query(create_table_players)

        display_welcome_message()
        display_instructions()

        self.player_name = input('\nEnter your username or "guest": ')
        if self.player_name != 'guest':
            self.insert_player()

        while True:
            modes = list(('easy', 'normal', 'difficult'))
            mode = input('Choose a mode (easy, normal, difficult): ').lower()
            if mode not in modes:
                continue
            else:
                break
        set_mode(self, mode)
        print(f'\nGood luck, {self.player_name}!\n')

        answer = random.choice(possible_answers)

        for i in range(self.guesses):
            self.display_board()
            self.display_remaining_letters()
            while True:
                guess = input('\nEnter a 5-letter word: ').lower()
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
            self.adjust_remaining_letters(guess, answer)
            self.squares = []
            if guess == answer:
                break

        if guess == answer:
            print(f'\nCongratulations! You guessed the word: {colored(answer.upper(), "green")}')
        else:
            print(
                f'\nThe correct word was: {colored(answer.upper(), "green")}\n'
                f'\nSorry, you failed to guess in {self.guesses} tries.'
            )
        print('GAME OVER')

        self.increment_games_played()
        db.close()


def main():
    while True:
        game = WordleGame()
        game.run_game()
        if replay_prompt() is False:
            break
        game.reset_squares()
        game.reset_rows()
    print('\n\nThank you for playing!\n')


def display_welcome_message():
    print('Welcome to Wordle CL!\n')
    time.sleep(2)
    print('Created by Marc Schwartz\n')
    time.sleep(2)


def display_instructions():
    green_w = colored('[W]', 'green')
    yellow_i = colored('[I]', 'yellow')
    print('INSTRUCTIONS:\n'
          'Guess the WORDLE in the given number of tries (based on mode).\n'
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


def replay_prompt():
    prompt = input('\nWould you like to play again? (y/n): ').lower()
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
    guess_letters = list(guess)
    answer_letters = list(answer)
    for guess, answer in zip(guess_letters, answer_letters):
        if guess == answer:
            row.append(colorize_square(guess.upper(), 'green'))

        elif guess != answer and guess in answer_letters:
            row.append(colorize_square(guess.upper(), 'yellow'))

        elif guess not in answer_letters:
            row.append(colorize_square(guess.upper()))
    return row


def validate_user_guess(user_guess):
    if len(user_guess) != 5:
        raise GuessLengthException
    elif user_guess not in possible_guesses:
        raise InvalidWordException
    return True


def set_mode(game, mode):
    if mode == 'normal':
        return
    elif mode == 'easy':
        game.easy_mode()
    elif mode == 'difficult':
        game.difficult_mode()


if __name__ == '__main__':
    possible_answers = import_word_list('wordle-answers-alphabetical.txt')
    possible_guesses = import_word_list('wordle-allowed-guesses.txt')
    main()
