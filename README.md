- page 16


- when i finich a level the next level must created
- Complete Lost State code <<<<<<<<<<<<<
- the config file must support additional comments C/C++


# Rules:
• Your project must adhere to the flake8 coding standard.
• Your code must include type hints for function parameters, return types, and variables where applicable (using the typing module). Use mypy for static type checking. All functions must pass mypy without errors.
• Include docstrings in functions and classes following PEP 257 (e.g., Google or
NumPy style) to document purpose, parameters, and returns.


 Game progression
• The game consists of multiple levels (at least 10).
• Each level has a time limit (e.g., 90 seconds).
• If the time limit is reached, you can decide what happens (e.g., restart the level,
end the game, etc.).
• If the player completes a level, they move to the next level.
• The player keeps their score and remaining lives between levels.
• The game ends when all levels are completed or when the player loses all lives.
• During the game, the player can pause and resume the game.
• When the game ends (win or lose), the final score is displayed, and the player can
enter their name to save the highscore.
• After the game ends, the player is returned to the main menu.

### page 16

VI.8 User Interface

• Main Menu:
◦ ✅ Start Game - Allows the player to start a new game.
◦ ✅ View Highscores - Displays the Top 10 scores with player names.
◦ ❌ Instructions - Shows the game controls and rules.
◦ ❌ Exit - Closes the game application.

• In-Game HUD (always visible during gameplay):
◦ Current score
◦ Remaining lives
◦ ❌ Current level
◦ Remaining time for the level

• Pause Menu:
◦ Resume the game - Allows the player to return to the ongoing game.
◦ Return to the main menu - Allows the player to exit the current game and go
back to the main menu.

• Game Over Screen:
◦ Displays the final score.
◦ Prompts the player to enter their name to save the score in the highscores list.

• Victory Screen:
◦ Displays the final score and a congratulatory message.
◦ Prompts the player to enter their name to save the score in the highscores list.



# Questions :

1. How to upload a game to Itch.io

# Tasks:
1. A cheat mode for evaluation purposes
2. Deployment to a public gaming platform (Steam/Itch.io or similar) for demonstration.
3. When time end display lost screen
4. hande play again