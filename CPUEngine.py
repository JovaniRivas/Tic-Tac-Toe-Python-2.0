import random


def easy_CPU_engine(player_name, board):
    # First compile all the available moves on the board
    available_moves = determine_available_moves(board)
    return random.choice(available_moves)
    # return max_moves_to_win(player_name, board.board_matrix)


def medium_CPU_engine(player_name, board):
    if player_name == "X":
        opponent = "O"
    else:
        opponent = "X"
    row = len(board.board_matrix)
    col = len(board.board_matrix)

    # First compile all the available moves on the board
    available_moves = determine_available_moves(board)

    # For all the available moves, check to see if any result in a win or a block
    for coordinate in available_moves:
        # Check for any winning moves first
        selected_coordinate = coordinate
        selected_row, selected_col = selected_coordinate
        board.board_matrix[selected_row][selected_col] = player_name
        """ Checking wins disabled for medium. Re-enable/modify if needed
        if board.check_for_win(player_name) or len(available_moves) == 1:
            board.board_matrix[selected_row][selected_col] = " "
            return coordinate
        """
        # Check for any blocking moves next
        board.board_matrix[selected_row][selected_col] = " "
        board.board_matrix[selected_row][selected_col] = opponent
        if board.check_for_win(opponent):
            board.board_matrix[selected_row][selected_col] = " "
            return coordinate
        board.board_matrix[selected_row][selected_col] = " "
    # If no wins or blocks, make the worst best move (still an attempt to win, but the longest path)
    return max_moves_to_win(player_name, board.board_matrix)


def hard_CPU_engine(player_name, board):
    if player_name == "X":
        opponent = "O"
    else:
        opponent = "X"
    row = len(board.board_matrix)
    col = len(board.board_matrix)

    # First compile all the available moves on the board
    available_moves = determine_available_moves(board)

    # For all the available moves, check to see if any result in a win or a block
    for coordinate in available_moves:
        # Check for any winning moves first
        selected_coordinate = coordinate
        selected_row, selected_col = selected_coordinate
        board.board_matrix[selected_row][selected_col] = player_name
        if board.check_for_win(player_name) or len(available_moves) == 1:
            board.board_matrix[selected_row][selected_col] = " "
            return coordinate
        # Check for any blocking moves next
        board.board_matrix[selected_row][selected_col] = " "
        board.board_matrix[selected_row][selected_col] = opponent
        if board.check_for_win(opponent):
            board.board_matrix[selected_row][selected_col] = " "
            return coordinate
        board.board_matrix[selected_row][selected_col] = " "
    # If no wins or blocks, make the best move (minimum that will result in a win)
    return min_moves_to_win(player_name, board.board_matrix)


def determine_available_moves(board):
    available_moves = []
    row = len(board.board_matrix)
    col = len(board.board_matrix)
    for i in range(row):
        for j in range(col):
            if board.board_matrix[i][j] == " ":
                available_moves.append([i, j])
    return available_moves


# Given a player and board, find an available move that is closest to a win
def min_moves_to_win(player_name, board_matrix):

    # First, get the # of moves needed to win for every empty position
    row_move_dict, col_move_dict, fwd_diag_dict, rev_diag_dict = calculate_moves_to_win(
        player_name, board_matrix
    )

    # Determine the best move (minimum amount of moves to win) - Check ALL dictionaries
    min_moves_to_win = float("inf")
    # Rows
    for coordinate, moves_to_win in row_move_dict.items():
        if moves_to_win < min_moves_to_win:
            min_moves_to_win = moves_to_win
            min_coordinate = coordinate
    # Columns
    for coordinate, moves_to_win in col_move_dict.items():
        if moves_to_win < min_moves_to_win:
            min_moves_to_win = moves_to_win
            min_coordinate = coordinate
    # Forward Diagonal (Top Left to Bottom Right)
    for coordinate, moves_to_win in fwd_diag_dict.items():
        if moves_to_win < min_moves_to_win:
            min_moves_to_win = moves_to_win
            min_coordinate = coordinate
    # Reverse Diagonal (Top Right to Bottom Left)
    for coordinate, moves_to_win in rev_diag_dict.items():
        if moves_to_win < min_moves_to_win:
            min_moves_to_win = moves_to_win
            min_coordinate = coordinate

    return min_coordinate


