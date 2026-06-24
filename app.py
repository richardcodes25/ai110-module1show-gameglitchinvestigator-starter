import random
import time
import streamlit as st

from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
    time_bonus,
    format_duration,
    update_streak,
    streak_bonus,
    PENALTY_MULTIPLIER,
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
            # Start the game clock now -- the game begins once the name is in.
            st.session_state.start_time = time.time()
            st.rerun()
        else:
            st.warning("Please enter a name to continue.")


# Gate the whole app on having a name: until one is entered we only show the
# dialog and stop here, so the timer never starts counting during name entry.
if not st.session_state.player_name:
    ask_name()
    st.stop()



def celebrate_win(name: str, secret: int, score: int, attempts: int):
    """Render a custom confetti + animated trophy banner for a win."""
    import streamlit.components.v1 as components

    safe_name = name or "Investigator"
    components.html(
        f"""
        <div class="win-wrap">
          <div class="trophy">🏆</div>
          <div class="headline">👑 GuessMaster Victory!</div>

            <div style="
                font-size:24px;
                margin-top:12px;
                font-weight:800;
                background: linear-gradient(90deg,#FFD700,#FFB347,#FFD700);
                -webkit-background-clip:text;
                background-clip:text;
                color:transparent;
            ">
                Congratulations, {safe_name}! 🎉
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

def guess_feedback(message: str, show_hint: bool):
    """Animated banner for a wrong guess.

    The higher/lower direction (``message``) is only revealed when hints are
    enabled. With hints off the player only learns the guess was wrong.
    """
    import streamlit.components.v1 as components

    detail = message if show_hint else "Keep going — you'll crack it!"
    components.html(
        f"""
        <div class="fb-banner">
          <div class="fb-emoji">❌</div>
          <div class="fb-title">Not quite!</div>
          <div class="fb-detail">{detail}</div>
        </div>
        <style>
          .fb-banner {{
            font-family: system-ui, sans-serif;
            text-align: center;
            background: linear-gradient(135deg,#ff5858,#f857a6);
            color: white;
            padding: 16px;
            border-radius: 14px;
            animation: shake 0.5s ease;
          }}
          .fb-emoji {{ font-size: 42px; }}
          .fb-title {{ font-size: 24px; font-weight: 800; margin-top: 2px; }}
          .fb-detail {{ font-size: 17px; margin-top: 6px; opacity: 0.95; }}
          @keyframes shake {{
            0%,100% {{ transform: translateX(0); }}
            20% {{ transform: translateX(-10px); }}
            40% {{ transform: translateX(10px); }}
            60% {{ transform: translateX(-8px); }}
            80% {{ transform: translateX(8px); }}
          }}
        </style>
        """,
        height=150,
    )


@st.dialog("🏆 GuessMaster Champion")
def celebration_dialog(name, secret, attempts, score):

    celebrate_win(
        name=name,
        secret=secret,
        score=score,
        attempts=attempts,
    )

    st.markdown(
        f"""
        ### 🎉 Victory Statistics

        🎯 **Secret Number:** {secret}

        ⏱ **Attempts:** {attempts}

        🏆 **Score:** {score}
        """
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

# Let the player know Hard deducts more per wrong guess.
penalty_multiplier = PENALTY_MULTIPLIER.get(difficulty, 1)
if penalty_multiplier > 1:
    st.sidebar.caption(f"⚠️ {difficulty}: wrong guesses cost {penalty_multiplier}× points")

if "match_history" not in st.session_state:
    st.session_state.match_history = []

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    # TODO: This should probably start at 0, but let's see if the glitch is that it starts at 1 instead
    # st.session_state.attempts = 1
    st.session_state.attempts = 0

if "score" not in st.session_state:
    # Score accumulates from 0 and is revealed only when the game ends.
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

if "history_index" not in st.session_state:
    st.session_state.history_index = 0

if "last_win" not in st.session_state:
    st.session_state.last_win = None

# Timed mode: when the current game started, and the final time of the last
# finished game (frozen so the timer stops once the game is over).
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if "last_game_time" not in st.session_state:
    st.session_state.last_game_time = None

# A win defers its celebration to the run AFTER the winning guess (see the win
# handler). By now the guess box is already emptied and disabled, so the win is
# shown over a locked board. This is a one-shot flag, cleared once celebrated.
if st.session_state.get("celebrate_now"):
    st.session_state.celebrate_now = False
    win = st.session_state.last_win
    # Balloons fire exactly once here (one-shot flag). The confetti banner is
    # rendered by celebration_dialog below -- don't also call celebrate_win()
    # on the page, or the effect would play twice.
    st.balloons()
    st.success(
        f"⏱️ Solved in {format_duration(win['time'])} — "
        f"speed bonus +{win['bonus']}, streak bonus +{win.get('streak_bonus', 0)} "
        f"→ final score {win['score']}  🔥 Streak: {win['streak']}"
    )
    celebration_dialog(
        name=win["name"],
        secret=win["secret"],
        attempts=win["attempts"],
        score=win["score"],
    )

# Streak tracking: consecutive wins, plus the best streak this session.
if "streak" not in st.session_state:
    st.session_state.streak = 0

if "best_streak" not in st.session_state:
    st.session_state.best_streak = 0

@st.fragment(run_every=1)
def render_game_timer():
    """Live game timer.

    Counts the whole time from the start of the game and ticks up every second
    while the game is in progress; freezes at the final time once the game is
    over.
    """
    if st.session_state.status == "playing":
        seconds = time.time() - st.session_state.start_time
    else:
        seconds = st.session_state.last_game_time or 0
    st.metric("⏱️ Time", format_duration(seconds))


score_col, attempt_col, remain_col = st.columns(3)

with score_col:
    # Hide the running score during play -- show 0 until the game ends, then
    # reveal the final score for that match.
    display_score = st.session_state.score if st.session_state.status != "playing" else 0
    st.metric("🏆 Score", display_score)

with attempt_col:
    st.metric("🎯 Attempts", st.session_state.attempts)

with remain_col:
    st.metric(
        "⏳ Remaining",
        max(0, attempt_limit - st.session_state.attempts)
    )

time_col, streak_col, best_col = st.columns(3)

with time_col:
    render_game_timer()

with streak_col:
    st.metric("🔥 Streak", st.session_state.streak)

with best_col:
    st.metric("🏅 Best Streak", st.session_state.best_streak)

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
    st.session_state.start_time = time.time()
    st.session_state.last_game_time = None
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

# Once the game is over the guess box is emptied and disabled until the player
# starts a New Game. Deleting the stored value BEFORE the widget is created is
# what makes it render empty (you can't clear a widget after it's drawn).
is_playing = st.session_state.status == "playing"
guess_key = f"guess_input_{difficulty}"
if not is_playing and guess_key in st.session_state:
    del st.session_state[guess_key]

# FIXME: A plain text_input + st.button meant pressing Enter did nothing; you had to
# click Submit. Wrapping the input and submit button in st.form makes Enter submit too.
with st.container(border=True):

    with st.form(key=f"guess_form_{difficulty}"):

        raw_guess = st.text_input(
            "Enter your guess",
            placeholder=f"Pick a number from {low} to {high}",
            key=guess_key,
            disabled=not is_playing,
        )

        submit = st.form_submit_button(
            "🚀 Submit Guess",
            use_container_width=True,
            disabled=not is_playing,
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
    # Restart the game clock for timed mode.
    st.session_state.start_time = time.time()
    st.session_state.last_game_time = None
    # Clear the guess box so the new game starts with an empty input.
    guess_key = f"guess_input_{difficulty}"
    if guess_key in st.session_state:
        del st.session_state[guess_key]
    st.success("New game started.")
    st.rerun()

# Game-over notice. We DON'T st.stop() here -- stopping would skip everything
# below (Recent Guesses + the Match History carousel), so paging the carousel
# after a win/loss would wipe the page back to just this banner. Instead we
# only block processing of NEW guesses while keeping the rest of the page alive.
game_over = st.session_state.status != "playing"
if game_over:
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error(
            f"💀 Game over! The secret was {st.session_state.secret}. "
            f"Final score: {st.session_state.score}. "
            f"Click New Game to play again."
        )

if submit and not game_over:
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

        # FIXME: We pass the INTEGER secret (st.session_state.secret), not the local
        # `secret` above which becomes a string on even attempts -- abs(guess - secret)
        # would crash on a str. Also passes guess so scoring can use distance.
        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
            guess=guess_int,
            secret=st.session_state.secret,
            difficulty=difficulty,
        )

        if outcome == "Win":
            # Timed mode: freeze the clock and add a decaying speed bonus.
            game_time = time.time() - st.session_state.start_time
            st.session_state.last_game_time = game_time
            bonus = time_bonus(game_time)
            st.session_state.score += bonus

            # Streak: a win extends the streak and may set a new best, and the
            # longer the streak the bigger the streak bonus added to the score.
            st.session_state.streak = update_streak(st.session_state.streak, True)
            st.session_state.best_streak = max(
                st.session_state.best_streak,
                st.session_state.streak,
            )
            s_bonus = streak_bonus(st.session_state.streak)
            st.session_state.score += s_bonus

            st.session_state.status = "won"
            st.session_state.match_history.append({
                "result": "WIN",
                "difficulty": difficulty,
                "attempts": st.session_state.attempts,
                "secret": st.session_state.secret,
                "score": st.session_state.score,
                "time": game_time,
                "streak": st.session_state.streak,
            })
            # Show the newest game in the carousel.
            st.session_state.history_index = len(st.session_state.match_history) - 1
            st.session_state.last_win = {
                "name": st.session_state.player_name,
                "secret": st.session_state.secret,
                "attempts": st.session_state.attempts,
                "score": st.session_state.score,
                "time": game_time,
                "bonus": bonus,
                "streak_bonus": s_bonus,
                "streak": st.session_state.streak,
            }
            # Defer the celebration to the next run and rerun now, so the guess
            # box is already emptied and disabled by the time the win is shown.
            st.session_state.celebrate_now = True
            st.rerun()
        else:
            if st.session_state.attempts >= attempt_limit:
                # Timed mode: freeze the clock. Streak: a loss resets it to 0.
                game_time = time.time() - st.session_state.start_time
                st.session_state.last_game_time = game_time
                st.session_state.streak = update_streak(st.session_state.streak, False)

                st.session_state.status = "lost"
                # Record the FINAL game result only when the game actually ends.
                st.session_state.match_history.append({
                    "result": "LOSS",
                    "difficulty": difficulty,
                    "attempts": st.session_state.attempts,
                    "secret": st.session_state.secret,
                    "score": st.session_state.score,
                    "time": game_time,
                    "streak": st.session_state.streak,
                })
                # Show the newest game in the carousel.
                st.session_state.history_index = len(st.session_state.match_history) - 1
                # Rerun so the now-finished game empties and disables the guess
                # box. The game-over banner above shows the result details.
                st.rerun()
            else:
                # Game continues: show the wrong-answer feedback (direction only
                # when hints are on).
                guess_feedback(message, show_hint)

if st.session_state.history:

    st.divider()

    st.subheader("📜 Recent Guesses")

    history = list(reversed(st.session_state.history[-10:]))

    cols = st.columns(min(5, len(history)))

    secret_value = st.session_state.secret

    for idx, guess in enumerate(history):
        num = len(st.session_state.history) - idx

        # When hints are on, show a direction arrow for each numeric guess:
        # green ↑ if the secret is higher (guess too low), red ↓ if the secret
        # is lower (guess too high). Direction only -- no distance revealed.
        arrow = ""
        if show_hint and isinstance(guess, int) and guess != secret_value:
            if guess < secret_value:
                arrow = " <span style='color:#22c55e;'>↑</span>"
            else:
                arrow = " <span style='color:#ef4444;'>↓</span>"

        cols[idx % len(cols)].markdown(
            f"<div style='color:#888; font-size:0.8rem;'>#{num}</div>"
            f"<div style='font-size:1.7rem; font-weight:600;'>{guess}{arrow}</div>",
            unsafe_allow_html=True,
        )

st.divider()

st.subheader("📜 Match History")

if not st.session_state.match_history:

    st.markdown("""
    <div style="
        height:180px;
        border-radius:15px;
        border:2px dashed #ccc;
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:20px;
        color:gray;
        background:white;
    ">
        No History Played Yet
    </div>
    """, unsafe_allow_html=True)

else:
    current = st.session_state.match_history[
        st.session_state.history_index
    ]

    color = "#22c55e" if current["result"] == "WIN" else "#ef4444"
    # Older history entries (saved before timed/streak mode) may lack these keys.
    time_text = format_duration(current["time"]) if current.get("time") is not None else "—"
    streak_text = current.get("streak", "—")

    st.markdown(
        f"""
<div style="background:white; padding:25px; border-radius:16px; box-shadow:0 4px 12px rgba(0,0,0,.1); min-height:220px;">
<h2 style="color:{color}; margin:0;">{current["result"]}</h2>
<h3 style="color:#333;">Score: {current["score"]}</h3>
<hr>
<p style="color:#333;">🎯 Attempts: {current["attempts"]}</p>
<p style="color:#333;">🔢 Secret Number: {current["secret"]}</p>
<p style="color:#333;">⚙️ Difficulty: {current["difficulty"]}</p>
<p style="color:#333;">⏱️ Time: {time_text}</p>
<p style="color:#333;">🔥 Streak after game: {streak_text}</p>
</div>
""",
        unsafe_allow_html=True,
    )

    last_index = len(st.session_state.match_history) - 1
    at_start = st.session_state.history_index <= 0
    at_end = st.session_state.history_index >= last_index

    left, spacer, right = st.columns([1,5,1])

    with left:
        # Disable when already at the oldest game; re-enables once there's
        # an older game to move back to.
        if st.button("⬅️", disabled=at_start):
            st.session_state.history_index = max(
                0,
                st.session_state.history_index - 1
            )
            st.rerun()

    with right:
        # Disable when already at the newest game; re-enables once there's
        # a newer game to move forward to.
        if st.button("➡️", disabled=at_end):
            st.session_state.history_index = min(
                last_index,
                st.session_state.history_index + 1
            )
            st.rerun()
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