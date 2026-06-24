# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Expand the game with four new features, keeping all game logic in pure,
unit-testable functions:

1. **Recent Guesses** — show the player's latest guesses for the current
   match, with a green ↑ / red ↓ hint arrow per guess when hints are on.
2. **Winning streak** — count consecutive wins, plus a best-streak record.
3. **Game timer** — a live timer that runs while playing and freezes when the
   game ends, with a speed bonus for fast wins.
4. **Match-history carousel** — a browsable card per finished game (result,
   score, attempts, secret, difficulty, time, streak) with prev/next arrows.

**What did the agent do?**

1. **`logic_utils.py`** — added pure functions with Google-style docstrings:
   - `time_bonus(elapsed_seconds)` — decaying speed bonus (50 → 0).
   - `format_duration(seconds)` — `"42s"` / `"1m 05s"` formatting.
   - `update_streak(current_streak, won)` — +1 on a win, reset to 0 on a loss.
2. **`app.py`** — wired the four features into the Streamlit UI:
   - **Recent Guesses** rendered from `st.session_state.history`, cleared on
     New Game / difficulty change, with per-guess direction arrows shown only
     when the hint checkbox is on (direction only — no distance revealed).
   - **Streak** + **Best Streak** metrics, updated on win/loss.
   - **Timer** via an `st.fragment(run_every=1)` that ticks live and freezes
     at the final time once the game is over.
   - **Carousel** driven by a `match_history` list and a `history_index`, with
     ⬅️/➡️ buttons that disable at the ends.
3. **`tests/test_game_logic.py`** — grew the suite to **32 tests** covering the
   pure logic (time-bonus tiers/boundaries, duration formatting, streak
   win/loss, scoring + penalties, difficulty multiplier, input validation).
4. Ran `pytest` (**32/32 passing**) and `flake8` (clean) to verify.

**What did you have to verify or fix manually?**

- Caught the **carousel rendering as a raw code block** — the agent's HTML card
  had blank lines + indentation, which Markdown treated as a code fence; fixed
  by making it a flush-left, gap-free HTML string.
- Caught the **carousel disappearing when paging after a win/loss** — an
  `st.stop()` on game-over halted the script before the carousel rendered;
  replaced it with a `game_over` flag that blocks new guesses but keeps the
  page alive.
- Made the **timer freeze** at game over (save the final time; only compute
  live elapsed while `status == "playing"`).
- Guarded the hint arrows so **non-numeric / invalid guesses** are skipped, and
  the carousel uses `.get()` fallbacks for older history entries.
- Decided arrows must be **direction-only**: `st.metric`'s delta would have
  leaked the exact distance (`guess + delta = secret`), spoiling the game.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

Tests live in `tests/test_game_logic.py` (32 tests, all passing). The table
below highlights the trickiest edge cases the AI suggested.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
| --- | --- | --- | --- | --- |
| Score must never go negative | "Add tests proving the wrong-guess penalty can't push the score below 0" | `test_score_never_goes_negative` — score 0, far-off guess (penalty 10) stays 0 | ✅ Yes | Confirms the `max(0, ...)` floor; without it the score would read −10. |
| Win reward has a floor | "What happens if the player wins on a very late attempt?" | `test_win_reward_floors_at_10` — attempt 20 → `100 − 10·19 = −90` clamps to 10 | ✅ Yes | Guards against negative win rewards on long games. |
| Hard deducts more | "Verify difficulty scales the penalty" | `test_hard_doubles_the_penalty` — same guess: Normal −10, Hard −20 | ✅ Yes | Pins the `PENALTY_MULTIPLIER` (Hard = 2×) contract. |
| Reject decimals | "Reject non-integer guesses like 3.5" | `test_parse_guess_rejects_decimals` / `_integer_looking_decimals` (`"10.0"`) | ✅ Yes | Even whole-valued decimals (`10.0`) are rejected — only true integers allowed. |
| Reject negatives & zero | "Guesses must be positive whole numbers" | `test_parse_guess_rejects_negative_numbers` / `_rejects_zero` | ✅ Yes | Smallest valid guess is 1; `-5` and `0` are invalid. |
| Empty / None input | "Handle blank or missing input safely" | `test_parse_guess_rejects_empty_and_none` (`""`, `"   "`, `None`) | ✅ Yes | No crash on empty/whitespace/None; returns a friendly error. |
| Timer boundary values | "Make sure the speed-bonus tiers are inclusive on the edges" | `test_time_bonus_boundaries_are_inclusive` — `time_bonus(10)==50`, `(20)==30` | ✅ Yes | Off-by-one on a `<=` boundary would silently drop a tier. |
| Duration formatting | "Format seconds; pad and clamp negatives" | `test_format_duration_over_a_minute_zero_pads_seconds` / `_truncates_floats_and_clamps_negatives` | ✅ Yes | `65 → "1m 05s"`, `12.9 → "12s"`, `-5 → "0s"`. |
| Streak resets on a loss | "Streak should reset when the player loses" | `test_update_streak_resets_on_loss` — `update_streak(7, False) == 0` | ✅ Yes | A loss breaks the consecutive-win streak. |
| Difficulty range never overflows | "Prove a generated secret stays inside the difficulty range" | `test_easy_secret_never_exceeds_its_max` — 1000 Easy secrets, max ≤ 20 | ✅ Yes | Regression test for the original out-of-range secret bug. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```text
logic_utils.py needs professional docstrings and the linter is reporting
issues. Run flake8, add Google-style docstrings to every function, and fix
the style warnings without changing the game logic.
```

