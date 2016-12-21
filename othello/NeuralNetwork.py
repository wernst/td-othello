"""Neural Network for TD-Othello"""

import numpy as np
np.set_printoptions(threshold='nan', precision=5)
from Othello import Othello
from Player import Player
import pickle, sys, time, os

inputUnits = 64

class NeuralNetwork(object):

    """Initialize neural Network Parameters"""
    def __init__(self, numHidLayers, gamma, ld, learningRate):
        self.wMatrix1 = np.random.uniform(-0.5, 0.5, (inputUnits, numHidLayers)) #weight matrix from input to hidden layer
        self.eMatrix1 = np.zeros((inputUnits, numHidLayers)) # eligility traces from hidden to input layer
        self.wMatrix2 = np.random.uniform(-0.5, 0.5,(numHidLayers, 1)) #weight matrix from hidden to output layer
        self.eMatrix2 = np.zeros((numHidLayers, 1)) # eligility traces from hidden to input layer
        self.learningRate = learningRate
        self.numHidLayers = numHidLayers #number of hidden units in the hidden layer
        self.gamma = gamma
        self.ld = ld #lambda
        self.bwin = 0
        self.wwin = 0
        self.iteration = 0
        self.total_iterations = None


    def sigmoid(self, x):
        return 1/(1+np.exp(-1*x))


    def sigmoid_prime(self, x):
        return self.sigmoid(x)*(1-self.sigmoid(x))

    def setTotal(self, total):
        self.total_iterations = total


    def getValue(self, stateVec):
        z2 = self.calcHiddenSum(stateVec)
        a2 = self.sigmoid(z2)
        z3 = self.calcOutputSum(a2)
        outputValue = self.sigmoid(z3)

        return outputValue


    def calcHiddenSum(self, stateVec):
        return np.dot(stateVec, self.wMatrix1)


    def calcOutputSum(self, hiddenVec):
        return np.dot(hiddenVec, self.wMatrix2)

    def calcGradientMatrix2(self, stateVec):
        hiddenSum = self.calcHiddenSum(stateVec)
        hiddenVec = self.sigmoid(hiddenSum)
        outputSum = self.calcOutputSum(hiddenVec)
        outputDelta = self.sigmoid_prime(outputSum)

        gradMatrix = outputDelta * hiddenVec



        return gradMatrix.T

    def calcGradientMatrix1(self, stateVec):
        hiddenSum = self.calcHiddenSum(stateVec)
        hiddenVec = self.sigmoid(hiddenSum)
        outputSum = self.calcOutputSum(hiddenVec)
        outputDelta = self.sigmoid_prime(outputSum)


        hiddenVecPrime = np.empty([1, self.numHidLayers])
        for index, value in np.ndenumerate(hiddenSum):
            hiddenVecPrime[index] = self.sigmoid_prime(value)

        deltaMatrix = np.empty([1, self.numHidLayers])
        for index, value in np.ndenumerate(hiddenVecPrime):
            deltaMatrix[index] = outputDelta[0,0] * self.wMatrix2.T[index] * value

        gradMatrix = ((stateVec.T)*deltaMatrix)


        return gradMatrix




    """Save our weight matrix into a loadable files, prevents retraining"""
    def save(self, filename, p_type, op_type, ld_val):
        pathToFile = "../" + p_type + "/" + str(ld_val) + "/" + op_type + "/NetworkFiles"
        if not os.path.exists(pathToFile):
            os.makedirs(pathToFile)
        filePath = pathToFile + "/" + filename
        with open(filePath, "wb") as f:
            pickle.dump(self, f)

    """Save our weight matrix into a loadable files, prevents retraining"""
    def save_simple(self, filename, dirname):
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        filePath = dirname + "/" + filename
        with open(filePath, "wb") as f:
            pickle.dump(self, f)


    """Load our Weight Matrix into out layer variable"""
    def load(self, filename, p_type, op_type, ld_val):
        pathToFile = "../" + p_type + "/" + str(ld_val) + "/" + op_type + "/NetworkFiles"
        if not os.path.exists(pathToFile):
            print("No such file or directory")
        #print(filename)
        filePath = pathToFile + "/" + filename
        with open(filePath, "rb") as f:
            # print(self.wMatrix1)
            # print("-------------")
            nn = pickle.load(f)
            self.wMatrix1 = nn.wMatrix1
            self.eMatrix1 = nn.eMatrix1
            self.wMatrix2 = nn.wMatrix2
            self.eMatrix2 = nn.eMatrix2
            self.learningRate = nn.learningRate
            self.numHidLayers = nn.numHidLayers
            self.gamma = nn.gamma
            self.ld = nn.ld

    """Load our Weight Matrix into out layer variable"""
    def load_simple(self, filename, dirname):
        if not os.path.exists(dirname):
            print("No such file or directory")
        #print(filename)
        filePath = dirname + "/" + filename
        with open(filePath, "rb") as f:
            # print(self.wMatrix1)
            # print("-------------")
            nn = pickle.load(f)
            self.wMatrix1 = nn.wMatrix1
            self.eMatrix1 = nn.eMatrix1
            self.wMatrix2 = nn.wMatrix2
            self.eMatrix2 = nn.eMatrix2
            self.learningRate = nn.learningRate
            self.numHidLayers = nn.numHidLayers
            self.gamma = nn.gamma
            self.ld = nn.ld

    """ Determines how much of a reward to apply """
    def delta(self, pValue, reward, cValue, game_over):
        if not game_over:
            return (reward + (self.gamma * cValue) - pValue)
        else:
            return reward - pValue

    """Single Timestep in the reinforcement Learning"""

    def train(self, pstate, reward, state, game_over):
        pstateValue = self.getValue(pstate)
        cstateValue = self.getValue(state)

        gradientMatrix2 = self.calcGradientMatrix2(state)

        gradientMatrix1 = self.calcGradientMatrix1(state)


        self.eMatrix2 = self.gamma * self.ld * self.eMatrix2 + gradientMatrix2
        self.eMatrix1 = self.gamma * self.ld * self.eMatrix1 + gradientMatrix1



        delta = self.delta(pstateValue, reward, cstateValue, game_over)

        self.wMatrix2 +=  np.multiply((self.learningRate * delta), self.eMatrix2)
        self.wMatrix1 +=  np.multiply((self.learningRate * delta), self.eMatrix1)

    """Basic structure of our lean iteration function, going to be implemented elsewhere"""
    #This can actually be moved to the play class.
    def learn(self, num_episode, p_type, op_type, ld_val):
        for i in xrange(num_episode):
            #print(i)
            game = Othello()
            black_player = Player(self, game, True, p_type)
            white_player = Player(self, game, False, op_type)

            game.game_board.updateValidMoves()
            print("{}: {} vs. {}, lambda - {}:").format(self.iteration, p_type, op_type, ld_val)
            print("Valid Moves: {}").format(game.validMovesStringify())
            for k, v in black_player.getNNInputs().items():
            	print("{}: {}").format(game.validMoveStringify(k), self.getValue(np.matrix(v)))
            print("")

            while True:
                #print turn
                if game.game_board.black_turn:
                    #print("Black's Turn")
                    pstateVector = black_player.getBoardVector()
                    black_player.makeMove()
                    cstateVector = black_player.getBoardVector()

                else:
                    #print("White's Turn")
                    pstateVector = white_player.getBoardVector()
                    white_player.makeMove()
                    cstateVector = white_player.getBoardVector()

                if game.isGameOver():
                    break
                else:
                    self.train(pstateVector, 0, cstateVector, False)




            if(game.black_score > game.white_score):
                #game is over, update matrix and reset elegibility matrix
                self.bwin += 1
                self.train(pstateVector, 1, cstateVector, True)
                self.reset()
                # print("black wins\n")

            elif(game.black_score < game.white_score):
                #game is over, update matrix and reset elegibility matrix
                self.wwin += 1
                self.train(pstateVector, 0, cstateVector, True)
                self.reset()
                # print("white wins\n")


            elif(game.black_score == game.white_score):
                #game is over, update matrix and reset elegibility matrix
                self.train(pstateVector, 0.5, cstateVector, True)
                self.reset()
                # print("tie\n")

            self.iteration+=1
        print("{}: {} vs. {}, lambda - {}:").format(self.iteration, p_type, op_type, self.ld)
        print("black wins: {}").format(self.bwin)
        print("white wins: {}\n").format(self.wwin)
    def reset(self):
        self.eMatrix2 = np.zeros((self.numHidLayers, 1))
        self.eMatrix1 = np.zeros((inputUnits, self.numHidLayers))
