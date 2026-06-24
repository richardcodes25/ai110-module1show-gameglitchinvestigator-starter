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
<img width="593" height="405" alt="Screenshot 2026-06-23 at 9 17 10 PM" src="https://github.com/user-attachments/assets/ce503848-9764-4e4d-9576-c75a7b64737c" />


3. <!-- Describe this step --> 
<img width="578" height="401" alt="Screenshot 2026-06-23 at 9 18 59 PM" src="https://github.com/user-attachments/assets/b4e0f86a-8a61-462c-b1a6-ce24c6e6ff24" />

4. <!-- Describe this step --> Score updates correctly after each guess
5. <!-- Add more steps as needed --> Game ends after the correct guess. User can click on New Game button to open a new game.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here --> \
<img width="602" height="362" alt="Screenshot 2026-06-23 at 9 19 27 PM" src="https://github.com/user-attachments/assets/294de005-b92a-4f9a-b7e9-a515a2580e14" />


## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```
<img width="1252" height="487" alt="Screenshot 2026-06-23 at 9 21 10 PM" src="https://github.com/user-attachments/assets/ce6258fa-c112-44ed-a3f3-d035276eef29" />


## 🚀 Stretch Features

- [x] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional] \
Below are new design of Game Glitches Investigator (new name: GuessMaster).
<img width="1468" height="702" alt="Screenshot 2026-06-23 at 9 21 48 PM" src="https://github.com/user-attachments/assets/49998846-d328-473d-80f4-721d220c0566" />

<img width="1470" height="761" alt="Screenshot 2026-06-23 at 9 22 08 PM" src="https://github.com/user-attachments/assets/27b0f855-a05f-483d-b064-281767ace690" />

Winning animation: \
<img width="449" height="427" alt="Screenshot 2026-06-23 at 9 38 26 PM" src="https://github.com/user-attachments/assets/f3ba2eb9-5df2-44b4-8571-a53d78088f91" />


- [x] New Feature 1: Recent Guess of each match \
Users can see the number they guessed, so that they can review and make a better decision on next attempt (No repeat guess). If user check the hints box, they will see arrow up and down, so that they can know whether secret number is lower or higher than the guess number.
<img width="498" height="121" alt="Screenshot 2026-06-23 at 9 23 47 PM" src="https://github.com/user-attachments/assets/d85c55f8-11b9-4fe1-91c9-7720abb99903" /> \

- [x] New Feature 2: Streak of winning \
Users can see their streak of winning, and they will get bonus point in the next round for how long streak they got. Image 2 below is the description of streak
<img width="648" height="153" alt="Screenshot 2026-06-23 at 9 30 41 PM" src="https://github.com/user-attachments/assets/0efddb10-7dcd-4cfb-aa9d-fdf45a8a1f20" />
<img width="346" height="95" alt="Screenshot 2026-06-23 at 9 33 09 PM" src="https://github.com/user-attachments/assets/196f84fd-2eae-4a3a-92ad-b87297716749" />

- [x] New Feature 3: Timer of each round \
Users got time counting for their match.
<img width="560" height="144" alt="Screenshot 2026-06-23 at 9 34 24 PM" src="https://github.com/user-attachments/assets/e96fc899-a1e0-404a-ba9b-2028bc5f3a9c" />

- [x] New feature 4: Carousel of match history \
User can click on left\right button to see history of matches of guessing. These include Score, How many attempts took, Secret number, Level of difficulty, Time usage, and Streak (if possible)
<img width="631" height="473" alt="Screenshot 2026-06-23 at 9 35 17 PM" src="https://github.com/user-attachments/assets/f5074c3f-bd3a-4673-b68c-bfa70ebcf1c1" />