**Linter:** `flake8 7.1.1` (pycodestyle 2.12.1, pyflakes 3.2.0), run as
`flake8 logic_utils.py --max-line-length=120`.

**Linting output before:**

```text
logic_utils.py:41:63: E703 statement ends with a semicolon
logic_utils.py:48:42: E703 statement ends with a semicolon
logic_utils.py:52:43: E703 statement ends with a semicolon
logic_utils.py:70:121: E501 line too long (140 > 120 characters)
logic_utils.py:73:121: E501 line too long (183 > 120 characters)
```

**Linting output after:**

```text
(no output — exit code 0)
```

**Changes applied:**

- **E703 (trailing semicolons):** removed the stray `;` from three debug
  `print()` statements in `check_guess` — a non-Pythonic habit carried over
  from C-style languages.
- **E501 (line too long):** wrapped two over-long `# TODO` comments in
  `update_score` across multiple lines.
- **Docstrings:** upgraded all four functions
  (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`)
  from one-line summaries to Google-style docstrings with `Args:` and
  `Returns:` sections.

**Verification:** re-ran `flake8` (clean, exit 0) and `pytest`
(6/6 passing) to confirm the cleanup did not change behavior.

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->
For Model A (Claude Opus 4.8), I asked:
- Suggest changes I can make to redesign the UI to make it better.
For Model B (ChatGPT running GPT-5.5):
- Adding 4 new features: Recent Guess of each match, Streak of winning, Timer of each round, and Carousel of match history. It also suggests me more features, but for a simple application, and not to make it more complicated (adding servers, ...), I chose 4 most suitable for my opinion for this.
- I also asked some same questions for both models, for some answer from a model that does not seem suitable for me. For example, redesigning the celebration animation (which is shown in the table below), ...

|                          | Model A | Model B |
|--------------------------|---------|---------|
| **Model name**           | Claude Opus 4.8 (1M context) | ChatGPT running GPT-5.5 |
| **Response summary**     |When you asked for a better win animation, I added a celebrate_win() helper that replaces the plain balloons-and-success-box with a custom HTML/CSS/JS celebration — a bouncing 🏆 trophy, a shimmering gold-to-red gradient headline personalized with the player's name, a stats line (secret, number of tries, final score), and a 120-piece falling-confetti burst with a pop-in animation — wired so st.balloons() fires first and the banner (rendered in a sandboxed st.components.html iframe) follows, while the old st.success message was dropped; I also flagged that it replayed on each rerun and offered a full-page confetti variant. | I redesigned the winning experience in GuessMaster by replacing the inline celebration with a dedicated champion dialog that automatically appears when the player wins. The dialog features a bouncing trophy, confetti animation, a branded "👑 GuessMaster Victory!" headline, and a bright gold "Congratulations, <Player Name>! 🎉" message. I removed the duplicate summary line and instead display the game statistics clearly below the animation, including the secret number, attempts taken, and score earned. Additionally, the most recent victory is saved so players can reopen the celebration later using a "🏆 Replay Last Victory" button, creating a more polished and game-like user experience. |
| **More Pythonic?**       | Same | Same |
| **Clearer explanation?** | When a player guesses the secret number correctly, the game now throws a proper celebration instead of just showing a plain "You won" message. I built this in a few layers. First, balloons float up the screen (Streamlit's built-in st.balloons()), and they fire only once per win. Then a custom-designed banner appears: a bouncing 🏆 trophy, a shimmering "👑 GuessMaster Victory!" headline in a gold gradient, and a personalized "Congratulations, [your name]!" message — all created with custom HTML, CSS animations, and a little JavaScript that drops ~120 colorful confetti pieces. Below the animation, the game shows a clean summary of that round: the secret number, how many attempts it took, and the final score. To make it feel polished, I put this celebration inside a pop-up dialog (a modal) that appears over the rest of the page, and I timed it so the celebration only shows after the game has locked the board — meaning the guess box is already emptied and disabled, so nothing looks half-finished behind the popup. I also made sure the celebration plays just once and doesn't accidentally repeat when the player clicks around (for example, while browsing match history). The result is that winning feels like a real "moment" — animated, personal, and clearly the end of that round. | I enhanced the GuessMaster winning experience by replacing the basic success message with a dedicated champion dialog that automatically appears when a player correctly guesses the secret number. The dialog includes an animated trophy, confetti effects, a custom "👑 GuessMaster Victory!" banner, and a congratulatory message personalized with the player's name. To avoid clutter, I removed the duplicate result summary and instead display the key game statistics—secret number, attempts taken, and final score—in a clean, easy-to-read format below the animation. I also added support for saving the player's most recent victory, allowing them to reopen and replay the celebration later through a "🏆 Replay Last Victory" button, making the game feel more interactive and polished. |

**Which did you prefer and why?** \
About the Logic, I prefer utilizing ChatGPT's reasoning models due to their superior performance in raw mathematical reasoning and isolated script optimization. \
Conversely, about the UI design, I rely on the Claude model because of its exceptional grasp of modern styling systems and design cohesion. Claude consistently generates cleaner, more responsive HTML that natively respect layout constraints right out of the box. \
However, since I did not have much experience working with different models, I would love to experience more to understand deeply on how and which fields each model work better
<!-- Your conclusion -->
