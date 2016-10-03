"""An Othello Game"""

import string
from Board import Board

class Othello(object):
    def __init__(self):

        self.start()

    #initializes game board
    def start(self):
        self.game_board = Board()

    #Gets valid moves and places a tile on the board
    def setTile(self, row, col):
        self.game_board.updateValidMoves()
        self.game_board.addTile(row, col)

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


    #plays the game
    def play(self):

        while True:
            self.game_board.updateValidMoves()

            #if no valid moves, switch turns and check for winner
            if self.game_board.valid_moves == {}:
                if self.game_board.black_turn:
                    print("Black cannot make any valid moves")
                else:
                    print("White's cannot make any valid moves")
                self.game_board.switchTurns()
                #check for winner
                self.game_board.updateValidMoves()
                if self.game_board.valid_moves == {}:
                    break

            #print score
            print("Black - {}\tWhite - {}").format(self.game_board.black_score, self.game_board.white_score)
            #print board
            print(self.game_board)

            #print turn
            if self.game_board.black_turn:
                print("Black's Turn")
            else:
                print("White's Turn")

            #Print valid moves
            print("Valid Moves: {}").format(self.validMovesStringify())

            #Get move input
            move = raw_input("Choose move (q to quit): ")

            #validate input
            is_valid_move = self.validateMoveInput(move)

            if is_valid_move:
                if move == "q" :
                    break
                else:
                    move = self.moveToCoords(move)
                    self.setTile(move[0], move[1])


        #Game Over
        print("Black - {}\tWhite - {}").format(self.game_board.black_score, self.game_board.white_score)
        print(self.game_board)

        #Check score
        if(self.game_board.black_score > self.game_board.white_score):
            print("Black Wins!")
        elif(self.game_board.black_score < self.game_board.white_score):
            print("White Wins!")
        elif(self.game_board.black_score == self.game_board.white_score):
            print("It's a tie!")
