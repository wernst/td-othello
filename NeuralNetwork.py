"""Neural Network for TD-Othello"""

import numpy as np
np.set_printoptions(threshold='nan', precision=5)
from Othello import Othello
from Player import Player
import pickle, sys, os


inputUnits = 64
class NeuralNetwork(object):

    """Initialize neural Network Parameters"""
    def __init__(self, numHidLayers, gamma, ld, learningRate, startExplorationRate, totalIterations):
        self.wMatrix1 = np.random.uniform(-0.5, 0.5, (inputUnits, numHidLayers)).astype(np.float32) # Weight Matrix at the Heart of the Neural Network
        self.eMatrix1 = np.zeros((inputUnits, numHidLayers)).astype(np.float32) # eligility traces for each of the inputs of our Weight Matrix
        self.wMatrix2 = np.random.uniform(-0.5, 0.5,(numHidLayers, 1)).astype(np.float32) # Weight Matrix at the Heart of the Neural Network
        self.eMatrix2 = np.zeros((numHidLayers, 1)).astype(np.float32) # eligility traces for each of the inputs of our Weight Matrix
        self.learningRate = learningRate
        self.numHidLayers = numHidLayers
        self.gamma = gamma #gamma used in calculating reward return
        self.ld = ld #used to determine how much you rely on pass
        #Training info on wins
        self.bwin = 0
        self.wwin = 0
        #ExplorationRate & output variables
        self.startExplorationRate = startExplorationRate
        self.curExplorationRate = startExplorationRate
        self.totalIterations = totalIterations
        self.numIterations = 0

    def calcExplorationRate(self):
        return (self.startExplorationRate - (self.startExplorationRate)*(self.numIterations / self.totalIterations))


    def sigmoid(self, x):
        return 1/(1+np.exp(-1*x))

    def sigmoid_prime(self, x):
        return self.sigmoid(x)*(1-self.sigmoid(x))


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


    def calcGradientMatrix2_2(self, stateVec):
        hiddenSum = self.calcHiddenSum(stateVec)
        hiddenVec = self.sigmoid(hiddenSum)
        outputSum = self.calcOutputSum(hiddenVec)
        #outputValue = self.sigmoid(outputSum)
        outputDelta = self.sigmoid_prime(outputSum)

        gradMatrix = outputDelta * hiddenVec



        return gradMatrix.T


    def calcGradientMatrix1_2(self, stateVec):
        hiddenSum = self.calcHiddenSum(stateVec)
        hiddenVec = self.sigmoid(hiddenSum)
        outputSum = self.calcOutputSum(hiddenVec)
        #outputValue = self.sigmoid(outputSum)
        outputDelta = self.sigmoid_prime(outputSum)
        # print(outputDelta)
        # print(hiddenSum)
        # print(hiddenSum[0])


        hiddenVecPrime = np.empty([1, self.numHidLayers])
        for index, value in np.ndenumerate(hiddenSum):
            hiddenVecPrime[index] = self.sigmoid_prime(value)

        deltaMatrix = np.empty([1, self.numHidLayers])
        for index, value in np.ndenumerate(hiddenVecPrime):
            deltaMatrix[index] = outputDelta[0,0] * self.wMatrix2.T[index] * value

        gradMatrix = ((stateVec.T)*deltaMatrix)


        return gradMatrix



    """Save our weight matrix into a loadable files, prevents retraining"""
    def save(self, filename, p_type):
        if not os.path.exists(p_type):
            os.makedirs(p_type)
        filePath = p_type + "/" + filename
        with open(filePath, "wb") as f:
            pickle.dump(self, f)

    """Load our Weight Matrix into out layer variable"""
    def load(self, filename, p_type):
        if not os.path.exists(p_type):
            print("No such file or directory")
        filePath = p_type + "/" + filename
        with open(filePath, "rb") as f:
            # print(self.wMatrix1)
            # print("-------------")
            nn = pickle.load(f)
            self.wMatrix1 = nn.wMatrix1
            self.eMatrix1 = nn.eMatrix1
            self.wMatrix2 = nn.wMatrix2
            self.eMatrix2 = nn.eMatrix2
            self.numIterations = nn.numIterations
            self.totalIterations = nn.totalIterations
            self.curExplorationRate = nn.curExplorationRate
            self.startExplorationRate = nn.startExplorationRate

    """ Determines how much of a reward to apply """
    def delta(self, pValue, reward, cValue, game_over):
        # Core Error Calculation, returns the reward of the current state
        #print(pstateValue)
        if not game_over:
            return (reward + (self.gamma * cValue) - pValue)
        else:
            return reward - pValue

    """Single Timestep in the reinforcement Learning"""
    def train(self, pstate, reward, state, game_over):
        rewardMatrix = np.matrix([reward]*self.numHidLayers)
        pHiddenOutput = self.sigmoid(self.calcHiddenSum(pstate))
        cHiddenOutput = self.sigmoid(self.calcHiddenSum(state))
        pstateValue = self.getValue(pstate)
        cstateValue = self.getValue(state)

        gradientMatrix2 = self.calcGradientMatrix2_2(state)

        gradientMatrix1 = self.calcGradientMatrix1_2(state)

        self.eMatrix2 = self.gamma * self.ld * self.eMatrix2 + gradientMatrix2
        self.eMatrix1 = self.gamma * self.ld * self.eMatrix1 + gradientMatrix1



        delta = self.delta(pstateValue, reward, cstateValue, game_over)

        self.wMatrix2 +=  np.multiply((self.learningRate * delta), self.eMatrix2)
        self.wMatrix1 +=  np.multiply((self.learningRate * delta), self.eMatrix1)

        #print(self.wMatrix2)
        # print("W1: {}").format(self.wMatrix1)
        # print("W2: {}").format(self.wMatrix2)

    """Basic structure of our lean iteration function, going to be implemented elsewhere"""
    #This can actually be moved to the play class.
    def learn(self, num_episode = 1000, p_type = "nn"):
        for i in xrange(num_episode):
            #print(self.numIterations)
            game = Othello()
            black_player = Player(self, game, True, p_type)
            white_player = Player(self, game, False, p_type)

            game.game_board.updateValidMoves()
            # print("Valid Moves: {}").format(game.validMovesStringify())
            # for k, v in black_player.getNNInputs().items():
            #     print("{}: {}").format(game.validMoveStringify(k), self.getValue(np.matrix(v)))

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
                    self.numIterations += 1
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


        print("black wins: {}").format(self.bwin)
        print("white wins: {}").format(self.wwin)
    def reset(self):
        self.eMatrix2 = np.zeros((self.numHidLayers, 1))
        self.eMatrix1 = np.zeros((inputUnits, self.numHidLayers))


if __name__ == "__main__":
    main()
