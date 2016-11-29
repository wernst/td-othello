"""Plays othello game"""


from Othello import Othello
from Player import Player
from NeuralNetwork import NeuralNetwork
from Board import Board
import numpy as np
import random
import sys

#sys.path.append("/anaconda/bin")
nn = NeuralNetwork(50, 1.0, 0.9, 0.01)
bWin = 0
wWin = 0
ties = 0


def main():
    global nn

    #learn("nn2000_nnrand.pk1", 2000, "nn_random")
    #runGames("nn2000_nnrand.pk1", 200)
    #testBoardState("nn500.pk1")
    runGameWithOutput("nn5000_nnrand.pk1")
    #nn.load("nn5000_nnrand.pk1")
    #play1(True)


#===============================================================================
#Testing
#===============================================================================

#trains neural network
def learn(nn_file, episodes=1000, p_type="nn"):
    global nn
    nn.learn(episodes, p_type)
    nn.save(nn_file)

#runs a certain number of game iterations
def runGames(nn_file, iterations):
    global nn, bWin, wWin, ties
    nn.load(nn_file)
    for i in xrange(iterations):
        print(i)
        play0()
    print("black wins: {}").format(bWin)
    print("white wins: {}").format(wWin)
    print("ties: {}").format(ties)
    print("\nwin pct: {}").format(bWin/(iterations*1.0))


def runGameWithOutput(nn_file):
    global nn
    nn.load(nn_file)
    playVerbose()

#Tests a board state (input inside the function)
def testBoardState(nn_file):
    state = [[" ", "W", "W", "W", "B", "B", " ", " "],
            ["W", "W", "W", "W", "W", "B", "W", " "],
            ["W", "B", "W", "B", "W", "B", "W", "B"],
            ["B", "B", "W", "W", "B", "W", "B", "W"],
            ["B", "W", "W", "W", "B", "B", "W", "B"],
            ["W", "W", "W", "W", "W", "B", "W", "B"],
            ["W", "B", "W", "B", "W", "B", "W", "B"],
            ["B", "B", "W", "W", "B", "W", "B", "W"]]

    state_vec = np.matrix([0, -1, -1, -1, 1, 1, 0, 0,
                        -1, -1, -1, -1, -1, 1, -1, 0,
                        -1, 1, -1, 1, -1, 1, -1, 1,
                        1, 1, -1, -1, 1, -1, 1, -1,
                        1, -1, -1, -1, 1, 1, -1, 1,
                        -1, -1, -1, -1, -1, 1, -1, 1,
                        -1, 1, -1, 1, -1, 1, -1, 1,
                        1, 1, -1, -1, 1, -1, 1, -1])
    state2 = [[" ", "W", "W", "W", "W", "W", "W", "W"],
            ["W", "W", "W", "W", "W", "W", "W", "W"],
            ["W", "W", "W", "W", "W", "W", "W", "W"],
            ["W", "W", "W", "W", "W", "W", "W", "W"],
            ["W", "W", "W", "W", "W", "W", "W", "W"],
            ["W", "W", "W", "W", "W", "W", "W", "W"],
            ["W", "W", "W", "W", "W", "W", "W", "W"],
            ["B", "W", "W", "W", "W", "W", "W", "W"]]
    state3 = [[" ", "B", "B", "B", "B", "B", "B", "B"],
            ["B", "B", "B", "B", "B", "B", "B", "B"],
            ["B", "B", "B", "B", "B", "B", "B", "B"],
            ["B", "B", "B", "B", "B", "B", "B", "B"],
            ["B", "B", "B", "B", "B", "B", "B", "B"],
            ["B", "B", "B", "B", "B", "B", "B", "B"],
            ["B", "B", "B", "B", "B", "B", "B", "B"],
            ["W", "B", "B", "B", "B", "B", "B", "B"]]
    board = Board(state3)
    print(board)
    #print(nn.wMatrix1)
    #print("-------------")
    nn.load(nn_file)
    #print(nn.wMatrix1)
    board_vector = board.boardToVector()
    value = nn.getValue(board_vector)
    print(value)


