"""Neural Network for TD-Othello"""

import numpy as np
from Othello import Othello
from Player import Player
import pickle, sys

inputUnits = 64
class NeuralNetwork(object):

    """Initialize neural Network Parameters"""
    def __init__(self, numHidLayers, gamma, ld, learningRate):
        self.wMatrix1 = np.random.randn(inputUnits, numHidLayers) / np.sqrt(inputUnits) # Weight Matrix at the Heart of the Neural Network
        self.eMatrix1 = np.zeros((inputUnits, numHidLayers)) # eligility traces for each of the inputs of our Weight Matrix
        self.wMatrix2 = np.random.randn(numHidLayers, 1) / np.sqrt(numHidLayers) # Weight Matrix at the Heart of the Neural Network
        self.eMatrix2 = np.zeros((numHidLayers, 1)) # eligility traces for each of the inputs of our Weight Matrix
        self.learningRate = learningRate
        self.numHidLayers = numHidLayers
        self.gamma = gamma #gamma used in calculating reward return
        self.ld = ld #used to determine how much you rely on pass
        self.bwin = 0
        self.wwin = 0

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
        stateVec.transpose()
        return np.dot(stateVec, self.wMatrix1)

    def calcOutputSum(self, hiddenVec):
        return np.dot(hiddenVec, self.wMatrix2)

    def calcGradientMatrix2(self, stateVec):
        hiddenSum = self.calcHiddenSum(stateVec)
        hiddenVec = self.sigmoid(hiddenSum)
        outputSum = self.calcOutputSum(hiddenVec)
        #outputValue = self.sigmoid(outputSum)
        outputDelta = self.sigmoid_prime(outputSum)

        gradMatrix = np.zeros((1, self.numHidLayers))
        for i, v in np.ndenumerate(gradMatrix):
            gradMatrix[i] = outputDelta * hiddenVec[i]


        return gradMatrix

    def calcGradientMatrix1(self, stateVec):
        hiddenSum = self.calcHiddenSum(stateVec)
        #print("hidden sum: {}").format(hiddenSum[0,0])
        #print(self.sigmoid_prime(hiddenSum[0,0]))
        hiddenDeltas = np.zeros((1, self.numHidLayers))
        for i, v in np.ndenumerate(hiddenDeltas):
            hiddenDeltas[i] = self.sigmoid_prime(hiddenSum[i])

        # print("hidden deltas: {}").format(hiddenDeltas)
        # print(self.wMatrix1.shape)
        # print(hiddenDeltas.shape)

        gradMatrix = np.zeros((inputUnits, self.numHidLayers))

        for i, v in np.ndenumerate(gradMatrix):
            gradMatrix[i] = stateVec.transpose()[i[0], 0] * hiddenDeltas[0,i[1]]

        return gradMatrix












    # def getValuePrime2(self, stateVec):
    #     J = numdifftools.Jacobian(lambda z: getValue(z.reshape(stateVec.shape), B, C).ravel())
    # return J(A.ravel()).reshape(A.shape)
    # def getValuePrime1(self):
    #     pass

    """Save our weight matrix into a loadable files, prevents retraining"""
    def save(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self.wMatrix1, f)

    """Load our Weight Matrix into out layer variable"""
    def load(self, filename):
        with open(filename, "rb") as f:
            self.wMatrix1 = pickle.load(f)

    """ Determines how much of a reward to apply """
    def delta(self, pstateValue, reward, stateValue):
        # Core Error Calculation, returns the reward of the current state
        #print(pstateValue)
        return (reward + (self.gamma * stateValue) - pstateValue)

    """Single Timestep in the reinforcement Learning"""
    def train(self, pstate, reward, state):
        pstateValue = self.getValue(pstate)
        cstateValue = self.getValue(state)

        #not sure about the partial derivative
        # print(self.eMatrix2)
        # print(self.eMatrix2.shape)
        #test = np.array([pstateValue]*self.eMatrix2.shape[0]).T
        # print(test)
        gradientMatrix2 = self.calcGradientMatrix2(pstate)
        #print(gradientMatrix2)
        gradientMatrix1 = self.calcGradientMatrix1(pstate)

        # print(self.gamma)
        # print(self.ld)
        # print()


        self.eMatrix2 = self.gamma * self.ld * self.eMatrix2 + gradientMatrix2.transpose()
        self.eMatrix1 = self.gamma * self.ld * self.eMatrix1 + gradientMatrix1
        delta = self.delta(pstateValue, 0, cstateValue)

        #print(self.wMatrix2)

        self.wMatrix2 +=  np.multiply((self.learningRate * delta), self.eMatrix2)
        self.wMatrix1 +=  np.multiply((self.learningRate * delta), self.eMatrix1)

        #print(self.wMatrix2)

        #print("W1: {}").format(self.wMatrix1)
        #print("W2: {}").format(self.wMatrix2)
    """Basic structure of our lean iteration function, going to be implemented elsewhere"""
    #This can actually be moved to the play class.
    def learn(self, num_episode = 300):
        for i in xrange(num_episode):
            game = Othello()
            black_player = Player(self, game, True)
            white_player = Player(self, game, False)
            while True:
                game.game_board.updateValidMoves()

                #if no valid moves, switch turns and check for winner
                if game.game_board.valid_moves == {}:
                    game.game_board.switchTurns()
                    #check for winner
                    game.game_board.updateValidMoves()
                    if game.game_board.valid_moves == {}:
                        break
                #print turn
                if game.game_board.black_turn:
                    #print("Black's Turn")
                    pstateVector = black_player.getBoardVector()
                    black_player.makeMove()
                    cstateVector = black_player.getBoardVector()
                    self.train(pstateVector, 0, cstateVector) #need to check that this is done by reference
                else:
                    #print("White's Turn")
                    pstateVector = white_player.getBoardVector()
                    white_player.makeMove()
                    pstateVector = white_player.getBoardVector()
                    self.train(pstateVector, 0, cstateVector) #need to check that this is done by reference

            if(game.black_score > game.white_score):
                #game is over, update matrix and reset elegibility matrix
                self.bwin += 1
                self.train(pstateVector, 1, cstateVector)
                self.reset()

            elif(game.black_score < game.white_score):
                #game is over, update matrix and reset elegibility matrix
                self.wwin += 1
                self.train(pstateVector, 0, cstateVector)
                self.reset()

            elif(game.black_score == game.white_score):
                #game is over, update matrix and reset elegibility matrix
                self.train(pstateVector, 0, cstateVector)
                self.reset()




    def reset(self):
        self.eMatrix1 = np.zeros((inputUnits, 1))
        self.eMatrix2 = np.zeros((self.numHidLayers, 1))


if __name__ == "__main__":
    main()
