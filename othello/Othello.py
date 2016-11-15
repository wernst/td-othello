"""An Othello Game"""

import string
import numpy as np
from Board import Board

class Othello(object):
    def __init__(self):

        self.start()

    #initializes game board
    def start(self):
        self.game_board = Board()
        self.black_score = 2
        self.white_score = 2

    #Gets valid moves and places a tile on the board
    def setTile(self, row, col):
        self.game_board.updateValidMoves()
        points = self.game_board.addTile(row, col)
        self.updateScore(points)
        self.game_board.switchTurns()
    #Updates an input string to board coordinates
    def moveToCoords(self, move):
        move = move.upper()
        row = int(string.ascii_uppercase.index(move[0]))
        col = int(move[1])-1
        return (row, col)

    #Returns list of valid moves for the turn as strings
    def validMovesStringify(self):
        str_moves = []
        for k in self.game_board.valid_moves.keys():
            row = string.ascii_uppercase[k[0]]
            col = str(k[1]+1)
            str_moves.append(row+col)
        return str_moves

    def validMoveStringify(self, move):
        row = string.ascii_uppercase[move[0]]
        col = str(move[1]+1)
        return row+col

    #Validates user input
    def validateMoveInput(self, move):
        #too long or too short
        if move != "q":
            if (len(move)>2 or len(move) <= 1):
                print("invalid input")
                return False
            #not a valid board position
            elif not move[0].isalpha() or not move[1].isdigit():
                print("invalid input")
                return False

        return True

    def updateScore(self, points):
        if points > 0:
            if self.game_board.black_turn:
                self.black_score += points
                self.white_score -= (points-1)
            else:
                self.white_score += points
                self.black_score -= (points-1)
