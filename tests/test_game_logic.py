from logic_utils import check_guess

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
