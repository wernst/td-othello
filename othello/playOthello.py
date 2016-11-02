"""Plays othello game"""

from Othello import Othello
from Player import Player


def main():
    n = 200
    bwins = 0
    wwins = 0
    ties = 0
    for i in xrange(n):
        output = play0()
        if output == 1:
            bwins+= 1
        elif output == -1:
            wwins += 1
        else:
            ties += 1
    print("black wins: {}").format(bwins)
    print("white wins: {}").format(wwins)
    print("Ties: {}").format(ties)

#plays game with two agents
def play0():
    game = Othello()
    black_player = Player("neural network goes here", game, True, "greedy")
    white_player = Player("neural network goes here", game, False, "random")
    while True:
        game.game_board.updateValidMoves()

        #if no valid moves, switch turns and check for winner
        if game.game_board.valid_moves == {}:
            # if game.game_board.black_turn:
            #     print("Black cannot make any valid moves")
            # else:
            #     print("White's cannot make any valid moves")
            game.game_board.switchTurns()
            #check for winner
            game.game_board.updateValidMoves()
            if game.game_board.valid_moves == {}:
                break

        #print score
        #print("Black - {}\tWhite - {}").format(game.black_score, game.white_score)
        #print board
        #print(game.game_board)


        #print turn
        if game.game_board.black_turn:
            # print("Black's Turn")
            black_player.makeMove()
        else:
            # print("White's Turn")
            white_player.makeMove()

        # print("\n==========================================================\n")

    #Game Over
    # print("Black - {}\tWhite - {}").format(game.black_score, game.white_score)
    # print(game.game_board)

    #Check score
    if(game.black_score > game.white_score):
        # print("Black Wins!")
        return 1
    elif(game.black_score < game.white_score):
        # print("White Wins!")
        return -1
    elif(game.black_score == game.white_score):
        # print("It's a tie!")
        return 0


#plays game with one user, one agent
def play1(player_black):
    game = Othello()
    agent = Player("neural network goes here", game, not player_black)
    while True:
        game.game_board.updateValidMoves()

        #if no valid moves, switch turns and check for winner
        if game.game_board.valid_moves == {}:
            if game.game_board.black_turn:
                print("Black cannot make any valid moves")
            else:
                print("White's cannot make any valid moves")
            game.game_board.switchTurns()
            #check for winner
            game.game_board.updateValidMoves()
            if game.game_board.valid_moves == {}:
                break

        #print score
        print("Black - {}\tWhite - {}").format(game.black_score, game.white_score)
        #print board
        print(game.game_board)


        #agent's turn
        if game.game_board.black_turn and not player_black:
            print("Black's Turn")
            agent.makeMove()
        elif not game.game_board.black_turn and player_black:
            print("White's Turn")
            agent.makeMove()

        #player's turn
        else:
            if player_black:
                print("Black's Turn")
            else:
                print("White's Turn")
            #Print valid moves
            print("Valid Moves: {}").format(game.validMovesStringify())

            #Get move input
            move = raw_input("Choose move (q to quit): ")

            #validate input
            is_valid_move = game.validateMoveInput(move)

            if is_valid_move:
                if move == "q" :
                    break
                else:
                    move = game.moveToCoords(move)
                    game.setTile(move[0], move[1])

        print("\n==========================================================\n")

    #Game Over
    print("Black - {}\tWhite - {}").format(game.black_score, game.white_score)
    print(game.game_board)

    #Check score
    if(game.black_score > game.white_score):
        print("Black Wins!")
    elif(game.black_score < game.white_score):
        print("White Wins!")
    elif(game.black_score == game.white_score):
        print("It's a tie!")

#plays game with two users
def play2():
    game = Othello()
    while True:
        game.game_board.updateValidMoves()

        #if no valid moves, switch turns and check for winner
        if game.game_board.valid_moves == {}:
            if game.game_board.black_turn:
                print("Black cannot make any valid moves")
            else:
                print("White's cannot make any valid moves")
            game.game_board.switchTurns()
            #check for winner
            game.game_board.updateValidMoves()
            if game.game_board.valid_moves == {}:
                break

        #print score
        print("Black - {}\tWhite - {}").format(game.black_score, game.white_score)
        #print board
        print(game.game_board)


        #print turn
        if game.game_board.black_turn:
            print("Black's Turn")
        else:
            print("White's Turn")

        #Print valid moves
        print("Valid Moves: {}").format(game.validMovesStringify())

        #Get move input
        move = raw_input("Choose move (q to quit): ")

        #validate input
        is_valid_move = game.validateMoveInput(move)

        if is_valid_move:
            if move == "q" :
                break
            else:
                move = game.moveToCoords(move)
                game.setTile(move[0], move[1])

        print("\n==========================================================\n")

    #Game Over
    print("Black - {}\tWhite - {}").format(game.black_score, game.white_score)
    print(game.game_board)

    #Check score
    if(game.black_score > game.white_score):
        print("Black Wins!")
    elif(game.black_score < game.white_score):
        print("White Wins!")
    elif(game.black_score == game.white_score):
        print("It's a tie!")


if __name__ == "__main__":
    main()
