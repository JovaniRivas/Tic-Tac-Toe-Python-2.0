# Tic Tac Toe Python 2.0
This is a small personal project designed to gain further experience/exposure to Python. This is a simple tic-tac-toe game with various options presented to the user. 

## main.py
This contains the core structure of the game. The game starts, ends, and restarts here. All logic of the game itself is contained here. 

The following classes are defined in this file:
 - Player: 
    - Represents a real human player
    - Has the ability to make moves via input from the serial terminal
 - CPU: 
    - Represents the computer playing the game
    - This is an extension of the Player class 
    - Has the ability to make moves using logic defined in *CPUEngine.py* based on the difficulty attribute
 - Board: 
    - Representation of the tic-tac-toe board as a 2D list
    - Has the ability to print the current state of the board (with or without data)
    - Has the ability to check whether a given player has won the game
 - Game_UI: 
    - Contains a majority of the UI options presented to the user (via serial terminal)
 - Configuration: 
    - Determines the structure of the game based on user input
        - Game mode (easy/medium/hard), board size, and CPU difficulty 

The following functions are defined in this file:
 - game_configuration:
    - Builds the game based on user input (creates a configuration class)
    - Initiates the game after configuration is complete
 - game:
    - Begins the game and continues it until a win or draw is reached
    - Once a conclusion has been made, it will redirect to game_configuration to prompt user for new game setup


## miscFunctions.py
This file contains some miscellaneous helper functions to support the game. 

The following functions are defined in this file:
 - print_dash:
    - Just prints a series of dashes to form a line on the screen
    - Used aesthetically for the serial terminal UI
 - print_blank_lines:
    - Just prints a couple blank lines on the screen
    - Used aesthetically for the serial terminal UI
 - get_algebraic_input:
    - This is used to obtain a move to make from a human player
    - Converts algebraic input (a3) to a coordinate (1, 1)
        - Coordinate format is required for program to perform that move (2D list mapping)
 - num_to_algebraic:
    - This is used to convert the move made by a CPU from coordinate (1,1) to algebraic notation (a3)
    - This is required for the program to print the move performed by the CPU on the serial terminal during play
    - Aesthetics for game play visibility


## CPUEngine.py
This file contains the logic/calculations for the CPU players to make moves. Below is a description of the basic intent for each difficulty "engine". Adjustments should be made here if you feel that a particular CPU type (easy/medium/hard) is too easy/difficult for it's assigned difficulty level.It is important to note that in order for an engine to check for wins/blocks/etc., it must actually make the move, check for state, and undo the move. 

The following functions are defined in this file:
 - easy_CPU_engine:
    - Returns a random coordinate that is available on the board
 - medium_CPU_engine:
    - Blocks opponents if they set up a winning 
    - Attempts to win but takes the longest path to get there
    - Note: This engine will not look for an immediate win. This part of the code is commented out and is left to your discretion to keep/modify. Reason for this is that I felt it was a bit too similar to 'Hard' difficulty with it enabled. 
 - hard_CPU_engine:
    - Checks for immediate winning moves
    - Blocks opponents if they set up a winning move
    - If no wins or blocks, picks the ideal move that will get it to a win (*min_moves_to_win*)

The following functions are defined in this file but are only there to support the functions above:
 - determine_available_moves:
    - Helper function for all of the engines. This will return a list of all the available (empty) coordinates
 - min_moves_to_win:
    - Helper function for *hard_CPU_engine*
    - Returns the coordinate that will result in the fastest win in any direction (row, col, diagonal)
 - max_moves_to_win:
    - Helper function for *medium_CPU_engine*
    - Returns the coordinate that will result in the slowest win in any direction (row, col, diagonal)
 - calculate_moves_to_win
    - Helper function for *min_moves_to_win* and *max_moves_to_win*
    - Assigned the number of moves required for a given player to win to each available coordinate
    - Because one coordinate can span different moves for a win (based on direction), multiple dictionaries are required to map the number of moves to each coordinate


