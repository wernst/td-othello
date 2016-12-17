"""Plays othello game"""


from Othello import Othello
from Player import Player
from NeuralNetwork import NeuralNetwork
from Board import Board
import numpy as np
import random
import sys, os
import multiprocessing as pool
from gui import GameBoard
import Tkinter as tk
#sys.path.append("/anaconda/bin")

bWin = 0
wWin = 0
ties = 0


def main():
    #nn = NeuralNetwork2(50, 1.0, 0.9, 0.001)
    #nn2 = NeuralNetwork2(50, 1.0, 0.9, 0.0001)
    #test("nn_random", nn)
    #learn(nn, 50000, "nn_random", "nn_random-7")

    nn = NeuralNetwork(50, 1.0, 0.9, 0.001)
    nn2 = NeuralNetwork(50, 1.0, 1.0, 0.001)
    jobs = []
    player_type = ["nn_random"]
    player_type2 = ["nn_dec_random"]
    opponent_type = ["nn_random", "pos_values", "random"]
    opponent_type2 = ["nn_dec_random", "pos_values", "random"]
    learn_From = [9]
    learn_From2 = [1]
    learn_type = raw_input("Select learn type (1,2,3,4):")
    if int(learn_type) == 1:
        for pt in player_type:
            for op in opponent_type:
                for lf in learn_From:
                    p = pool.Process(target=learn, args=(nn, 5, pt , lf, op, 20))
                    jobs.append(p)
                    p.start()

        for j in jobs:
            j.join()

    elif int(learn_type) == 2:
        for pt in player_type:
            for op in opponent_type:
                for lf in learn_From2:
                    p = pool.Process(target=learn, args=(nn2, 5, pt , lf, op, 20))
                    jobs.append(p)
                    p.start()

        for j in jobs:
            j.join()

    elif int(learn_type) == 3:
        for pt in player_type2:
            for op in opponent_type2:
                for lf in learn_From:
                    p = pool.Process(target=learn, args=(nn, 5, pt , lf, op, 20))
                    jobs.append(p)
                    p.start()

        for j in jobs:
            j.join()

    elif int(learn_type) == 4:
        for pt in player_type2:
            for op in opponent_type2:
                for lf in learn_From2:
                    p = pool.Process(target=learn, args=(nn2, 5, pt , lf, op, 20))
                    jobs.append(p)
                    p.start()

        for j in jobs:
            j.join()

    #testBoardState(nn, "nn_random-1", "nn10000-nn_random.pk1")
    #runGameWithOutput(nn, "nn_random-1", "nn10000-nn_random.pk1")
def test(dirname, nn):
    for filename in os.listdir(dirname):
        nn.load(filename, "nn_random")
        print("{}:").format(filename)
        runGames(nn, 1000)
        print("\n")
#===============================================================================
#Testing
#===============================================================================

def learn2(nn, episodes, p_type, dirname):
    nn.setTotal(episodes)
    nn.learn(episodes, p_type)
    nn_name = "nn" + str(episodes) + "-" + p_type + ".pkl"
    nn.save(nn_name, dirname)

#trains neural network
def learn(nn, episodes, p_type, ld_val, op_type, total):
    iterations = 0
    nn.setTotal(total)
    while(iterations < total):
        pathToFiles = p_type + "/" + str(ld_val) + "/" + op_type
        if not os.path.exists(pathToFiles):
            os.makedirs(pathToFiles)
        #Calc Results
        resultsFile = p_type + "/" + str(ld_val) + "/" + op_type + "/results.txt"
        with open(resultsFile, 'a+') as f:
            f.write(str(iterations) + " " + str(calcResults(nn)) + "\n")

        nn.learn(episodes, p_type, op_type, ld_val)
        iterations += episodes
        nn_name = str(ld_val) + "-" + op_type + "_" + str(iterations) + ".pkl"
        nn.save(nn_name, p_type, op_type, ld_val)

def calcResults(nn, iterations=5):
    global bWin, wWin, ties
    bWin, wWin, ties = 0, 0, 0
    for i in range(iterations):
        play0(nn, None)
    return bWin/(iterations*1.0)

#trains neural network
def learn_and_save(nn, episodes, total, p_type, dirname):
    iterations = 0
    while(iterations < total):
        nn.learn(episodes, p_type)
        iterations += episodes
        nn_name = "nn" + str(iterations) + "-" + p_type + ".pkl"
        print(nn_name)
        nn.save(nn_name, dirname)

#runs a certain number of game iterations
def runGames(nn, nn_file, dirname, iterations):
    global bWin, wWin, ties
    bWin = 0
    wWin = 0
    ties = 0
    nn.load(nn_file, dirname)
    for i in xrange(iterations):
        #print(i)
        play0(nn, None)
    print("black wins: {}").format(bWin)
    print("white wins: {}").format(wWin)
    print("ties: {}").format(ties)
    print("\nwin pct: {}").format(bWin/(iterations*1.0))


def runGameWithOutput(nn, nn_file, dirname):
    nn.load2(dirname, nn_file)
    playVerbose(nn, None)

#Tests a board state (input inside the function)
def testBoardState(nn, dirname, nn_file):
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
    state4 = [[" ", " ", " ", "W", "B", " ", "B", "B"],
            [" ", " ", "B", "B", "B", "B", "B", "W"],
            [" ", " ", " ", "W", "B", "W", "B", "W"],
            [" ", " ", "B", "B", "B", "B", "B", "W"],
            [" ", " ", " ", "W", " ", "W", "B", " "],
            [" ", " ", " ", " ", "B", "B", "B", "W"],
            [" ", " ", " ", "W", " ", "W", "B", "W"],
            [" ", " ", " ", "W", "B", "W", "B", "W"]]
    state_init = [[" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", "W", "B", " ", " ", " ", " "],
            [" ", " ", " ", "W", "B", " ", " ", " "],
            [" ", " ", " ", "B", "W", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "]]
    board = Board(state_init)
    print(board)
    #print(nn.wMatrix1)
    #print("-------------")
    nn.load2(nn_file, dirname)
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
def playGui(nn_file=None):
    root = tk.Tk()
    #root.resizable(width = False, height = False)
    game = Othello()
    if nn_file != None:
        nn.load(nn_file)
    black_player = Player(nn, game, True, "human_gui")
    white_player = Player(nn, game, False, "nn")
    gui_board = GameBoard(root, game, black_player, white_player)
    gui_board.play()

def playVerbose(nn_black, nn_white):
    continue_play = False
    game = Othello()
    black_player = Player(nn_black, game, True)
    white_player = Player(nn_white, game, False, "pos_values")
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
                    print("{}: {}").format(game.validMoveStringify(k), black_player.nn.getValue(np.matrix(v)))

            else:
                print("White's Turn")
                # print("Valid Moves: {}").format(game.validMovesStringify())
                # rand = random.randrange(0, len(game.game_board.valid_moves.keys()))
                # print("Random index: {}").format(rand)
                print("Valid Moves: {}").format(game.validMovesStringify())
                for k, v in black_player.getNNInputs().items():
                    print("{}: {}").format(game.validMoveStringify(k), black_player.nn.getValue(np.matrix(v)))

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
def play0(nn_black, nn_white):
    global bWin, wWin, ties
    game = Othello()
    black_player = Player(nn_black, game, True)
    white_player = Player(nn_white, game, False, "random")
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
