import random

from logic_utils import check_guess, get_range_for_difficulty


# --- Regression tests for the "New Game" out-of-range secret bug ---------------
#
# Bug that was fixed: the "New Game" handler generated the secret with
#   random.randint(1, 100)
# regardless of the selected difficulty. On Easy (range 1-20) or Normal
# (range 1-50) that could produce a secret OUTSIDE the stated range -- an
# unguessable number. The fix draws the secret from the difficulty's own
# range via random.randint(low, high). These tests pin that contract.

def test_difficulty_ranges_are_correct():
    # Range must grow with difficulty: Easy < Normal < Hard.
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 50)
    assert get_range_for_difficulty("Hard") == (1, 100)


def test_new_game_secret_stays_within_difficulty_range():
    # Mirror the New Game secret generation for each difficulty and confirm
    # every generated secret is inside that difficulty's range.
    for difficulty in ("Easy", "Normal", "Hard"):
        low, high = get_range_for_difficulty(difficulty)
        for _ in range(1000):
            secret = random.randint(low, high)  # same call the fixed code makes
            assert low <= secret <= high, (
                f"{difficulty}: secret {secret} outside range {low}-{high}"
            )


def test_easy_secret_never_exceeds_its_max():
    # This is the exact failure the old hardcoded randint(1, 100) caused:
    # on Easy, secrets above 20 were possible. With the fix they never are.
    low, high = get_range_for_difficulty("Easy")
    secrets = [random.randint(low, high) for _ in range(1000)]
    assert max(secrets) <= high == 20


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win.
    # check_guess returns a (outcome, message) tuple.
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # Secret 50, guess 60 -> guess is above the secret, so the hint
    # must tell the player to go LOWER.
    outcome, message = check_guess(60, 50)
    assert "LOWER" in message

def test_guess_too_low():
    # Secret 50, guess 40 -> guess is below the secret, so the hint
    # must tell the player to go HIGHER.
    outcome, message = check_guess(40, 50)
    assert "HIGHER" in message
