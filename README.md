# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [X] Describe the game's purpose.
- [X] Detail which bugs you found.
- [X] Explain what fixes you applied.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step --> User selected Normal level (range: [1, 50]) (Secret number: 31)
2. <!-- Describe this step --> 
<img width="583" height="243" alt="Screenshot 2026-06-23 at 5 32 29 AM" src="https://github.com/user-attachments/assets/9f9d38ee-562b-4442-8858-2a25bb2c20b7" />

3. <!-- Describe this step --> 
<img width="587" height="248" alt="Screenshot 2026-06-23 at 5 34 55 AM" src="https://github.com/user-attachments/assets/6b261af7-548e-4406-b1bc-8cf4c589fb6f" />

4. <!-- Describe this step --> Game returned Toow
<img width="588" height="313" alt="Screenshot 2026-06-23 at 5 35 47 AM" src="https://github.com/user-attachments/assets/9cf03edb-a6d7-462c-b583-c5c8d992f24f" />

5. <!-- Describe this step --> Score updates correctly after each guess
6. <!-- Add more steps as needed --> Game ends after the correct guess. User can click on New Game button to open a new game.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->
<img width="580" height="301" alt="Screenshot 2026-06-23 at 5 36 49 AM" src="https://github.com/user-attachments/assets/aea77fcf-075e-42e8-a194-00ec1b9cda91" />


## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```
<img width="1194" height="170" alt="Screenshot 2026-06-22 at 3 45 21 PM" src="https://github.com/user-attachments/assets/ccfa5c3b-c59f-49b8-937f-4fc04d4f27a0" />

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
