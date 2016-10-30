"""Neural Network for TD-Othello"""

import numpy as np
import pickle


class NeuralNetwork:

    """Initialize neural Network Parameters"""
    def _init_(self, layerDims, gamma, ld, learningRate):
        self.wMatrix = [] # Weight Matrix at the Heart of the Neural Network
        self.eMarix = [] # eligility traces for each of the inputs of our Weight Matrix
        self.learningRate = learningRate
        self.wDims # Number of input, hidden and output layers
        self.gamma = gamma #gamma used in calculating reward return
        self.ld = ld #used to determine how much you rely on pas
        for i in range(len(wDims)-1): #Randomly initialize weights from 0,1 based on Gaussian Distribution
            self.layers.append(np.random.normal(0, 1, size=(wDims[i+1], wDims[i]+1)))
        self.eMatrix = np.zeros

    """Save our weight matrix into a loadable files, prevents retraining"""
    def save(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self.wMatrix, f)


    """Load our Weight Matrix into out layer variable"""
    def load(self, filename):
        with open(filename, "rb") as f:
            self.wMatrix = pickle.load(f)

    """ Determines how much of a reward to apply """
    def delta
    def softmax(x):
        e = np.exp(x)
        return e/np.sum(e)
