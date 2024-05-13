def print_dash():
    for x in range(40):
        print('-', end='')
    print('')

def print_blank_lines():
    for x in range(2):
        print('')

def get_valid_integers(x, y): # range from x to y
    while True:
        try:
            valid_int = int(input("Input: "))

            if x <= valid_int <= y:
                return valid_int
            else:
                print(f"Please enter a valid number between {x} and {y}.")
        except ValueError:
            print(f"Please enter a valid number between {x} and {y}.")

def get_algebraic_input(board_matrix_size):
    algebraic_cols = ['a', 'b', 'c', 'd', 'e']
    algebraic_rows = ['1', '2', '3', '4', '5'] #max will be 5. Not all values used depending on size
    while True:
        algebraic_input = input("Input: ")
        if len(algebraic_input) == 2 and algebraic_input.isalnum: # Basic criteria
            algebraic_input = algebraic_input.lower()
            for x in range(board_matrix_size ):
                for y in range(board_matrix_size):
                    if algebraic_input == str(algebraic_cols[x] + algebraic_rows[y]):
                        match algebraic_input[0]:
                            case 'a': 
                                valid_col = 1
                            case 'b': 
                                valid_col = 2
                            case 'c': 
                                valid_col = 3
                            case 'd': 
                                valid_col = 4
                            case 'e': 
                                valid_col = 5
                        valid_row = board_matrix_size - int(algebraic_input[1]) + 1
                        return valid_col, valid_row
        print(f"Invalid input, please enter a value from a1 to {algebraic_cols[board_matrix_size - 1] + algebraic_rows[board_matrix_size - 1]}")