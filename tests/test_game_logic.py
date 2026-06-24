from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_high_low_hints_point_the_right_way():
    # Regression: the hint messages used to be swapped.
    # A guess ABOVE the secret must tell the player to go LOWER.
    _, message = check_guess(60, 50)
    assert "LOWER" in message

    # A guess BELOW the secret must tell the player to go HIGHER.
    _, message = check_guess(40, 50)
    assert "HIGHER" in message

def test_banner_range_reflects_difficulty():
    # Regression: the guess banner used to hardcode "between 1 and 100"
    # regardless of difficulty. The range must track the selected level.
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 50)
    assert get_range_for_difficulty("Hard") == (1, 100)

    # The banner string is built from this range, so the upper bound shown
    # must match the difficulty's high value.
    low, high = get_range_for_difficulty("Hard")
    banner = f"Guess a number between {low} and {high}. "
    assert "between 1 and 100" in banner


def test_parse_guess_rejects_decimal_input():
    # Regression: "6.9" used to be silently truncated to 6 via int(float(...)).
    # A decimal is not a valid integer guess and must be rejected.
    ok, value, err = parse_guess("6.9")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


def test_parse_guess_handles_whitespace():
    # Surrounding whitespace around a valid integer should still parse.
    ok, value, err = parse_guess("  42  ")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_guess_whitespace_only_is_empty():
    # A string that is only whitespace counts as no guess.
    ok, value, err = parse_guess("   ")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


def test_parse_guess_empty_input():
    # An empty string prompts the player to enter a guess.
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


def test_first_attempt_win_awards_90():
    # attempt_number is 1-based; a first-attempt win should award 90, not 80.
    assert update_score(0, "Win", 1) == 90


def test_later_win_points_decay():
    # Each attempt costs 10 points off the win value.
    assert update_score(0, "Win", 2) == 80


def test_win_points_floor_at_10():
    # Regression: late wins never award less than 10 points.
    assert update_score(0, "Win", 20) == 10


def test_too_high_always_penalizes():
    # Regression: "Too High" used to award +5 on even attempts. A wrong
    # guess must always cost 5, regardless of attempt parity.
    assert update_score(100, "Too High", 2) == 95
    assert update_score(100, "Too High", 3) == 95


def test_too_low_penalizes():
    assert update_score(100, "Too Low", 1) == 95
