def get_range_for_difficulty(difficulty: str):
    """Return the inclusive guessing range for a given difficulty level.

    Args:
        difficulty: The difficulty name, e.g. "Easy", "Normal", or "Hard".

    Returns:
        A (low, high) tuple of ints describing the inclusive range the
        secret number can fall in. Unknown difficulties fall back to the
        default range.
    """
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


def parse_guess(raw: str):
    """Parse raw user input into an integer guess.

    Args:
        raw: The raw guess string entered by the user. May be None or empty.

    Returns:
        A (ok, guess_int, error_message) tuple:
            ok: True if parsing succeeded, False otherwise.
            guess_int: The parsed int guess, or None when parsing failed.
            error_message: A user-facing error string when parsing failed,
                or None on success.
    """
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


def check_guess(guess, secret):
    """Compare a guess against the secret number.

    Args:
        guess: The player's guessed number.
        secret: The secret number to be guessed.

    Returns:
        An (outcome, message) tuple:
            outcome: One of "Win", "Too High", or "Too Low".
            message: A user-facing message describing the outcome.
    """
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Compute the new score after a guess.

    Args:
        current_score: The player's score before this guess.
        outcome: The result of the guess, e.g. "Win", "Too High", "Too Low".
        attempt_number: The number of the current attempt.

    Returns:
        The updated score as an int.
    """
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")
