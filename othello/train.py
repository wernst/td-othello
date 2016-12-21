import multiprocessing as pool
from NeuralNetwork import NeuralNetwork
import sys, os

def main():
    pass

#===============================================================================
#Train
#===============================================================================

def train():
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

def plot():
    opponent_type = ["nn_random", "pos_values", "random"]
    opponent_type2 = ["nn_dec_random", "pos_values", "random"]
    learn_From = [9, 1]
    for lf in learn_From:
        plotLearning("nn_random", lf, opponent_type)
    for lf in learn_From:
        plotLearning("nn_dec_random", lf, opponent_type2)
    player_type = ["nn_random", "nn_dec_random"]
    agent_type = ["pos_values", "alphabeta"]
    ld_val = [9,1]
    for at in agent_type:
        for ld in ld_val:
            plotVSAgent(player_type, ld, at)

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

    nn = NeuralNetwork(50, 1.0, 0.9, 0.001)

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
#Learning
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

#trains neural network
def learn_and_save(nn, episodes, total, p_type, dirname):
    iterations = 0
    while(iterations < total):
        nn.learn(episodes, p_type)
        iterations += episodes
        nn_name = "nn" + str(iterations) + "-" + p_type + ".pkl"
        print(nn_name)
        nn.save(nn_name, dirname)

def calcResults(nn, iterations=500):
    global bWin, wWin, ties
    bWin, wWin, ties = 0, 0, 0
    for i in range(iterations):
        play0(nn, None)
    return bWin/(iterations*1.0)



if __name__ == "__main__":
    main()