def getNNInputs(state):
    nn_inputs = {}
    for coord in self.game.game_board.valid_moves.keys():
        board_copy = copy.deepcopy(self.game.game_board)
        board_copy.addTile(coord[0], coord[1])
        board_vector = board_copy.boardToVector()
        nn_inputs[coord] = board_vector
    return nn_inputs


def prototypePresention():
    while(True):
        nn_type = raw_input("(1) For Random NeuralNetwork, (2) For Pre-Trained NerualNetwork, (q) to quit\n")
        if(nn_type == "1"):
            nn = NeuralNetwork(16, 0.7, 0.9, 0.5)
        elif(nn_type == "2"):
            nn.load("nn1000.pk1")
        else:
            break
        game_type = raw_input("(1) For Random Opponent, (2) Human Player\n")
        if(game_type == "1"):
            print "Starting Computer vs Computer Games"
            for i in xrange(200):
                print i
                play0()
            print("Black Wins: {} White wins: {}").format(bWin, wWin)
            bwin = 0
            wwin = 0
        else:
            print "Starting User vs Computer Games"
            play1(True)


#===============================================================================
#Playing
#===============================================================================


def playVerbose():
    continue_play = False
    game = Othello()
    black_player = Player(nn, game, True)
    white_player = Player(None, game, False, "alphabeta")
    #white_player = Player(None, game, False, "greedy")
    while True:
        game.game_board.updateValidMoves()

        #if no valid moves, switch turns and check for winner
        if game.game_board.valid_moves == {}:
            if game.game_board.black_turn:
                print("Black cannot make any valid moves")
            else:
                print("White's cannot make any valid moves")
            game.game_board.switchTurns()
            #check for winner
            game.game_board.updateValidMoves()
            if game.game_board.valid_moves == {}:
                break

        #print score
        print("Black - {}\tWhite - {}").format(game.black_score, game.white_score)
        #print board
        print(game.game_board)

        #if coninuing play
        if continue_play:
            if game.game_board.black_turn:
                black_player.makeMove()
            else:
                white_player.makeMove()

        #if not coninuing play
        else:
            #print turn
            if game.game_board.black_turn:
                print("Black's Turn")
            else:
                print("White's Turn")

            rand = None
            #print valid moves
            if game.game_board.black_turn:
                print("Black's Turn")
                print("Valid Moves: {}").format(game.validMovesStringify())
                for k, v in black_player.getNNInputs().items():
                    print("{}: {}").format(game.validMoveStringify(k), nn.getValue(np.matrix(v)))

            else:
                print("White's Turn")
                # print("Valid Moves: {}").format(game.validMovesStringify())
                # rand = random.randrange(0, len(game.game_board.valid_moves.keys()))
                # print("Random index: {}").format(rand)
                print("Valid Moves: {}").format(game.validMovesStringify())
                for k, v in black_player.getNNInputs().items():
                    print("{}: {}").format(game.validMoveStringify(k), nn.getValue(np.matrix(v)))

            command = raw_input("n to next (default), c to play game, q to quit: ")
            if command == "n" or command == "":
                if game.game_board.black_turn:
                    black_player.makeMove()
                else:
                    white_player.makeMove(rand)
            elif command == "c":
                continue_play = True
                if game.game_board.black_turn:
                    black_player.makeMove()
                else:
                    white_player.makeMove(rand)
            elif command == "q":
                break
            else:
                print("not a valid command, try again")

            print("\n==========================================================\n")

    #Game Over
    print("Black - {}\tWhite - {}").format(game.black_score, game.white_score)
    print(game.game_board)

    #Check score
    if(game.black_score > game.white_score):
        print("Black Wins!")
    elif(game.black_score < game.white_score):
        print("White Wins!")
    elif(game.black_score == game.white_score):
        print("It's a tie!")


