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
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
