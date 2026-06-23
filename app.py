import random
import streamlit as st

from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)

st.set_page_config(
    page_title="GuessMaster",
    page_icon="🎯",
    layout="centered",
)

st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
}

.stButton button {
    border-radius: 12px;
    font-weight: 600;
}

.stMetric {
    border-radius: 12px;
}

.guessmaster-title {
    text-align: center;
    padding: 10px 0 20px 0;
}

.guessmaster-title h1 {
    font-size: 4rem;
    margin-bottom: 0;
}

.guessmaster-title p {
    font-size: 1.2rem;
    color: #888;
}

.hero-card {
    padding: 20px;
    border-radius: 16px;
    background: linear-gradient(135deg, #4F46E5, #7C3AED);
    color: white;
    text-align: center;
    margin-bottom: 20px;
}

.hero-card h2 {
    margin: 0;
}

.hero-card p {
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# Ask the player for their name the first time they open the app.
if "player_name" not in st.session_state:
    st.session_state.player_name = ""


@st.dialog("🎯 Welcome to GuessMaster!")
def ask_name():
    st.write(
        "The ultimate number guessing challenge starts now.\n\n"
        "What should we call you?"
    )
    name = st.text_input("Your name", key="name_dialog_input")
    if st.button("Let's go 🚀"):
        if name.strip():
            st.session_state.player_name = name.strip()
            st.rerun()
        else:
            st.warning("Please enter a name to continue.")


if not st.session_state.player_name:
    ask_name()


def celebrate_win(name: str, secret: int, score: int, attempts: int):
    """Render a custom confetti + animated trophy banner for a win."""
    import streamlit.components.v1 as components

    safe_name = name or "Investigator"
    components.html(
        f"""
        <div class="win-wrap">
          <div class="trophy">🏆</div>
          <div class="headline">👑 GuessMaster Victory!</div>

        <div style="font-size:20px; margin-top:10px;">
            Congratulations, {safe_name}!
        </div>
          <div class="stats">
            Secret was <b>{secret}</b> &nbsp;•&nbsp;
            Solved in <b>{attempts}</b> {"try" if attempts == 1 else "tries"} &nbsp;•&nbsp;
            Score <b>{score}</b>
          </div>
        </div>
        <div id="confetti"></div>
        <style>
          .win-wrap {{
            text-align: center;
            font-family: system-ui, sans-serif;
            animation: pop 0.6s cubic-bezier(.18,.89,.32,1.28);
          }}
          .trophy {{
            font-size: 64px;
            animation: bounce 1s ease infinite;
          }}
          .headline {{
            font-size: 26px;
            font-weight: 800;
            margin-top: 4px;
            background: linear-gradient(90deg,#f9d423,#ff4e50,#f9d423);
            background-size: 200% auto;
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            animation: shine 2s linear infinite;
          }}
          .stats {{ font-size: 15px; color: #444; margin-top: 6px; }}
          @keyframes pop {{ from {{ transform: scale(0); opacity: 0; }} to {{ transform: scale(1); opacity: 1; }} }}
          @keyframes bounce {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-14px); }} }}
          @keyframes shine {{ to {{ background-position: 200% center; }} }}
          .confetti-piece {{
            position: fixed; top: -10px; width: 10px; height: 14px;
            opacity: 0.9; animation: fall linear forwards;
          }}
          @keyframes fall {{
            to {{ transform: translateY(105vh) rotate(720deg); opacity: 0.7; }}
          }}
        </style>
        <script>
          const colors = ["#f9d423","#ff4e50","#1fddff","#a3ff5b","#ff6ec7","#7c4dff"];
          const root = document.getElementById("confetti");
          for (let i = 0; i < 120; i++) {{
            const p = document.createElement("div");
            p.className = "confetti-piece";
            p.style.left = Math.random() * 100 + "vw";
            p.style.background = colors[i % colors.length];
            p.style.animationDuration = (2 + Math.random() * 2) + "s";
            p.style.animationDelay = (Math.random() * 0.8) + "s";
            root.appendChild(p);
          }}
        </script>
        """,
        height=220,
    )

st.markdown(
    """
    <div class="guessmaster-title">
        <h1>🎯 GuessMaster</h1>
        <p>Think. Guess. Conquer.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Greet the player by name in the header once they've introduced themselves.
if st.session_state.player_name:
    st.markdown(
        f"""
        <div class="hero-card">
            <h2>Welcome, {st.session_state.player_name}! 🎮</h2>
            <p>Can you become the next GuessMaster?</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.sidebar.title("🎯 GuessMaster")
st.sidebar.markdown("### Game Settings")

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

st.sidebar.metric("Range", f"{low} - {high}")
st.sidebar.metric("Max Attempts", attempt_limit)

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

score_col, attempt_col, remain_col = st.columns(3)

with score_col:
    st.metric("🏆 Score", st.session_state.score)

with attempt_col:
    st.metric("🎯 Attempts", st.session_state.attempts)

with remain_col:
    st.metric(
        "⏳ Remaining",
        max(0, attempt_limit - st.session_state.attempts)
    )

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

st.markdown("## 🔢 Make Your Guess")

# FIXME: This prompt used to hardcode "between 1 and 100", which contradicted the
# actual range on Easy/Normal. Now it uses the real {low}/{high} for the difficulty.
st.info(
    f"""
🎯 **Mission**

Guess the secret number between **{low}** and **{high}**

Attempts Remaining: **{attempt_limit - st.session_state.attempts}**
"""
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

# FIXME: A plain text_input + st.button meant pressing Enter did nothing; you had to
# click Submit. Wrapping the input and submit button in st.form makes Enter submit too.
with st.container(border=True):

    with st.form(key=f"guess_form_{difficulty}"):

        raw_guess = st.text_input(
            "Enter your guess",
            placeholder=f"Pick a number from {low} to {high}",
            key=f"guess_input_{difficulty}",
        )

        submit = st.form_submit_button(
            "🚀 Submit Guess",
            use_container_width=True,
        )

col2, col3 = st.columns([2, 1])
with col2:
    new_game = st.button(
        "🔄 New Game",
        use_container_width=True
    )
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
    # Clear the guess box so the new game starts with an empty input.
    guess_key = f"guess_input_{difficulty}"
    if guess_key in st.session_state:
        del st.session_state[guess_key]
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
            celebrate_win(
                name=st.session_state.player_name,
                secret=st.session_state.secret,
                score=st.session_state.score,
                attempts=st.session_state.attempts,
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )
if st.session_state.history:

    st.divider()

    st.subheader("📜 Recent Guesses")

    history = list(reversed(st.session_state.history[-10:]))

    cols = st.columns(min(5, len(history)))

    for idx, guess in enumerate(history):
        cols[idx % len(cols)].metric(
            f"#{len(st.session_state.history) - idx}",
            guess,
        )

# Footer
st.divider()

st.markdown(
    """
    <div style="text-align:center; padding:20px 0;">
        <h4 style="margin-bottom:5px;">🎯 GuessMaster</h4>
        <p style="margin:0; color:gray;">
            Think. Guess. Conquer.
        </p>
        <br>
        <small style="color:gray;">
            © 2026 Thanh Nguyen Do. All Rights Reserved.
        </small>
    </div>
    """,
    unsafe_allow_html=True,
)