#plays game with two agents
def play0():
    global bWin, wWin, ties
    game = Othello()
    black_player = Player(nn, game, True)
    white_player = Player(None, game, False, "random")
    while True:
        game.game_board.updateValidMoves()

        #if no valid moves, switch turns and check for winner
        if game.game_board.valid_moves == {}:
            # if game.game_board.black_turn:
            #     print("Black cannot make any valid moves")
            # else:
            #     print("White's cannot make any valid moves")
            game.game_board.switchTurns()
            #check for winner
            game.game_board.updateValidMoves()
            if game.game_board.valid_moves == {}:
                break

        #print score
        #print("Black - {}\tWhite - {}").format(game.black_score, game.white_score)
        #print board
        #print(game.game_board)


        #print turn
        if game.game_board.black_turn:
            #print("Black's Turn")
            black_player.makeMove()
        else:
            #print("White's Turn")
            white_player.makeMove()

        #print("\n==========================================================\n")

    #Game Over
    # print("Black - {}\tWhite - {}").format(game.black_score, game.white_score)
    # print(game.game_board)

    #Check score
    if(game.black_score > game.white_score):
        bWin +=1
        # print("Black Wins!")
    elif(game.black_score < game.white_score):
        wWin +=1
        # print("White Wins!")
    elif(game.black_score == game.white_score):
        ties+=1
        # print("It's a tie!")

#plays game with one user, one agent
def play1(player_black):
    game = Othello()
    agent = Player(nn, game, not player_black, "alphabeta")
    while True:
        game.game_board.updateValidMoves()

        #if no valid moves, switch turns and check for winner
        if game.game_board.valid_moves == {}:
            if game.game_board.black_turn:
                print("Black cannot make any valid moves")
            else:
                print("White's cannot make any valid moves")
            game.game_board.switchTurns()
            #check for winner
            game.game_board.updateValidMoves()
            if game.game_board.valid_moves == {}:
                break

        #print score
        print("Black - {}\tWhite - {}").format(game.black_score, game.white_score)
        #print board
        print(game.game_board)


        #agent's turn
        if game.game_board.black_turn and not player_black:
            print("Black's Turn")
            agent.makeMove()
        elif not game.game_board.black_turn and player_black:
            print("White's Turn")
            agent.makeMove()

        #player's turn
        else:
            if player_black:
                print("Black's Turn")
            else:
                print("White's Turn")
            #Print valid moves
            print("Valid Moves: {}").format(game.validMovesStringify())

            #Get move input
            move = raw_input("Choose move (q to quit): ")

            #validate input
            is_valid_move = game.validateMoveInput(move)

            if is_valid_move:
                if move == "q" :
                    break
                else:
                    move = game.moveToCoords(move)
                    game.setTile(move[0], move[1])

        print("\n==========================================================\n")

    #Game Over
    print("Black - {}\tWhite - {}").format(game.black_score, game.white_score)
    print(game.game_board)

    #Check score
    if(game.black_score > game.white_score):
        print("Black Wins!")
    elif(game.black_score < game.white_score):
        print("White Wins!")
    elif(game.black_score == game.white_score):
        print("It's a tie!")

#plays game with two users
def play2():
    game = Othello()
    while True:
        game.game_board.updateValidMoves()

        #if no valid moves, switch turns and check for winner
        if game.game_board.valid_moves == {}:
            if game.game_board.black_turn:
                print("Black cannot make any valid moves")
            else:
                print("White's cannot make any valid moves")
            game.game_board.switchTurns()
            #check for winner
            game.game_board.updateValidMoves()
            if game.game_board.valid_moves == {}:
                break

        #print score
        print("Black - {}\tWhite - {}").format(game.black_score, game.white_score)
        #print board
        print(game.game_board)


        #print turn
        if game.game_board.black_turn:
            print("Black's Turn")
        else:
            print("White's Turn")

        #Print valid moves
        print("Valid Moves: {}").format(game.validMovesStringify())

        #Get move input
        move = raw_input("Choose move (q to quit): ")

        #validate input
        is_valid_move = game.validateMoveInput(move)

        if is_valid_move:
            if move == "q" :
                break
            else:
                move = game.moveToCoords(move)
                game.setTile(move[0], move[1])

        print("\n==========================================================\n")

    #Game Over
    print("Black - {}\tWhite - {}").format(game.black_score, game.white_score)
    print(game.game_board)

    #Check score
    if(game.black_score > game.white_score):
        print("Black Wins!")
    elif(game.black_score < game.white_score):
        print("White Wins!")
    elif(game.black_score == game.white_score):
        print("It's a tie!")


if __name__ == "__main__":
    main()
