import miscFunctions
import math
import random

class Player:
    def __init__(self, name):
        self.name = name

    def make_move(self, board_matrix):#, board
        print(f"Player {self.name}'s turn.")
        print("Make a move using algebraic notation")
        miscFunctions.print_dash()
        while True:
            col, row = miscFunctions.get_algebraic_input(len(board_matrix))
            if (board_matrix[row - 1][col - 1] == ' '):
                board_matrix[row - 1][col - 1] = self.name
                break
            else:
                print("There is already a value at this position, please try again.")
        miscFunctions.print_dash()

class CPU(Player):
    def __init__(self, name, difficulty_level):
        super().__init__(name)
        self.difficulty_level = difficulty_level

    def make_move(self, board_matrix_array):#, board
        print(f"{self.__class__.__name__} {self.name}'s turn.")
        #Random Algorithm: Randomly pick from empty spots on the board
        row = len(board_matrix_array)
        col = len(board_matrix_array)
        availableCell = []
        for i in range(row):
            for j in range(col):
                if (board_matrix_array[i][j] == ' '):
                    availableCell.append([i, j])
        selected_coordinate = random.choice(availableCell)
        selected_row, selected_col = selected_coordinate
        board_matrix_array[selected_row][selected_col] = self.name
    

class Board:
    def __init__(self, size, board_matrix):
        self.size = size
        length = int(math.sqrt(size))
        self.board_matrix = [[' '] * length for x in range(length)]
        
    
    def print_board(self):
        miscFunctions.print_blank_lines()
        row = int(math.sqrt(self.size)) - 1
        col = int(math.sqrt(self.size)) - 1
        algebraic_cols = ['a', 'b', 'c', 'd', 'e'] # known max is 5
        algebraic_rows = ['1', '2', '3', '4', '5']

        for x in range(row + 1):# Printing row by row
            for y in range(col + 1): # Printing matrix coordinate on col
                print_string = " " + self.board_matrix[x][y] + " "
                print(print_string, end='')
                if (y < col):
                    print("|", end='')
                if (y == col):
                    print('   ' + algebraic_rows[row - x], end='')# algebraic notation guide
            print('')
            if x < row:  # Print horizontal dividers except after the last row
                for z in range(col): 
                    print("---|", end='')
                print("---")
        print('')
        # algebraic notation guide
        for x in range(row + 1):
            print(' '+ algebraic_cols[x], end='  ')
        print('')
        miscFunctions.print_blank_lines()
    
    def check_for_win(self, player_name):
        row = int(math.sqrt(self.size))
        col = int(math.sqrt(self.size))

        # Basic Row/Col checks
        for i in range(row):
            if all(cell == player_name for cell in self.board_matrix[i]):
                return True
        for j in range(col):
            if all(self.board_matrix[i][j] == player_name for i in range(row)):
                return True
        # Left to right diagonals
        if all(self.board_matrix[m][m] == player_name for m in range(row)):
            return True
        # Right to left diagonals
        if all(self.board_matrix[row - 1 - m][m] == player_name for m in range(row)):
            return True
        
        return False

class Game_UI:
    def __init__(self) -> None:
        pass
    def print_main_menu(self):
        miscFunctions.print_blank_lines()
        miscFunctions.print_dash()
        print("\t\tTic-Tac-Toe")
        print("\t\tMain Menu")
       
    def print_game_modes(self):
        miscFunctions.print_dash()
        print("Select a game mode")
        print("1. Player vs Player")
        print("2. Player vs CPU")
        print("3. CPU vs CPU")
        miscFunctions.print_dash()

    def print_CPU_difficulty_levels(self):
        miscFunctions.print_dash()
        print("Select a difficulty level for the CPU")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        miscFunctions.print_dash()

    def print_board_options(self):
        miscFunctions.print_dash()
        print('Select a board size')
        print('1. 3x3')
        print('2. 4x4')
        print('3. 5x5')
        miscFunctions.print_dash()

class Configuration:
    
    def __init__(self, game_mode, board_size):
        self.game_mode = game_mode
        self.board_size = board_size

    def get_game_mode(self):
        self.game_mode = miscFunctions.get_valid_integers(1, 3)
    
    def get_board_size(self):
        board_option = miscFunctions.get_valid_integers(1,3)
        match board_option:
            case 1: #3x3
                board_size = 9
            case 2: #4x4
                board_size = 16
            case 3: #5x5
                board_size = 25
        self.board_size = board_size

    def get_CPU_difficulty_level(self):
        Game_UI.print_CPU_difficulty_levels(Game_UI)
        return miscFunctions.get_valid_integers(1, 3)
        



def game_configuration():
    # Main Menu/Title
    game_config = Configuration(None, None)
    Game_UI.print_main_menu(Game_UI)
    
    # Present user w/ 3 game modes and configure based on input
    Game_UI.print_game_modes(Game_UI)
    game_config.get_game_mode()
    # Player v Player
    if (game_config.game_mode == 1): 
        Player1 = Player('X')
        Player2 = Player('O')
    # Player v CPU
    elif (game_config.game_mode == 2): 
        Player1 = Player('X')
        CPU_difficulty = game_config.get_CPU_difficulty_level()
        Player2 = CPU('O', CPU_difficulty)
    # CPU v CPU
    elif (game_config.game_mode == 3): 
        CPU_difficulty = game_config.get_CPU_difficulty_level()
        Player1 = CPU('X', CPU_difficulty)
        CPU_difficulty = game_config.get_CPU_difficulty_level()
        Player2 = CPU('O', CPU_difficulty)

    # Determine the board size
    Game_UI.print_board_options(Game_UI)
    game_config.get_board_size()
    game_board = Board(game_config.board_size, None)

    #Start the game now that configuration is complete
    game(game_config.game_mode, Player1, Player2, game_board)



def game(game_mode, player1, player2, game_board):
    print("Game ON")
    turn_limit = game_board.size
    turn = 0

    while (turn < turn_limit):
        game_board.print_board()
        # Player 1 turn
        player1.make_move(game_board.board_matrix)
        turn += 1
        if (game_board.check_for_win(player1.name) == True):
            game_board.print_board()
            print("Player 1 has won the game!!!")
            game_configuration()
        # Player 2 turn
        if (turn < turn_limit):
            game_board.print_board()
            player2.make_move(game_board.board_matrix)
            turn += 1
            if (game_board.check_for_win(player2.name) == True):
                game_board.print_board()
                print("Player 2 has won the game!!!")
                game_configuration()
    
    # Turn limit reached without a win
    game_board.print_board()
    print("The game is a DRAW.")
    game_configuration()


game_configuration() # This will build and start game