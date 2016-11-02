"""Neural Network for TD-Othello"""

import numpy as np
from Othello import Othello
from Player import Player
import pickle

class NeuralNetwork(object):

    """Initialize neural Network Parameters"""
    def __init__(self, numHidLayers, gamma, ld, learningRate):
        self.wMatrix1 = np.random.randn(64, numHidLayers) / np.sqrt(64) # Weight Matrix at the Heart of the Neural Network
        self.eMatrix1 = np.zeros((64, numHidLayers)) # eligility traces for each of the inputs of our Weight Matrix
        self.wMatrix2 = np.random.randn(numHidLayers, 1) / np.sqrt(numHidLayers) # Weight Matrix at the Heart of the Neural Network
        self.eMatrix2 = np.zeros((numHidLayers, 1)) # eligility traces for each of the inputs of our Weight Matrix
        self.learningRate = learningRate
        self.numHidLayers = numHidLayers
        self.gamma = gamma #gamma used in calculating reward return
        self.ld = ld #used to determine how much you rely on pass
        self.bwin = 0
        self.wwin = 0

    def getValue(self, stateVec):
        stateVec.transpose()
        hiddenOutput = np.dot(stateVec, self.wMatrix1)
        outputValue = np.dot(hiddenOutput, self.wMatrix2)
        return outputValue

    def getHidSum(self, stateVec):
        stateVec.transpose()
        hidSum = np.dot(stateVec, self.wMatrix1)
        return hidSum

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
        return (reward + (self.gamma * stateValue) - pstateValue)

    """Single Timestep in the reinforcement Learning"""
    def train(self, pstate, reward, state):
        pstateValue = self.getValue(pstate)
        cstateValue = self.getValue(state)

        delta = self.delta(pstate, reward, state)

        #hidSum = self.getHidSum(state);
        #hide = self.sigmoid(hidSum)
        pstateMatrix = np.matrix(np.repeat(pstate.T, 10, axis = 1))

        self.eMatrix1 = pstateMatrix
      	self.eMatrix2 = np.matrix(np.random.randn(10, 1) / np.sqrt(100))
        #self.eMatrix1 = self.ld * self.eMatrix1 + ((1 - nextStateVal) * nextStateVal * (1 - hide) * hide)

        print(self.eMatrix2.shape)
        print(self.wMatrix2.shape)
        print(self.eMatrix1.shape)
        print(self.wMatrix1.shape)
        self.wMatrix2 +=  self.learningRate * delta * self.eMatrix2
        self.wMatrix1 +=  self.learningRate * delta * self.eMatrix1
        #self.eMatrix1 *= (self.gamma * self.ld)
        #self.eMatrix2 *= (self.gamma * self.ld)

    """Basic structure of our lean iteration function, going to be implemented elsewhere"""
    #This can actually be moved to the play class.
    def learn(self, num_episode = 100):
        game = Othello()
        black_player = Player(self, game, True)
        white_player = Player(self, game, False)
        for i in range(num_episode):
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


    def sigmoid(self, x):
        return 1/ 1 + np.exp(-x);

    def reset(self):
        self.eMatrix1 = np.zeros((64, 1))
        self.eMatrix2 = np.zeros((self.numHidLayers, 1))


if __name__ == "__main__":
    main()
