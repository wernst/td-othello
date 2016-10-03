"""An object representing an othello board"""


import string
from Direction import directions
EMPTY_VAL = 0
BLACK_VAL = "B"
WHITE_VAL = "W"
ROWS = 8
COLS = 8

class Board(object):
    def __init__(self):
        self.start()

    #set up board's initial state
    def start(self):
        self.board = []
        for i in range(ROWS):
            self.board.append([])
            for j in range(COLS):
                self.board[i].append(EMPTY_VAL)

        self.board[3][3] = BLACK_VAL
        self.board[4][4] = BLACK_VAL
        self.board[3][4] = WHITE_VAL
        self.board[4][3] = WHITE_VAL

        self.valid_moves = {}
        self.black_turn = True
        self.black_score = 2
        self.white_score = 2


    """Valid move: adjacent to other color, same color on that diagonal/row/col"""
    #Updates our current memory of valid moves
    def updateValidMoves(self):
        self.valid_moves = {}
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == EMPTY_VAL:
                    dir_list = self.checkAdjacents(i, j)
                    valid_dirs = self.confirmMove(dir_list, i , j)
                    if len(valid_dirs) > 0:
                        self.valid_moves[(i, j)] = valid_dirs


    def switchTurns(self):
        self.black_turn = not self.black_turn

    #checks a tile's adjacent tiles to see if there is a possible valid move
    def checkAdjacents(self, row, col):
        adjacent_list = [] #list of locations where there is an adjacent opposite color
        for k, d in directions.items():
            new_row = row + d[0]
            new_col = col + d[1]

            #if valid row/col combination
            if new_row > 0 and new_col > 0 and new_row < ROWS and new_col < COLS:
                if self.black_turn and self.board[new_row][new_col] == WHITE_VAL:
                    adjacent_list.append(k)
                elif (not self.black_turn) and self.board[new_row][new_col] == BLACK_VAL:
                    adjacent_list.append(k)

        return adjacent_list

    #Confirm that a possible move is indeed a valid move (the move surrounds the opposite color)
    def confirmMove(self, dir_list, row, col):
        valid_directions = []

        #for each possible direction
        for d in dir_list:
            #valid = False
            #current = self.board[row][col]
            curr_row = row
            curr_col = col
            while True:
                curr_row += directions[d][0]
                curr_col += directions[d][1]

                #if invalid or empty
                if curr_col >= COLS or curr_row >= ROWS or self.board[curr_row][curr_col]==EMPTY_VAL:
                    break

                #if direction valid, append to list of valid directions for this move
                else:
                    if self.black_turn and self.board[curr_row][curr_col] == BLACK_VAL:
                        valid_directions.append(d)
                    elif (not self.black_turn) and self.board[curr_row][curr_col] == WHITE_VAL:
                        valid_directions.append(d)
        return valid_directions



    #Place a piece on the board
    def addTile(self, row, col):
        if (row, col) in self.valid_moves.keys():
            if self.black_turn:
                self.board[row][col] = BLACK_VAL
            else:
                self.board[row][col] = WHITE_VAL
            self.updateBoard(row, col)
            self.switchTurns()
        else:
            print("INVALID MOVE")

    #Updates the board after a move (flips tiles and changes score)
    def updateBoard(self, row, col):
        update_dirs = self.valid_moves[(row, col)]
        counter = 1 #start at 1 for the piece you put down
        for d in update_dirs:

            curr_row = row
            curr_col = col
            while True:
                #print("[{}, {}]").format(curr_row, curr_col)
                curr_row += directions[d][0]
                curr_col += directions[d][1]
                if self.black_turn:
                    if self.board[curr_row][curr_col] == BLACK_VAL:
                        break
                    else:
                        self.board[curr_row][curr_col] = BLACK_VAL
                        counter+=1
                elif not self.black_turn:
                    if self.board[curr_row][curr_col] == WHITE_VAL:
                        break
                    else:
                        self.board[curr_row][curr_col] = WHITE_VAL
                        counter+=1
        self.updateScore(counter)


 
    def updateScore(self, points):
        if self.black_turn:
            self.black_score += points
            self.white_score -= (points-1)
        else:
            self.white_score += points
            self.black_score -= (points-1)






    def __str__(self):

        board_string = "     1   2   3   4   5   6   7   8\n"
        board_string += "   +---+---+---+---+---+---+---+---+\n"
        for i in range(len(self.board)):
            board_string += " "+string.ascii_uppercase[i]+" "
            for j in range(len(self.board[i])):
                board_string += "+ "+str(self.board[i][j]) + " "
            board_string += "+\n"
            board_string += "   +---+---+---+---+---+---+---+---+\n"
        return board_string
