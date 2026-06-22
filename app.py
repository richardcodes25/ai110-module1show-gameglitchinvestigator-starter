import random
import streamlit as st

# FIXME: Swap difificulty ranges to make the game harder on Easy and easier on Hard => Swap Hard with Normal
def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100


def parse_guess(raw: str):
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

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    # TODO: This should probably start at 0, but let's see if the glitch is that it starts at 1 instead
    # st.session_state.attempts = 1
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

# FIXME: Changing difficulty used to update the range caption but keep the OLD secret
# (the secret was only generated once). Now we detect the change and start a fresh
# game with a new secret drawn from the new range.
if difficulty != st.session_state.difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.rerun()

st.subheader("Make a guess")

# FIXME: This prompt used to hardcode "between 1 and 100", which contradicted the
# actual range on Easy/Normal. Now it uses the real {low}/{high} for the difficulty.
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

# FIXME: A plain text_input + st.button meant pressing Enter did nothing; you had to
# click Submit. Wrapping the input and submit button in st.form makes Enter submit too.
with st.form(key=f"guess_form_{difficulty}"):
    raw_guess = st.text_input(
        "Enter your guess:",
        key=f"guess_input_{difficulty}"
    )
    submit = st.form_submit_button("Submit Guess 🚀")

col2, col3 = st.columns(2)
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# FIXME: New Game used to reset attempts/secret but NOT status, so after a win/loss the
# status stayed "won"/"lost" and the guard below ran st.stop(), disabling Submit. We now
# reset status/score/history too, and draw the secret from the difficulty's range.
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.score = 0
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        # FIXME: The "glitch" was that the secret would alternate between being an int and a str on each attempt, which would cause the hint logic to break with a TypeError every other attempt. We now always keep it as an int, and the hint logic can handle it without crashing.
        # if st.session_state.attempts % 2 == 0:
        #     secret = str(st.session_state.secret)
        # else:
        #     secret = st.session_state.secret
        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            st.warning(message)

        # FIXME: We pass the INTEGER secret (st.session_state.secret), not the local
        # `secret` above which becomes a string on even attempts -- abs(guess - secret)
        # would crash on a str. Also passes guess so scoring can use distance.
        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
            guess=guess_int,
            secret=st.session_state.secret,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