# Given a player and board, find an available move that is farthest from a win
def max_moves_to_win(player_name, board_matrix):

    # First, get the # of moves needed to win for every empty position
    row_move_dict, col_move_dict, fwd_diag_dict, rev_diag_dict = calculate_moves_to_win(
        player_name, board_matrix
    )

    # Find the best coordinate with the maximum moves to win
    # Must account for scenarios where it is impossible to win (calculate_moves_to_win logic)
    max_moves_to_win = float("-inf")
    max_coordinate = None
    # Rows
    for coordinate, moves_to_win in row_move_dict.items():
        if moves_to_win > max_moves_to_win and moves_to_win < len(board_matrix):
            max_moves_to_win = moves_to_win
            max_coordinate = coordinate
    # Columns
    for coordinate, moves_to_win in col_move_dict.items():
        if moves_to_win > max_moves_to_win and moves_to_win < len(board_matrix):
            max_moves_to_win = moves_to_win
            max_coordinate = coordinate
    # Forward Diagonal (Top Left to Bottom Right)
    for coordinate, moves_to_win in fwd_diag_dict.items():
        if moves_to_win > max_moves_to_win and moves_to_win < len(board_matrix):
            max_moves_to_win = moves_to_win
            max_coordinate = coordinate
    # Reverse Diagonal (Top Right to Bottom Left)
    for coordinate, moves_to_win in rev_diag_dict.items():
        if moves_to_win > max_moves_to_win and moves_to_win < len(board_matrix):
            max_moves_to_win = moves_to_win
            max_coordinate = coordinate

    # If moves_to_win > length of board, basically going to be a tied game
    # Just send the min moves to move along
    if max_coordinate != None:
        return max_coordinate
    else:
        return min_moves_to_win(player_name, board_matrix)


# Calculate the number of moves needed to win for each available position
def calculate_moves_to_win(player_name, board_matrix):
    row = len(board_matrix)
    col = len(board_matrix)
    row_move_dict = {}
    col_move_dict = {}
    fwd_diag_move_dict = {}
    rev_diag_move_dict = {}
    if player_name == "X":
        opponent_name = "O"
    else:
        opponent_name = "X"

    # For each row, col, and diag, determine the moves to win
    # Map that value appropriately for each
    # Rows
    for i in range(row):
        moves_to_win = row
        for j in range(col):
            if board_matrix[i][j] == " ":
                row_move_dict[(i, j)] = 0
            elif board_matrix[i][j] == player_name:
                moves_to_win -= 1
            elif board_matrix[i][j] == opponent_name:
                moves_to_win += row  # can't win..
        # Map the # of moves to win to each element in that row
        for j in range(col):
            if board_matrix[i][j] == " ":
                row_move_dict[(i, j)] = moves_to_win

    # Columns
    for i in range(col):
        moves_to_win = col
        for j in range(row):
            if board_matrix[j][i] == " ":
                col_move_dict[(j, i)] = 0
            elif board_matrix[j][i] == player_name:
                moves_to_win -= 1
            elif board_matrix[j][i] == opponent_name:
                moves_to_win += row  # can't win..
        # Map the # of moves to win to each element in that row
        for j in range(col):
            if board_matrix[j][i] == " ":
                col_move_dict[(j, i)] = moves_to_win

    # Forward Diagonal (Top Left to Bottom Right)
    board_width = len(board_matrix)
    for i in range(board_width):
        moves_to_win = board_width
        if board_matrix[i][i] == " ":
            fwd_diag_move_dict[(i, i)] = 0
        elif board_matrix[i][i] == player_name:
            moves_to_win -= 1
        elif board_matrix[i][i] == opponent_name:
            moves_to_win += board_width  # can't win..
    # Map the # of moves to win to each element in that row
    for j in range(board_width):
        if board_matrix[i][i] == " ":
            fwd_diag_move_dict[(i, i)] = moves_to_win

    # Reverse Diagonal (Top Right to Bottom Left)
    for i in range(board_width):
        moves_to_win = board_width
        if board_matrix[i][board_width - 1 - i] == " ":
            rev_diag_move_dict[(i, board_width - 1 - i)] = 0
        elif board_matrix[i][board_width - 1 - i] == player_name:
            moves_to_win -= 1
        elif board_matrix[i][board_width - 1 - i] == opponent_name:
            moves_to_win += board_width  # can't win..
    # Map the # of moves to win to each element in that row
    for j in range(board_width):
        if board_matrix[i][board_width - 1 - i] == " ":
            rev_diag_move_dict[(i, board_width - 1 - i)] = moves_to_win

    return row_move_dict, col_move_dict, fwd_diag_move_dict, rev_diag_move_dict