import random


# Easy: Returns a random move.
def easy_CPU_engine(board):
    available_moves = determine_available_moves(board)
    return random.choice(available_moves)


# Medium: Takes the longest path to win.
def medium_CPU_engine(player, board):
    available_moves = determine_available_moves(board)
    longest_path = max_moves_to_win(player, board.board_matrix)
    if longest_path != None:
        return longest_path
    else:
        return random.choice(available_moves)


# Hard: Takes the shortest path to win. Blocks if necessary.
def hard_CPU_engine(player, board):
    available_moves = determine_available_moves(board)

    # Check if any available moves result in a win
    for coordinate in available_moves:
        selected_row, selected_col = coordinate
        board.board_matrix[selected_row][selected_col] = player.name
        if board.check_for_win(player.name) or len(available_moves) == 1:
            board.board_matrix[selected_row][selected_col] = " "
            return coordinate
        board.board_matrix[selected_row][selected_col] = " "
    # Check if any available moves block opponent from winning
    for coordinate in available_moves:    
        selected_row, selected_col = coordinate
        board.board_matrix[selected_row][selected_col] = player.opponent_name()
        if board.check_for_win(player.opponent_name()):
            board.board_matrix[selected_row][selected_col] = " "
            return coordinate
        board.board_matrix[selected_row][selected_col] = " "
    # If no wins or blocks, make the best move (minimum that will result in a win)
    return min_moves_to_win(player, board.board_matrix)


# Simple function to determine all the available moves on the board
def determine_available_moves(board):
    available_moves = []
    row = len(board.board_matrix)
    col = len(board.board_matrix)
    for i in range(row):
        for j in range(col):
            if board.board_matrix[i][j] == " ":
                available_moves.append([i, j])
    return available_moves


# Determine the closes path to a win
def min_moves_to_win(player, board_matrix):

    # First, get the # of moves needed to win for every empty position
    # One position may span different paths so must account for each method of winning
    row_move_dict, col_move_dict, fwd_diag_dict, rev_diag_dict = calculate_moves_to_win(
        player, board_matrix
    )

    # Determine the minimum for each play Note: Board length not requred for min calculation
    min_row_coord, min_row_move = get_min_or_max(row_move_dict, "min", None)
    min_col_coord, min_col_move = get_min_or_max(col_move_dict, "min", None)
    min_fwd_diag_coord, min_fdiag_move = get_min_or_max(fwd_diag_dict, "min", None)
    min_rev_diag_coord, min_rdiag_move = get_min_or_max(rev_diag_dict, "min", None)

    min_dict = {
        min_row_move: min_row_coord,
        min_col_move: min_col_coord,
        min_fdiag_move: min_fwd_diag_coord,
        min_rdiag_move: min_rev_diag_coord,
    }

    return min_dict[min(min_row_move, min_col_move, min_fdiag_move, min_rdiag_move)]


# Determine the farthest path to a win (highest moves to win )
def max_moves_to_win(player, board_matrix):
    longest_path_coordinate = None

    # First, get the # of moves needed to win for every empty position
    # One position may span different paths so must account for each method of winning
    row_move_dict, col_move_dict, fwd_diag_dict, rev_diag_dict = calculate_moves_to_win(
        player, board_matrix
    )

    # Determine the maximum Note: Board length requred for max calculation
    max_row_coord, max_row_move = get_min_or_max(
        row_move_dict, "max", len(board_matrix)
    )
    max_col_coord, max_col_move = get_min_or_max(
        col_move_dict, "max", len(board_matrix)
    )
    max_fwd_diag_coord, max_fdiag_move = get_min_or_max(
        fwd_diag_dict, "max", len(board_matrix)
    )
    max_rev_diag_coord, max_rdiag_move = get_min_or_max(
        rev_diag_dict, "max", len(board_matrix)
    )

    max_dict = {
        max_row_move: max_row_coord,
        max_col_move: max_col_coord,
        max_fdiag_move: max_fwd_diag_coord,
        max_rdiag_move: max_rev_diag_coord,
    }

    longest_path_coordinate = max_dict[
        max(max_row_move, max_col_move, max_fdiag_move, max_rdiag_move)
    ]
    if longest_path_coordinate != None:
        return longest_path_coordinate
    else:
        return None


# Returns the shortest/longest path within a givin dictionary
def get_min_or_max(dictionary, choice, board_matrix_length):
    if choice == "min":
        min_moves_to_win = float("inf")
        min_coordinate = None
        for coordinate, moves_to_win in dictionary.items():
            if moves_to_win < min_moves_to_win:
                min_moves_to_win = moves_to_win
                min_coordinate = coordinate
        return min_coordinate, min_moves_to_win
    elif choice == "max":
        max_moves_to_win = float("-inf")
        max_coordinate = None
        for coordinate, moves_to_win in dictionary.items():
            if moves_to_win > max_moves_to_win and moves_to_win < board_matrix_length:
                max_moves_to_win = moves_to_win
                max_coordinate = coordinate
        if max_coordinate != None:
            return max_coordinate, max_moves_to_win
        else:
            return None, max_moves_to_win


# Calculate the number of moves needed to win for each available position
def calculate_moves_to_win(player, board_matrix):
    row = col = len(board_matrix)
    row_move_dict, col_move_dict, fwd_diag_move_dict, rev_diag_move_dict = (
        {},
        {},
        {},
        {},
    )

    # For each row, col, and diag, determine the moves to win

    # Rows
    for i in range(row):
        moves_to_win = row
        for j in range(col):
            if board_matrix[i][j] == " ":
                row_move_dict[(i, j)] = 0
            elif board_matrix[i][j] == player.name:
                moves_to_win -= 1
            elif board_matrix[i][j] == player.opponent_name():
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
            elif board_matrix[j][i] == player.name:
                moves_to_win -= 1
            elif board_matrix[j][i] == player.opponent_name():
                moves_to_win += row  # can't win..
        # Map the # of moves to win to each element in that row
        for j in range(col):
            if board_matrix[j][i] == " ":
                col_move_dict[(j, i)] = moves_to_win

    # Forward Diagonal (Top Left to Bottom Right)
    moves_to_win = len(board_matrix)
    for i in range(len(board_matrix)):
        if board_matrix[i][i] == " ":
            fwd_diag_move_dict[(i, i)] = 0
        elif board_matrix[i][i] == player.name:
            moves_to_win -= 1
        elif board_matrix[i][i] == player.opponent_name():
            moves_to_win += len(board_matrix)  # can't win..
    # Map the # of moves to win to each element in that row
    for i in range(len(board_matrix)):
        if board_matrix[i][i] == " ":
            fwd_diag_move_dict[(i, i)] = moves_to_win

    # Reverse Diagonal (Top Right to Bottom Left)
    moves_to_win = len(board_matrix)
    for i in range(len(board_matrix)):
        if board_matrix[i][len(board_matrix) - 1 - i] == " ":
            rev_diag_move_dict[(i, len(board_matrix) - 1 - i)] = 0
        elif board_matrix[i][len(board_matrix) - 1 - i] == player.name:
            moves_to_win -= 1
        elif board_matrix[i][len(board_matrix) - 1 - i] == player.opponent_name():
            moves_to_win += len(board_matrix)  # can't win..
    # Map the # of moves to win to each element in that row
    for i in range(len(board_matrix)):
        if board_matrix[i][len(board_matrix) - 1 - i] == " ":
            rev_diag_move_dict[(i, len(board_matrix) - 1 - i)] = moves_to_win

    return row_move_dict, col_move_dict, fwd_diag_move_dict, rev_diag_move_dict
