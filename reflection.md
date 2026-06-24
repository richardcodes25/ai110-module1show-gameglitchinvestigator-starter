# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| 10    |   "Go HIGHER!"    |   "Go LOWER"    |Checking guess: 10 against secret: 50|
| 50    |   "Go LOWER"      |   "Go HIGHER"   |Checking guess: 50 against secret: 23|
| Click on "New Game" button| Restart game | Not resetting game state (stuck with previous game final state) | None |
| After finish 1 game | Saving point after each game | Not saving point so far | Unless restart server, points will be keep track through matches |
| Too High/Low condition for deducting point | Point taking away for each too high/low guess should not depend on odd/even number inputted | Point subtracting for each too high/low guess is currently depended on odd/even number inputted | |
| Point calculating after attempt | If user guess exactly right on 1 attempt, they should not be deduct any point | User already be deduct 10 point from the first attempt | calculation should be 100 - 10*(attempt-1)|
| Final point | Final point should not be negative | e.g: -35 | |
| Difficulty | Range of Easy < Medium < Hard | Range of Easy < Hard < Normal | Normal is currently the hardest with the widest range, so we should swap it with Hard Level |
| Random function for new game | Get the range based on current difficulty level | Hard code from 1-100 (not true for Easy and Medium level) ||
| string-conversion hint bug | Everytime passing a number into check_guess function, secret is always an int. | in line ~199-202, on even-numbered attems, the secret number is converted into string before passed into check_guess. On odd, it stayed interger. | There is no reason for doing this, from my opinion|

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
=> Claude, ChatGPT
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
=> In the check_guess, Claude AI suggested me to swap 2 message that is correct but was put in wrong condition.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
=> Logic error: Claude AI suggest me to put in Easy - 20, Medium - 100, Hard - 50. This was more of misleading than a mistake, since it was intentionally put in the original code, which leads to the error of Claude AI here.
=> Coding error: ChatGPT provided a block of code to display history of matches, but it displayed as raw HTML code intead.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
=> I put in a print line to log out the guess versus the secret number with behavior
- Describe at least one test you ran (manual or using pytest) 
  
  and what it showed you about your code.
=> I ran `pytest` on `tests/test_game_logic.py`. The test `test_score_never_goes_negative` checks that a wrong guess cannot push the score below 0; it failed before I added the `max(0, ...)` floor in `update_score`, then passed after the fix. Another test, `test_easy_secret_never_exceeds_its_max`, generates 1000 Easy secrets and asserts none go above 20, which confirmed the difficulty-range fix. By the end the suite grew to 35 tests, all passing, so I was confident the fixes worked together and didn't break each other.
- Did AI help you design or understand any tests? How?
=> Yes. AI suggested edge cases I had not thought of, such as rejecting whole-looking decimals like "10.0", checking the time-bonus tiers exactly on their boundaries (10s, 20s), and clamping negative or float durations in the timer. It also explained why each case mattered, which helped me understand the expected contract of each function instead of just copying tests blindly.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
=> Streamlit re-runs the entire script from top to bottom every single time you interact with the app — clicking a button, typing a guess, or changing the difficulty. Because of that, any normal Python variable is recreated from scratch on each run, so the app "forgets" everything between interactions. `st.session_state` is a special dictionary that survives those reruns — it is basically the app's memory. Many of the original bugs (the secret number changing on every submit, the score resetting, New Game not working) came from values that were not stored in session state, or were being reset in the wrong place.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
=> Moving the core logic into a separate, pure module (`logic_utils.py`) and writing pytest tests for it. Keeping the logic out of the UI made each function easy to test in isolation, and the tests caught regressions whenever I changed the scoring, validation, or difficulty rules.
- What is one thing you would do differently next time you work with AI on a coding task?
=> I would verify AI-generated code more carefully before trusting it, especially UI code — I'd run it right away and read it line by line. In this project ChatGPT once gave me a block that rendered as raw HTML, and Claude suggested difficulty ranges that were actually wrong, so giving the AI clearer context up front and checking its output would have saved time.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
=> I now treat AI-generated code as a fast first draft, not a finished answer. It is usually right in structure but can hide subtle logic bugs, so I always test and review it myself before relying on it.
