# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Expand the game with two new features: a **timed mode** (track how long each
game takes and award a speed bonus for fast wins) and **streak counting**
(track consecutive wins, plus a best-streak record for the session). The
agent was asked to keep all new game logic in pure, unit-testable functions.

**What did the agent do?**

1. **`logic_utils.py`** — added three pure functions with Google-style
   docstrings:
   - `time_bonus(elapsed_seconds)` — decaying speed bonus (50 → 0).
   - `format_duration(seconds)` — `"42s"` / `"1m 05s"` formatting.
   - `update_streak(current_streak, won)` — +1 on a win, reset to 0 on a loss.
2. **`app.py`** — wired the features into the Streamlit UI:
   - new session-state keys (`start_time`, `last_game_time`, `streak`,
     `best_streak`);
   - reset the game clock on New Game and on difficulty change;
   - a second metrics row (⏱️ Time / 🔥 Streak / 🏅 Best Streak);
   - applied the speed bonus and streak update on win/loss, and added
     `time` + `streak` to each match-history carousel card.
3. **`tests/test_game_logic.py`** — added 8 tests (tiers, boundaries,
   monotonic decay, float/negative handling, win/loss streak).
4. Ran `pytest` (14/14 passing) and `flake8` (clean) to verify.

**What did you have to verify or fix manually?**

- Confirmed the **timer freezes** at game over instead of ticking forever
  (handled by saving `last_game_time` and only computing live elapsed while
  `status == "playing"`).
- Confirmed **older match-history entries** (saved before this feature) don't
  crash the carousel — the agent used `.get()` with fallbacks for the new
  `time`/`streak` keys.
- Noted the on-screen timer only refreshes on interaction (each guess/rerun),
  not every second; a live-ticking version would need `st.fragment`.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| | | | | |
| | | | | |
| | | | | |

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

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
