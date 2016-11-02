import string, copy

import string, copy, random


class Player(object):
    def __init__(self, nn, game, is_black, player_type = "nn"):
        self.nn = nn
        self.game = game
        self.is_black = is_black
        self.type = player_type

    def makeMove(self):
        nn_inputs = self.getNNInputs()

        if self.type == "random":
            rand = random.randrange(0, len(nn_inputs.keys()))
            if self.is_black:
                max_key = nn_inputs.keys()[rand]
                max_val = -1000
                self.game.setTile(*max_key)

            else:
                min_key = nn_inputs.keys()[rand]
                min_val = 1000
                self.game.setTile(*min_key)


        elif self.type == "greedy":
            if self.is_black:
                best_move = self.calcMaxScore(nn_inputs)
                self.game.setTile(*best_move)

            else:
                best_move = self.calcMaxScore(nn_inputs)
                self.game.setTile(*best_move)


        elif self.type == "nn":
            nn_inputs = self.getNNInputs()

            if self.is_black:
                max_key = nn_inputs.keys()[0]
                max_val = -1000
                for coord in nn_inputs.keys():
                    nn_output = self.nn.getValue(nn_inputs[coord])
                    if nn_output > max_val:
                        max_key = coord
                        max_val = nn_output
                self.game.setTile(*max_key)

            else:
                min_key = nn_inputs.keys()[0]
                min_val = 1000
                for coord in nn_inputs.keys():
                    nn_output = self.nn.getValue(nn_inputs[coord])
                    if nn_output < min_val:
                        min_key = coord
                        min_val = nn_output
                self.game.setTile(*min_key)


    def calcMaxScore(self, possible_states):
        max_score = 0
        best_move = (None, None)
        for coord in possible_states.keys():
            board_copy = copy.deepcopy(self.game.game_board)
            points = board_copy.addTile(coord[0], coord[1])
            if points > max_score:
                max_score = points
                best_move = coord

        return best_move



    def getNNInputs(self):
        nn_inputs = {}
        for coord in self.game.game_board.valid_moves.keys():
            board_copy = copy.deepcopy(self.game.game_board)
            board_copy.addTile(coord[0], coord[1])
            board_vector = board_copy.boardToVector()
            nn_inputs[coord] = board_vector
        return nn_inputs

     # Simple function to return the board vector, to make training easier
    def getBoardVector(self):
        board_copy = copy.deepcopy(self.game.game_board)
        board_vector = board_copy.boardToVector()
        return board_vector
