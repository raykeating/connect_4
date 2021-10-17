import copy

class Board:
    # The Board class is an object containing 3 class attributes: (rows, columns) -> the size of the board
    # and "board", a list of lists where each list represents a column on the board.

    # There are multiple functions in Board() that allow for manipulation of the board object.

    def __init__(self):
        # the constructor
        self.rows = 6
        self.columns = 7
        self.board = None
        self.initialize_board()

    def initialize_board(self):
        empty_board = []
        for i in range(self.columns):
            column = [None for x in range(6)]
            empty_board.append(column)
        self.board = empty_board

    def printBoard(self):
        print('   1     2     3     4     5     6     7   ', end="\n\n")
        for i in reversed(range(6)):
            print('|', end="  ")
            for j in range (7):
                if self.board[j][i]:
                    print(self.board[j][i],end="  |  ")
                else:
                    print(" ",end="  |  ")
            print('\n')

    def place(self, slot, player):
        # places a piece on the board.  
        # slot is an integer between 0 and 6 corresponding to columns on the board
        # player is an integer: 1 or 2 that represents which piece should be placed (X or O)

        # if a player tries to place in a column that is full, no piece will be placed and they lose their turn.

        if player == 1:
            for i in range(self.rows):
                if not self.board[slot][i]:
                    self.board[slot][i] = 'X'
                    break
        elif player == 2:
            for i in range(self.rows):
                if not self.board[slot][i]:
                    self.board[slot][i] = 'O'
                    break
        else:
            raise ValueError("Player value must be an integer: 1 or 2")
    
    def get_columns(self):
        # this method returns all columns of a given board as a list of lists, where each list is made of tuples (i, j) that 
        # correspond to indexes of a column on the board
        columns = []

        for j in range(self.columns):
            single_column = []
            for i in range(self.rows):
                single_column.append(self.board[j][i])
            columns.append(single_column)
        return columns

    def get_rows(self):
        # this method returns all rows of a given board as a list of lists, where each list is made of tuples (i, j) that 
        # correspond to indexes of a row on the board.
        rows = []

        for i in range(self.rows):
            single_row = []
            for j in range(self.columns):
                single_row.append(self.board[j][i])
            rows.append(single_row)
        return rows              

    def get_diagonals(self):
        # this method returns all diagonals of a given board as a list of lists, where each list is made of tuples (i, j) that correspond to a diagonal on the board
        # for the sake of this game, it only returns diagonals longer than 3, since you'd need 4 spaces in a row to win. 
        diagonals = []
        within_bounds = True
        # upwards-to-the-right diagonal (1) 
        for i in range(self.rows): # or self.rows
            index_i = i
            index_j = 0
            single_diagonal = []
            while(within_bounds):
                try:
                    single_diagonal.append(self.board[index_j][index_i])
                    index_i += 1
                    index_j += 1
                except IndexError:
                    within_bounds = False
            within_bounds = True
            if len(single_diagonal) >= 4:
                diagonals.append(single_diagonal)
        
        # upwards-to-the-right diagonal (2) 
        for i in range(self.columns): # or self.columns
            index_i = 0
            index_j = i
            single_diagonal = []
            while(within_bounds):
                try:
                    single_diagonal.append(self.board[index_j][index_i])
                    index_i += 1
                    index_j += 1
                except IndexError:
                    within_bounds = False
            within_bounds = True
            if len(single_diagonal) >= 4:
                diagonals.append(single_diagonal)

        # downwards-to-the-right diagonal (1) 
        for i in range(self.rows): # or self.rows
            index_i = i
            index_j = 0
            single_diagonal = []
            while(within_bounds):
                try:
                    if (index_i < 0 or index_j < 0):
                        raise IndexError
                    single_diagonal.append(self.board[index_i][index_j])
                    index_i -= 1
                    index_j += 1
                except IndexError:
                    within_bounds = False
            within_bounds = True
            if len(single_diagonal) >= 4:
                diagonals.append(single_diagonal)
        
        # downwards-to-the-right diagonal (2) 
        for i in range(self.columns): # or self.columns
            index_i = 5
            index_j = i
            single_diagonal = []
            while(within_bounds):
                try:
                    if (index_i < 0 or index_j < 0):
                        raise IndexError
                    single_diagonal.append(self.board[index_j][index_i])
                    index_i -= 1
                    index_j += 1
                except IndexError:
                    within_bounds = False
            within_bounds = True
            if len(single_diagonal) >= 4:
                diagonals.append(single_diagonal)
        
        return diagonals

    def get_all_lines(self):
        # combines the columns, rows, and diagonals to get all possible lines on the board
        # does not include diagonals of length < 4, since those wouldn't be winnable lines.
        all_lines = []
        all_lines.append(self.get_rows())
        all_lines.append(self.get_columns())
        all_lines.append(self.get_diagonals())
        # flattens the list so it isn't a list of list of lists but a list of lists
        all_lines = [item for sublist in all_lines for item in sublist]
        return all_lines

    def check_for_win(self):
        # goes through each line and checks the maximum consecutive pieces and the piece type
        # if there are 4 (or more) pieces in a row, the function will return True
        lines = self.get_all_lines()
        consecutive_piece_type = None
        consecutive_pieces_max = 0
        consecutive_pieces = 1
        previous_piece = None
        for i in range(len(lines)):
            consecutive_pieces = 1
            for j in range(len(lines[i])):
                if previous_piece != None and previous_piece == lines[i][j]:
                    consecutive_pieces += 1
                    if consecutive_pieces_max < consecutive_pieces:
                        consecutive_pieces_max = consecutive_pieces
                        consecutive_piece_type = lines[i][j]
                else:
                    consecutive_pieces = 1
                previous_piece = lines[i][j]
            previous_piece = None
        if consecutive_pieces_max >= 4:
            return True, consecutive_piece_type
        else:
            return False, 'No winner'

    def evaluate(self):
        # this function returns the value of the a board to player (integer: 1 or 2)
        # player 1 is 'X', player 2 is 'O'

        # Heuristic is pretty simple.  Checks how many pieces in a row player X has.
        # 2 pieces: +5pts, 3 pieces: +30pts, 4 pieces (win), +1000pts.
        # Opponent's pieces are rated inversely.  So if the player's opponent has
        # 2 pieces, it would be -5pts, 3 pieces: -30, and 4 pieces: -1000pts.

        # Note: it counts total number of consecutive pieces across the whole board,
        # so if a player made a move that created 2 rows of 3 pieces length, the board
        # would be rated +60pts rather than +30pts.

        # Assume the evaluation is from the perspective of the AI,
        # so a positive value would be a favourable position for the AI, 
        # and a negative would be an unfavourable position

        player_piece = 'O'
        opponent_piece = 'X'
        
        points = 0

        lines = self.get_all_lines()
        consecutive_pieces = 1
        consecutive_pieces_max = 0
        previous_piece = None
        for i in range(len(lines)):
            for j in range(len(lines[i])):
                if previous_piece != None and previous_piece == lines[i][j]:
                    consecutive_pieces += 1
                    if consecutive_pieces_max < consecutive_pieces:
                        consecutive_pieces_max = consecutive_pieces
                else:
                    if consecutive_pieces_max > 1:
                        if previous_piece == player_piece:
                            if consecutive_pieces_max == 2:
                                points += 5
                            if consecutive_pieces_max == 3:
                                points += 30
                            if consecutive_pieces_max >= 4:
                                return 1000
                        if previous_piece == opponent_piece:
                            if consecutive_pieces_max == 2:
                                points -= 5
                            if consecutive_pieces_max == 3:
                                points -= 30
                            if consecutive_pieces_max >= 4:
                                return -1000
                    consecutive_pieces = 1
                    consecutive_pieces_max = 0
                previous_piece = lines[i][j]
                
        return points
        
    def get_children(self, player):
        # this function returns all possible boards one move ahead of the given board.
        # returns as a list of Board objects

        children = []

        for i in range(self.columns):
            # if self.board[i][self.rows-1] == None: # as long the column isn't full already
            temp_board = copy.deepcopy(self)
            temp_board.place(i, player)
            # as long as the row isn't full
            if temp_board.board[i][self.rows-1] == None:
                children.append(temp_board)

        return children

    def minimax(self, depth, maximizing_player):
        # on my computer with semi-new hardware (i7 9th generation), this algorithm can run
        # at depth 5 in about 3-5 seconds.  Anything higher than 5 and it becomes too slow for this game.

        # base case: if the depth limit has been reached or if the board is a winning board.
        score = self.evaluate()
        if depth == 0 or score == -1000 or score == 1000:
            return (score, self)
        
        # if it is the AI's move (the AI is trying to maximize their score)
        if maximizing_player:
            maxEval = -1000
            best_board = None
            for child in self.get_children(2):
                eval = child.minimax((depth-1), False)
                if eval[0] > maxEval:
                    maxEval = eval[0]
                    best_board = child
            return (maxEval, best_board)
        
        # if it is the opponent's move (the AI is trying to minimize the opponent's score)
        else:
            min_eval = 1000
            best_board = None
            for child in self.get_children(1):
                eval = child.minimax((depth-1), True)
                if eval[0] < min_eval:
                    min_eval = eval[0]
                    best_board = child
            # if type(best_board) == None:
            #     best_board = self.place()
            return (min_eval, best_board)

        # The code for this algorithm is heavily inspired by Sebastian Lague's minimax video:
        # https://www.youtube.com/watch?v=l-hh51ncgDI
