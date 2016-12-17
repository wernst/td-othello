"""An object representing an othello board"""


import string, sys
import numpy as np
from Direction import directions
EMPTY_VAL = " "
BLACK_VAL = "B"
WHITE_VAL = "W"
ROWS = 8
COLS = 8

class Board(object):
    def __init__(self, board_arr = None, black_turn = True):
        self.start(board_arr, black_turn)

    #set up board's initial state
    def start(self, board_arr, black_turn):
        if board_arr == None:
            self.board = []
            for i in range(ROWS):
                self.board.append([])
                for j in range(COLS):
                    self.board[i].append(EMPTY_VAL)

            self.board[3][3] = WHITE_VAL
            self.board[4][4] = WHITE_VAL
            self.board[3][4] = BLACK_VAL
            self.board[4][3] = BLACK_VAL

            self.black_turn = True
            self.valid_moves = {}
            self.updateValidMoves()

        else:
            board_len = sum(len(x) for x in board_arr)
            if board_len != 64:
                print("Board length is {}, should be 64").format(board_len)
                sys.exit(1)
            else:
                self.board = board_arr
                self.black_turn = black_turn
                self.valid_moves = {}
                self.updateValidMoves()


    """Valid move: adjacent to other color, same color on that diagonal/row/col"""
    #Updates our current memory of valid moves
    def updateValidMoves(self):
        self.valid_moves.clear()
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
            if new_row >= 0 and new_col >= 0 and new_row < ROWS and new_col < COLS:
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
                if curr_col >= COLS or curr_row >= ROWS or curr_col < 0 or curr_row < 0 or self.board[curr_row][curr_col]==EMPTY_VAL:
                    break

                #if direction valid, append to list of valid directions for this move
                else:
                    if self.black_turn and self.board[curr_row][curr_col] == BLACK_VAL:
                        valid_directions.append(d)
                    elif (not self.black_turn) and self.board[curr_row][curr_col] == WHITE_VAL:
                        valid_directions.append(d)
        return valid_directions



    #Place a piece on the board, return score change
    def addTile(self, row, col):
        score_change = 0
        if self.black_turn:
            self.board[row][col] = BLACK_VAL
        else:
            self.board[row][col] = WHITE_VAL
        score_change = self.updateBoard(row, col)


        return score_change

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
        return counter

    def boardToVector(self):
        vector_input = []
        for row in self.board:
            for item in row:
                if item == EMPTY_VAL:
                    vector_input.append(0)
                    #vector_input.append(0)
                elif item == BLACK_VAL:
                    vector_input.append(1)
                    #vector_input.append(0)
                elif item == WHITE_VAL:
                    vector_input.append(-1)
                    #vector_input.append(1)

        vector = np.matrix(np.array(vector_input))
        return vector








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
