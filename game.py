# Connect 4
# Player 1 is 'X', player 2 is 'O'

from board import Board

def get_difficulty_input():
    # gets the difficulty from the user and returns as an integer
    proper_input = False
    user_input = input(f'Choose your difficulty level (between 1 and 5): ')
    while not proper_input:
        try:
            user_input = int(user_input)
            if user_input < 0 or user_input > 5: # 0, -1 for testing
                user_input = input("Difficulty must be an integer between 1 and 5: ")
                proper_input = False
                break                
            proper_input = True
        except ValueError:
            user_input = input("Difficulty must be an integer between 1 and 5: ")
    return user_input

def get_input():
    # get the slot number from the user and return as an integer
    proper_input = False
    user_input = input(f'Select a column: ')
    while not proper_input:
        try:
            user_input = int(user_input)
            if user_input < -1 or user_input > 7: # 0 and -1 are allowed for debugging purposes.  (in make_test_board)
                user_input = input("Input must be an integer between 1 and 7: ")
                proper_input = False
                break                
            proper_input = True
        except ValueError:
            user_input = input("Input must be an integer between 1 and 7: ")
    return user_input

def play_human():
    # to play against your friends
    board = Board()
    player = 2
    while not board.check_for_win():
        if player == 2:
            player = 1
        else:
            player = 2

        board.printBoard()
        user_input = get_input(player)
        board.place(user_input-1, player)
        board.printBoard()
    print(f'Congratulations Player {player}, you win!')

def play_computer(difficulty):
    # to play against the AI
    board = Board()
    player = 1
    while not board.check_for_win()[0]:
        # display board, allow user to choose a column, show new board to user
        board.printBoard()
        user_input = get_input()
        board.place(user_input-1, player)
        board.printBoard()

        # get minimax selection from computer
        board = board.minimax(difficulty, True)[1]
        board.printBoard()
    if board.check_for_win()[1] == 'O':
        print('The AI wins!')
    else:
        print(f'Congratulations! You beat the AI at difficulty level {difficulty}')

def make_test_board():
    # used for debugging purposes. Allows me to make a board using the CLI.
    board = Board()
    user_input = -10
    player = 1
    while not board.check_for_win()[0]:
        board.printBoard()
        if user_input == -1:
            player = 2 if player == 1 else 1
        user_input = get_input()
        if user_input != -1 and user_input != 0:
            board.place(user_input-1, player)
    board.printBoard()
    return board
        
        
    

def main():
    difficulty = get_difficulty_input()
    play_computer(difficulty)
if __name__ == "__main__":
    main()