def print_dash():
    for x in range(40):
        print("-", end="")
    print("")


def print_blank_lines():
    for x in range(2):
        print("")


def get_valid_integers(x, y):  # range from x to y
    while True:
        try:
            valid_int = int(input("Input: "))

            if x <= valid_int <= y:
                return valid_int
            else:
                print(f"Please enter a valid number between {x} and {y}.")
        except ValueError:
            print(f"Please enter a valid number between {x} and {y}.")


# Gets algebraic notation input from user (a1)
# Converts valid notations to an appropriate integer for program to use
def get_algebraic_input(board):
    while True:
        algebraic_input = input("Input: ")
        if len(algebraic_input) == 2 and algebraic_input.isalnum:  # Basic criteria
            algebraic_input = algebraic_input.lower()
            for x in range(board.matrix_size):
                for y in range(board.matrix_size):
                    valid_position = board.ascii_column[x] + str(board.num_row[y])
                    if algebraic_input == valid_position:
                        valid_col = (
                            ord(board.ascii_column[x]) - 96
                        )  # 97(a) - 96 = 1, 98(b) - 96 = 2, etc
                        valid_row = board.matrix_size - board.num_row[y] + 1
                        return valid_col, valid_row
        print(
            f"Invalid input, please enter a value from a1 to {board.ascii_column[board.matrix_size - 1] + str(board.num_row[board.matrix_size - 1])}"
        )


def num_to_algebraic(col_pos, row_pos, board):

    # Algebraic Column: ascii for a (col 0) is 97
    algebraic_col = chr(97 + col_pos)
    # Determine algebraic notation for row
    algebraic_row = board.matrix_size - row_pos

    # Return it already concatenated
    algebraic_coordinate = algebraic_col + str(algebraic_row)
    return algebraic_coordinate
