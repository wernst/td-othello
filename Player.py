import string, copy, random, sys
import numpy as np


class Player(object):
    def __init__(self, nn, game, is_black, player_type = "nn"):
        self.nn = nn
        self.game = game
        self.is_black = is_black
        self.type = player_type

    def makeMove(self, index = None):
        nn_inputs = self.getNNInputs()

        if self.type == "human_cl":
            #Print valid moves
            print("Valid Moves: {}").format(self.game.validMovesStringify())
            move = raw_input("Choose move (q to quit): ")

            #validate input
            is_valid_move = self.game.validateMoveInput(move)

            if is_valid_move:
                if move == "q" :
                    self.game.quit()
                else:
                    move = self.game.moveToCoords(move)
                    self.game.setTile(move[0], move[1])

        elif self.type == "human_gui":
            pass
        elif self.type == "random":
            if index == None:
                rand = random.randrange(0, len(nn_inputs.keys()))
            else:
                rand = index
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

        elif self.type == "nn_random":
            nn_inputs = self.getNNInputs()

            if self.is_black:
                #generate random number
                #decider = int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
                decider = random.random()
                if(decider < .5):
                    rand = random.randrange(0, len(nn_inputs.keys()))
                    max_key = nn_inputs.keys()[rand]
                    self.game.setTile(*max_key)
                else:
                    max_key = None
                    max_val = -1000
                    for coord in nn_inputs.keys():
                        nn_output = self.nn.getValue(nn_inputs[coord])
                        if nn_output > max_val:
                            max_key = coord
                            max_val = nn_output
                    self.game.setTile(*max_key)

            else:
                #generate random number
                #decider = int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
                decider = random.random()
                if(decider < .5):
                    rand = random.randrange(0, len(nn_inputs.keys()))
                    min_key = nn_inputs.keys()[rand]
                    self.game.setTile(*min_key)
                else:
                    min_key = None
                    min_val = 1000
                    for coord in nn_inputs.keys():
                        nn_output = self.nn.getValue(nn_inputs[coord])
                        if nn_output < min_val:
                            min_key = coord
                            min_val = nn_output
                    self.game.setTile(*min_key)

        elif self.type == "nn_dec_random":
            nn_inputs = self.getNNInputs()
            initial_rand = 0.5
            curr_it = self.nn.iteration
            total_it = self.nn.total_iterations
            z = 10*(curr_it-total_it)/(float(total_it))
            threshold = (1-initial_rand)*np.exp(z)+initial_rand
            #print(threshold)
            if self.is_black:
                #generate random number

                decider = random.random()
                if(decider > threshold):
                    rand = random.randrange(0, len(nn_inputs.keys()))
                    max_key = nn_inputs.keys()[rand]
                    self.game.setTile(*max_key)
                else:
                    max_key = None
                    max_val = -1000
                    for coord in nn_inputs.keys():
                        nn_output = self.nn.getValue(nn_inputs[coord])
                        if nn_output > max_val:
                            max_key = coord
                            max_val = nn_output
                    self.game.setTile(*max_key)

            else:
                #generate random number
                #decider = int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
                decider = random.random()
                if(decider > threshold):
                    rand = random.randrange(0, len(nn_inputs.keys()))
                    min_key = nn_inputs.keys()[rand]
                    self.game.setTile(*min_key)
                else:
                    min_key = None
                    min_val = 1000
                    for coord in nn_inputs.keys():
                        nn_output = self.nn.getValue(nn_inputs[coord])
                        if nn_output < min_val:
                            min_key = coord
                            min_val = nn_output
                    self.game.setTile(*min_key)

        elif self.type == "pos_values":
            board_inputs = self.getNNInputs()
            board_values = [[100, -25, 10, 5, 5, 10, -25, 100],
                                [-25, -25, 2, 2, 2, 2, -25, -25],
                                [10, 2, 5, 1, 1, 5, 2, 10],
                                [5, 2, 1, 2, 2, 1, 2, 5],
                                [5, 2, 1, 2, 2, 1, 2, 5],
                                [10, 2, 5, 1, 1, 5, 2, 10],
                                [-25, -25, 2, 2, 2, 2, -25, -25],
                                [100, -25, 10, 5, 5, 10, -25, 100]]
            max_key = None
            max_value = -1000
            for coord in board_inputs.keys():
                if board_values[coord[0]][coord[1]] > max_value:
                    max_key = coord
                    max_value = board_values[coord[0]][coord[1]]
            self.game.setTile(*max_key)


        elif self.type == "nn":
            nn_inputs = self.getNNInputs()

            if self.is_black:
                max_key = None
                max_val = -1000
                for coord in nn_inputs.keys():
                    nn_output = self.nn.getValue(nn_inputs[coord])
                    if nn_output > max_val:
                        max_key = coord
                        max_val = nn_output
                self.game.setTile(*max_key)

            else:
                min_key = None
                min_val = 1000
                for coord in nn_inputs.keys():
                    nn_output = self.nn.getValue(nn_inputs[coord])
                    if nn_output < min_val:
                        min_key = coord
                        min_val = nn_output
                self.game.setTile(*min_key)

        elif self.type == "alphabeta":
            max_depth = 4
            game_copy = copy.deepcopy(self.game)
            move = None
            score, move = self.alphabeta(game_copy, 0, max_depth, -1000, 1000, move, self.is_black)
            self.game.setTile(*move)

    def alphabeta(self, game, depth, max_depth, alpha, beta, chosen_move, player):
        #base case
        if depth == max_depth:
            v = game.black_score
        else:
            game.game_board.updateValidMoves()
            moves_list = game.game_board.valid_moves
            #base case
            if (moves_list == {}):
                v = game.black_score
            else:
                mover_black = game.game_board.black_turn

                #alpha beta for max node
                if mover_black:
                    v = -1000
                    best_move = None
                    for move in moves_list.keys():

                        if best_move == None:
                            best_move = move

                        game_copy = copy.deepcopy(game)
                        game_copy.setTile(*move)
                        new_v, new_move = self.alphabeta(game_copy, depth+1, max_depth, alpha, beta, move, False)

                        #update if better move
                        if v < new_v:
                            v = new_v
                            best_move = move
                        alpha = max(alpha, v)

                        #check alpha beta condition
                        if beta <= alpha:
                            break
                    chosen_move = best_move

                #alpha beta for min node
                else:
                    v = 1000
                    best_move = None
                    for move in moves_list.keys():

                        if best_move == None:
                            best_move = move

                        game_copy = copy.deepcopy(game)
                        game_copy.setTile(*move)
                        new_v, new_move = self.alphabeta(game_copy, depth+1, max_depth, alpha, beta, move, True)

                        #update if better move
                        if v > new_v:
                            v = new_v
                            best_move = move
                        beta = min(beta, v)

                        #check alpha beta condition
                        if beta <= alpha:
                            break
                    chosen_move = best_move

        return v, chosen_move






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
