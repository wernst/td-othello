"""Plays othello game"""


from Othello import Othello
from Player import Player
from NeuralNetwork2 import NeuralNetwork2
from Board import Board
import numpy as np
import random
import sys, os
import multiprocessing as pool
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

#sys.path.append("/anaconda/bin")

bWin = 0
wWin = 0
ties = 0


def main():
    # opponent_type = ["nn_random", "pos_values", "random"]
    # opponent_type2 = ["nn_dec_random", "pos_values", "random"]
    # learn_From = [9, 1]
    # for lf in learn_From:
    #     plotLearning("nn_random", lf, opponent_type)
    # for lf in learn_From:
    #     plotLearning("nn_dec_random", lf, opponent_type2)
    player_type = ["nn_random", "nn_dec_random"]
    agent_type = ["pos_values", "alphabeta"]
    ld_val = [9,1]
    for at in agent_type:
        for ld in ld_val:
            plotVSAgent(player_type, ld, at)
#===============================================================================
#Train
#===============================================================================

def train():
    nn = NeuralNetwork2(50, 1.0, 0.9, 0.001)
    nn2 = NeuralNetwork2(50, 1.0, 1.0, 0.001)
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
                    p = pool.Process(target=learn, args=(nn, 1000, pt , lf, op, 125000))
                    jobs.append(p)
                    p.start()

        for j in jobs:
            j.join()

    elif int(learn_type) == 2:
        for pt in player_type:
            for op in opponent_type:
                for lf in learn_From2:
                    p = pool.Process(target=learn, args=(nn2, 1000, pt , lf, op, 125000))
                    jobs.append(p)
                    p.start()

        for j in jobs:
            j.join()

    elif int(learn_type) == 3:
        for pt in player_type2:
            for op in opponent_type2:
                for lf in learn_From:
                    p = pool.Process(target=learn, args=(nn, 1000, pt , lf, op, 125000))
                    jobs.append(p)
                    p.start()

        for j in jobs:
            j.join()

    elif int(learn_type) == 4:
        for pt in player_type2:
            for op in opponent_type2:
                for lf in learn_From2:
                    p = pool.Process(target=learn, args=(nn2, 1000, pt , lf, op, 125000))
                    jobs.append(p)
                    p.start()

        for j in jobs:
            j.join()

#===============================================================================
#Plotting
#===============================================================================

def plotLearning(p_type, ld_val, opponent_type):

    p_name = "NN-Fixed" if p_type == "nn_random" else "NN-Decreasing"
    ld_name = "0.9" if ld_val == 9 else "1.0"

    colours = ['red', 'cyan', 'magenta']
    markers = ['o', 'v', '*']

    minorLocatorX = AutoMinorLocator()
    minorLocatorY = AutoMinorLocator()
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    ax.xaxis.set_minor_locator(minorLocatorX)
    ax.yaxis.set_minor_locator(minorLocatorY)

    plt.tick_params(which='both', width=2)

    plt.xlabel('Number of Games Trained')
    plt.ylabel('Win Percentage vs. Random Agent (500 games)')
    plt.title('Performance of Learning for ' + p_name + " and Lambda: " + ld_name)
    pathToFile =  p_type + "/" + str(ld_val) + "/"

    for index, op_type in enumerate(opponent_type):
        resultsFile = p_type + "/" + str(ld_val) + "/" + op_type + "/" + "results.txt"
        numGames = []
        winPercentage  =[]
        with open(resultsFile, 'rt') as f:
            for line in f:
                results = line.split()
                numGames.append(int(results[0]))
                results[1].rstrip()
                winPercentage.append(float(results[1]) * 100.0)
                for i in range(1):
                    try:
                        next(f)
                    except:
                        break
        plt.plot(numGames, winPercentage, marker=markers[index], c=colours[index])
        plt.axis([0, 124000, 0, 100])
        plt.grid(which='major', color='k', linestyle='--', alpha=0.8)
        plt.grid(which='minor', color='b', alpha=0.5)

    p1 = plt.Rectangle((0, 0), 0.1, 0.1, fc=colours[0])
    p2 = plt.Rectangle((0, 0), 0.1, 0.1, fc=colours[1])
    p3 = plt.Rectangle((0, 0), 0.1, 0.1, fc=colours[2])
    plt.legend((p1, p2, p3), ('self', opponent_type[1], opponent_type[2]), loc='lower right')
    figureName = pathToFile +"{1}_LD-{1}.eps".format(p_name, ld_name)
    fig.savefig(figureName, format='eps')


def plotVSAgent(player_type, ld_val, agent_type):

    nn = NeuralNetwork2(50, 1.0, 0.9, 0.001)

    ld_name = "0.9" if ld_val == 9 else "1.0"

    colours = ['red', 'cyan']
    markers = ['o', 'v']

    minorLocatorX = AutoMinorLocator()
    minorLocatorY = AutoMinorLocator()

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)


    ax.xaxis.set_minor_locator(minorLocatorX)
    ax.yaxis.set_minor_locator(minorLocatorY)

    plt.tick_params(which='both', width=2)

    plt.xlabel('Number of Games Trained')
    plt.ylabel('Black Score vs '+ agent_type)
    plt.title('Performance of Self-Trained NN with Lambda: ' + ld_name + 'vs. ' + agent_type)
    pathToFile = agent_type + "/" + str(ld_val) + "/"

    if not os.path.exists(pathToFile):
        os.makedirs(pathToFile)

    for index, p_type in enumerate(player_type):
        numGames = []
        blackScore = []
        for iteration in range(1000, 126000, 4000):
            p_name = "NN-Fixed" if p_type == "nn_random" else "NN-Decreasing"
            nn_name = str(ld_val) + "-" + p_type + "_" + str(iteration) + ".pkl"

            try:
                nn.load(nn_name, p_type, p_type, ld_val)
            except:
                break

            blackScore.append(int(calcBlackScore(nn, agent_type)))
            numGames.append(iteration)
        plt.plot(numGames, blackScore, marker=markers[index], c=colours[index])
        plt.axis([0, 124000, 0, 64])
        plt.grid(which='major', color='k', linestyle='--', alpha=0.8)
        plt.grid(which='minor', color='b', alpha=0.5)

    p1 = plt.Rectangle((0, 0), 0.1, 0.1, fc=colours[0])
    p2 = plt.Rectangle((0, 0), 0.1, 0.1, fc=colours[1])
    plt.legend((p1, p2), (player_type[0], player_type[1]), loc='best')
    figureName = pathToFile +"{1}_LD-{1}.eps".format(agent_type, ld_name)
    fig.savefig(figureName, format='eps')



def calcBlackScore(nn, agent_type):
    global bWin, wWin, ties
    game = Othello()
    black_player = Player(nn, game, True)
    white_player = Player(None, game, False, agent_type)
    while True:
        game.game_board.updateValidMoves()

        if game.game_board.valid_moves == {}:
            game.game_board.switchTurns()
            #check for winner
            game.game_board.updateValidMoves()
            if game.game_board.valid_moves == {}:
                return game.black_score
        #print turn
        if game.game_board.black_turn:
            black_player.makeMove()
        else:
            white_player.makeMove()

    #Check score
    if(game.black_score > game.white_score):
        bWin +=1
    elif(game.black_score < game.white_score):
        wWin +=1
    elif(game.black_score == game.white_score):
        ties+=1




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

def calcResults(nn, iterations=500):
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
    nn.load(nn_file, dirname)
    playVerbose(nn, None)

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
