# TD-Othello README
## CS 701 Fall 2016 Seminar Project

######How to play:
    1. Load a neural network. These networks are loaded with the following inputs:
        - filename
        - training player
        - opponent training player
        - lambda value (9 for 0.9, 1 for 1.0)
    2. Choose a mode to play with:
        - play0: Plays a game with two computer players in the command line
        - play1: Plays a game with one computer player and one human player in the command line
        - play2: Plays a game with two human players in the command line
        - playGui: Plays a game with one computer player and one human player in a Tkinter GUI

######TD Lambda algorithm:
TD Lambda is a temporal difference learning algorithm designed by Richard Sutton. More info on the algorithm can be found in the paper in this repository or at this link: https://webdocs.cs.ualberta.ca/~sutton/papers/sutton-89.pdf

######Known bugs:
With lambda < 1, the output values of the neural network approach 1 for all board states at some point during training. Performance decreases when this occurs.
