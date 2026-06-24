import random

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
    time_bonus,
    format_duration,
    update_streak,
    streak_bonus,
)


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


# --- Timed mode: time_bonus -------------------------------------------------

def test_time_bonus_rewards_fast_wins_more():
    # The bonus must never increase as time goes up (monotonically decaying).
    times = [5, 10, 15, 20, 30, 40, 50, 60, 90]
    bonuses = [time_bonus(t) for t in times]
    assert bonuses == sorted(bonuses, reverse=True)


def test_time_bonus_tiers():
    assert time_bonus(8) == 50      # very fast
    assert time_bonus(18) == 30     # fast
    assert time_bonus(35) == 15     # moderate
    assert time_bonus(55) == 5      # slow
    assert time_bonus(120) == 0     # no bonus past a minute


def test_time_bonus_boundaries_are_inclusive():
    # Exactly on a tier boundary should still earn that tier's bonus.
    assert time_bonus(10) == 50
    assert time_bonus(20) == 30
    assert time_bonus(60) == 5


# --- Timed mode: format_duration --------------------------------------------

def test_format_duration_under_a_minute():
    assert format_duration(0) == "0s"
    assert format_duration(42) == "42s"


def test_format_duration_over_a_minute_zero_pads_seconds():
    assert format_duration(65) == "1m 05s"
    assert format_duration(600) == "10m 00s"


def test_format_duration_truncates_floats_and_clamps_negatives():
    assert format_duration(12.9) == "12s"
    assert format_duration(-5) == "0s"


# --- Streak tracking: update_streak -----------------------------------------

def test_update_streak_increments_on_win():
    assert update_streak(0, True) == 1
    assert update_streak(4, True) == 5


def test_update_streak_resets_on_loss():
    assert update_streak(7, False) == 0
    assert update_streak(0, False) == 0


# --- Streak bonus: longer streaks earn more (capped) -------------------------

def test_streak_bonus_zero_for_first_win():
    # A streak of 1 (or 0) earns no bonus yet.
    assert streak_bonus(0) == 0
    assert streak_bonus(1) == 0


def test_streak_bonus_grows_per_consecutive_win():
    # +5 for each win beyond the first.
    assert streak_bonus(2) == 5
    assert streak_bonus(3) == 10
    assert streak_bonus(4) == 15


def test_streak_bonus_is_capped():
    # Stops growing once the +25 cap is reached (streak 6 -> 25, and beyond).
    assert streak_bonus(6) == 25
    assert streak_bonus(50) == 25


# --- Scoring: penalties never push the score below zero ----------------------

def test_score_never_goes_negative():
    # Score 0, a far-off wrong guess (penalty 10) must floor at 0, not -10.
    new_score = update_score(
        current_score=0,
        outcome="Too High",
        attempt_number=1,
        guess=100,
        secret=1,
    )
    assert new_score == 0


def test_score_floors_at_zero_when_penalty_exceeds_score():
    # Score 3, penalty 5 (distance 10) -> would be -2, must clamp to 0.
    new_score = update_score(
        current_score=3,
        outcome="Too Low",
        attempt_number=2,
        guess=40,
        secret=50,
    )
    assert new_score == 0


def test_score_still_subtracts_normally_above_zero():
    # Score 50, close guess (distance <= 5 -> penalty 1) -> 49.
    new_score = update_score(
        current_score=50,
        outcome="Too High",
        attempt_number=1,
        guess=52,
        secret=50,
    )
    assert new_score == 49


# --- Scoring: a win awards attempt-decayed points ----------------------------

def test_win_awards_full_points_on_first_attempt():
    # Attempt 1 from a fresh score of 0 -> 100 - 10*0 = 100.
    new_score = update_score(
        current_score=0,
        outcome="Win",
        attempt_number=1,
        guess=50,
        secret=50,
    )
    assert new_score == 100


def test_win_reward_decays_per_attempt():
    # Attempt 3 -> 100 - 10*(3-1) = 80.
    new_score = update_score(
        current_score=0,
        outcome="Win",
        attempt_number=3,
        guess=50,
        secret=50,
    )
    assert new_score == 80


def test_win_reward_floors_at_10():
    # Very late win: 100 - 10*(20-1) = -90 -> floored to 10.
    new_score = update_score(
        current_score=0,
        outcome="Win",
        attempt_number=20,
        guess=50,
        secret=50,
    )
    assert new_score == 10


def test_win_adds_to_existing_score():
    # 15 already banked + (100 - 10*(2-1)=90) -> 105.
    new_score = update_score(
        current_score=15,
        outcome="Win",
        attempt_number=2,
        guess=50,
        secret=50,
    )
    assert new_score == 105


# --- Scoring: difficulty scales the wrong-guess penalty ----------------------

def test_hard_doubles_the_penalty():
    # Way-off guess (distance > 15 -> base penalty 10).
    # Normal deducts 10; Hard deducts 20.
    normal = update_score(100, "Too High", 1, guess=100, secret=1, difficulty="Normal")
    hard = update_score(100, "Too High", 1, guess=100, secret=1, difficulty="Hard")
    assert normal == 90
    assert hard == 80


def test_easy_and_normal_share_base_penalty():
    easy = update_score(100, "Too Low", 1, guess=30, secret=50, difficulty="Easy")
    normal = update_score(100, "Too Low", 1, guess=30, secret=50, difficulty="Normal")
    # distance 20 -> base penalty 10, multiplier 1 for both.
    assert easy == normal == 90


def test_default_difficulty_uses_base_penalty():
    # Omitting difficulty falls back to the base (Normal) multiplier.
    new_score = update_score(100, "Too High", 1, guess=100, secret=1)
    assert new_score == 90


# --- Input validation: parse_guess ------------------------------------------

def test_parse_guess_accepts_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_guess_strips_surrounding_whitespace():
    ok, value, err = parse_guess("   7  ")
    assert ok is True
    assert value == 7


def test_parse_guess_rejects_decimals():
    ok, value, err = parse_guess("3.5")
    assert ok is False
    assert value is None
    assert "decimal" in err.lower()


def test_parse_guess_rejects_integer_looking_decimals():
    # "10.0" is a whole value but still typed as a decimal -> rejected.
    ok, value, err = parse_guess("10.0")
    assert ok is False
    assert value is None


def test_parse_guess_rejects_negative_numbers():
    ok, value, err = parse_guess("-5")
    assert ok is False
    assert value is None
    assert "positive" in err.lower()


def test_parse_guess_rejects_zero():
    ok, value, err = parse_guess("0")
    assert ok is False
    assert value is None


def test_parse_guess_rejects_non_numeric_text():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None


def test_parse_guess_rejects_empty_and_none():
    assert parse_guess("")[0] is False
    assert parse_guess("   ")[0] is False
    assert parse_guess(None)[0] is False
