def get_range_for_difficulty(difficulty: str):
    """Return the inclusive guessing range for a difficulty level.

    Args:
        difficulty: One of ``"Easy"``, ``"Normal"``, or ``"Hard"``. Any
            unrecognized value falls back to the widest range.

    Returns:
        tuple[int, int]: The ``(low, high)`` inclusive bounds for the secret
        number -- Easy ``(1, 20)``, Normal ``(1, 50)``, Hard ``(1, 100)``.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100


def parse_guess(raw: str):
    """Parse raw user input into a positive integer guess.

    Only whole positive numbers are accepted. Decimals (``"42.7"``),
    negatives, zero, and non-numeric text are all rejected with an
    explanatory message.

    Args:
        raw: The unvalidated text entered by the player.

    Returns:
        tuple[bool, int | None, str | None]: A ``(ok, guess, error_message)``
        triple. On success ``ok`` is True, ``guess`` is the parsed integer,
        and ``error_message`` is None. On failure ``ok`` is False, ``guess``
        is None, and ``error_message`` describes the problem.
    """
    if raw is None:
        return False, None, "Enter a guess."

    raw = raw.strip()
    if raw == "":
        return False, None, "Enter a guess."

    # Reject decimals -- only whole numbers are allowed (no "." or ",").
    if "." in raw or "," in raw:
        return False, None, "Whole numbers only — no decimals."

    try:
        value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    # Reject negatives and zero -- the smallest valid guess is 1.
    if value < 1:
        return False, None, "Enter a positive whole number (1 or more)."

    return True, value, None


def check_guess(guess, secret):
    """Compare a guess against the secret and return an outcome and hint.

    Args:
        guess: The player's guessed value.
        secret: The secret number to match against.

    Returns:
        tuple[str, str]: An ``(outcome, message)`` pair. ``outcome`` is one of
        ``"Win"``, ``"Too High"``, or ``"Too Low"``; ``message`` is a
        player-facing hint string.
    """
    print(f"Checking guess: {guess} against secret: {secret}")

    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            print("You have to go LOWER")
            # return "Too High", "📈 Go HIGHER!"
            return "Too Low", "📉 Go LOWER!"
        else:
            print("You have to go HIGhER")
            # return "Too Low", "📉 Go LOWER!"
            return "Too High", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            # return "Too High", "📈 Go HIGHER!"
            return "Too Low", "📉 Go LOWER!"
        # return "Too Low", "📉 Go LOWER!"
        return "Too High", "📈 Go HIGHER!"


# Wrong-guess penalties scale with difficulty: harder levels deduct more.
PENALTY_MULTIPLIER = {"Easy": 1, "Normal": 1, "Hard": 2}


def update_score(current_score: int, outcome: str, attempt_number: int,
                 guess: int, secret: int, difficulty: str = "Normal"):
    """Compute the new running score after a guess.

    Scoring accumulates from 0. A win awards points that decay with each
    attempt (``100 - 10 * (attempt - 1)``, floored at 10) -- so every extra
    attempt deducts from the win reward. Wrong guesses subtract a
    distance-based penalty (the closer the guess, the smaller the penalty),
    scaled by difficulty (see :data:`PENALTY_MULTIPLIER` -- Hard deducts
    double), never dropping below 0.

    Args:
        current_score: The score before this guess is applied.
        outcome: The result from :func:`check_guess` -- ``"Win"``,
            ``"Too High"``, or ``"Too Low"``.
        attempt_number: The 1-based index of the current attempt.
        guess: The player's numeric guess.
        secret: The secret number.
        difficulty: ``"Easy"``, ``"Normal"``, or ``"Hard"``. Controls the
            penalty multiplier for wrong guesses.

    Returns:
        int: The updated score (never negative).
    """
    if outcome == "Win":
        # Win reward decays by 10 per attempt taken, with a floor of 10.
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        distance = abs(guess - secret)
        if distance <= 5:
            penalty = 1      # very close
        elif distance <= 15:
            penalty = 5     # getting warm
        else:
            penalty = 10     # way off
        # Harder difficulties deduct more per wrong guess.
        penalty *= PENALTY_MULTIPLIER.get(difficulty, 1)
        # The score must never drop below 0, so floor it at zero.
        return max(0, current_score - penalty)

    return current_score


def time_bonus(elapsed_seconds: float) -> int:
    """Return a speed bonus that decays the longer a win takes.

    Used by *timed mode* to reward fast wins. The bonus is awarded once, on a
    win, and added on top of the normal attempt-based score.

    Args:
        elapsed_seconds: Wall-clock seconds between the start of the game and
            the winning guess.

    Returns:
        int: Bonus points -- 50 for a win within 10s, tapering to 0 after 60s.
    """
    if elapsed_seconds <= 10:
        return 50
    if elapsed_seconds <= 20:
        return 30
    if elapsed_seconds <= 40:
        return 15
    if elapsed_seconds <= 60:
        return 5
    return 0


def format_duration(seconds) -> str:
    """Format a duration in seconds as a compact human-readable string.

    Args:
        seconds: A non-negative duration. Floats are truncated to whole
            seconds.

    Returns:
        str: ``"42s"`` for under a minute, otherwise ``"1m 05s"`` style.
    """
    seconds = max(0, int(seconds))
    if seconds < 60:
        return f"{seconds}s"
    minutes, secs = divmod(seconds, 60)
    return f"{minutes}m {secs:02d}s"


def update_streak(current_streak: int, won: bool) -> int:
    """Return the new consecutive-win streak after a finished game.

    Args:
        current_streak: The streak before this game ended.
        won: True if the player won this game, False if they lost.

    Returns:
        int: ``current_streak + 1`` on a win, otherwise ``0``.
    """
    return current_streak + 1 if won else 0
