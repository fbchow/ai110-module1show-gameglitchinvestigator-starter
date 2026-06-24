def get_range_for_difficulty(difficulty: str):
    """Return the inclusive guessing range for a given difficulty level.

    Args:
        difficulty: The difficulty name, e.g. "Easy", "Normal", or "Hard".

    Returns:
        A (low, high) tuple of ints describing the inclusive range the
        secret number can fall in. Unknown difficulties fall back to the
        default range.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100


def parse_guess(raw: str, low: int, high: int):
    """Parse raw user input into an integer guess within the given range.

    Args:
        raw: The raw guess string entered by the user. May be None or empty.
        low: The inclusive lower bound the guess must fall within.
        high: The inclusive upper bound the guess must fall within.

    Returns:
        A (ok, guess_int, error_message) tuple:
            ok: True if parsing succeeded, False otherwise.
            guess_int: The parsed int guess, or None when parsing failed.
            error_message: A user-facing error string when parsing failed,
                or None on success.
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw.strip() == "":
        return False, None, "Enter a guess."

    try:
        value = int(raw)
    except ValueError:
        return False, None, "That is not a number."

    if value < low or value > high:
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


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
    if outcome == "Win":
        points = max(10, 100 - 10 * attempt_number)
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
