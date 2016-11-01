"""Neural Network for TD-Othello"""

import numpy as np
import pickle


class NeuralNetwork(object):

    """Initialize neural Network Parameters"""
    def __init__(self, numHidLayers, gamma, ld, learningRate):
        self.wMatrix1 = np.random.randn(64, numHidLayers) / np.sqrt(64) # Weight Matrix at the Heart of the Neural Network
        self.eMatrix1 = np.zeros((64, 1)) # eligility traces for each of the inputs of our Weight Matrix
        self.wMatrix2 = np.random.randn(numHidLayers, 1) / np.sqrt(numHidLayers) # Weight Matrix at the Heart of the Neural Network
        self.eMatrix2 = np.zeros((numHidLayers, 1)) # eligility traces for each of the inputs of our Weight Matrix
        self.learningRate = learningRate
        self.numHidLayers = numHidLayers
        self.gamma = gamma #gamma used in calculating reward return
        self.ld = ld #used to determine how much you rely on pass

    def getValue(self, stateVec, wMatrix1cpy, wMatrix2cpy):
        stateVec.transpose()
        hiddenOutput = np.dot(stateVec, wMatrix1cpy)
        outputValue = np.dot(hiddenOutput, wMatrix2cpy)
        return outputValue

    def getHidSum(self, wMatrix1cpy, stateVec):
        stateVec.transpose()
        hidSum = np.dot(stateVec, wMatrix1cpy)
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
    def delta(self, pstateValue, reward, stateValue, wMatrix1cp, wMatrix2cp ):
        # Core Error Calculation, returns the reward of the current state
        return (self.gamma * stateValue - pstateValue)

    """Single Timestep in the reinforcement Learning"""
    def train(self, wMatrix1cp, wMatrix2cp, pstate, reward, state):
        pstateValue = self.getValue(pstate, wMatrix1cp, wMatrix2cp)
        cstateValue = self.getValue(state, wMatrix1cp, wMatrix2cp)

        delta = self.delta(pstate, reward, state, wMatrix1cp, wMatrix2cp)

        hidSum = self.getHidSum(wMatrix1cp, state);
        hide = self.sigmoid(hidSum)
        for i in range(64):
            if pstate[0, i] == 1:
                self.eMatrix1[i, 0] += 1
            elif pstate[0, i] == -1:
                self.eMatrix1[i, 0] -=1
      	#self.eMatrix2 = self.ld * self.eMatrix2 + (1 - cstateValue) * cstateValue
        #self.eMatrix1 = self.ld * self.eMatrix1 + ((1 - nextStateVal) * nextStateVal * (1 - hide) * hide)

        wMatrix1cp += self.learningRate * delta * self.eMatrix1
        #wMatrix2cp += self.learningRate * delta * self.eMatrix2
        self.eMatrix1 *= (self.gamma * self.ld)

    """Basic structure of our lean iteration function, going to be implemented elsewhere"""
    # #This can actually be moved to the play class.
    # def learn(self, num_episode = 1000):
    #     #create a new NN with a set number of hidden layers, and variables.
    #     createCopies of the weight Matrix, and pass those in
    #     #Then iterate over games:
    #     for(i in range(num_episode)):
    #         self.reset()
    #         while(!game.isDone()):  #while game is not over
    #             for valid moves given the state and player
    #                 #calculate all new states, evaluate using NN, and store values
    #                 #If black pick the strongest move, if white pick the weakest
    #                 #call NN.train(wMatrix1 Copy, wMatrix2 Copy, state, reward = 0, newstate)
    #
    #         #when the game is done (ie: a player has won) set the values NN weight matrix equal to
    #         #the copies you were training, and keep going.

    def sigmoid(self, x):
        return 1/ 1 + np.exp(-x);

    def reset(self):
        self.eMatrix1 = np.zeros((64, 1))
        self.eMatrix2 = np.zeros((self.numHidLayers, 1))

def main():
    newNN = NeuralNetwork(10, 0.1, 0.9, 0.7)
    newVector = np.matrix(np.random.random_integers(-1, 1, 64))
    newVector2 = np.matrix(np.random.random_integers(-1, 1, 64))
    weightMatrix1cpy = newNN.wMatrix1
    weightMatrix2cpy = newNN.wMatrix2
    newNN.train(weightMatrix1cpy, weightMatrix2cpy, newVector, 0, newVector2)




if __name__ == "__main__":
    main()
