class GuessLengthException(Exception):
    """Raise if len(guess) != 5."""
    pass


class InvalidWordException(Exception):
    """Raises if word not in possible_guesses."""
    pass
