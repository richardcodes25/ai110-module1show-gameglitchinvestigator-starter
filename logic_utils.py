def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    print(f"Checking guess: {guess} against secret: {secret}");

    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            print("You have to go LOWER");
            # return "Too High", "📈 Go HIGHER!"
            return "Too Low", "📉 Go LOWER!"
        else:
            print("You have to go HIGhER");
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


def update_score(current_score: int, outcome: str, attempt_number: int, guess: int, secret: int):
    """Update score based on outcome, attempt number, and distance from the secret."""
    if outcome == "Win":
        print(f"Calculating score for win on attempt {attempt_number} with guess {guess} and secret {secret}")
        # TODO: The scoring system is supposed to reward earlier wins more, but maybe the glitch is that it rewards later wins more instead?
        # points = 100 - 10 * (attempt_number + 1)
        points = 100 - 10 * (attempt_number - 1)
        # TODO: This is tolerance for player, but I think the glitch is that it is actually a penalty for the player instead, so maybe it should be a minimum score of 0 instead of 10?
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        print(f"Calculating score for {outcome} on attempt {attempt_number} with guess {guess} and secret {secret}")
        distance = abs(guess - secret)
        if distance <= 5:
            penalty = 1      # very close
        elif distance <= 15:
            penalty = 5     # getting warm
        else:
            penalty = 10     # way off
        print(f"Applying penalty of {penalty} for {outcome} on attempt {attempt_number}")
        # TODO: Score can not be negative, but maybe the glitch is that it can go negative instead?
        current_score = current_score - penalty
        print(f"New score after penalty: {current_score}")
        return current_score

    return current_score
