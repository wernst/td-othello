import string, copy


class Player(object):
    def __init__(self, nn, game, is_black):
        self.nn = nn
        self.game = game
        self.is_black = is_black

    def makeMove(self):
        nn_inputs = self.getNNInputs()

        if self.is_black:
            max_key = nn_inputs.keys()[0]
            max_val = -1000
            # for coord, possible_move in nn_inputs.items():
            #     nn_output = 1
            #     if nn_output > max_val:
            #         max_key = coord
            #         max_val = nn_output
            self.game.setTile(*max_key)

        else:
            min_key = nn_inputs.keys()[0]
            min_val = 1000
            # for coord, possible_move in nn_inputs.items():
            #     nn_output = nn_output()
            #     if nn_output < min_val:
            #         min_key = coord
            #         min_val = nn_output
            self.game.setTile(*min_key)

    def getNNInputs(self):
        nn_inputs = {}
        for coord in self.game.game_board.valid_moves.keys():
            board_copy = copy.deepcopy(self.game.game_board)
            board_copy.addTile(coord[0], coord[1])
            board_vector = board_copy.boardToVector()
            nn_inputs[coord] = board_vector
        return nn_inputs
