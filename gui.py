import Tkinter as tk
import time

#code loosely based on answer to this stack overflow question http://stackoverflow.com/questions/4954395/create-board-game-like-grid-in-python

class GameBoard(tk.Frame):
    def __init__(self, parent, game, black_player, white_player, rows=8, columns=8, size=32):

        self.parent = parent
        self.game = game
        self.black_player = black_player
        self.white_player = white_player
        self.rows = rows
        self.columns = columns
        self.size = size

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)

        #create a canvas area to build board
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)
        self.canvas.bind("<Configure>", self.refreshBoardSize)
        self.canvas.bind("<Button-1>", self.clickMove)

        #create a menu area for buttons, score, messages, etc...
        self.menu_area = tk.Frame(self, borderwidth=0, highlightthickness=0,
                                width=100, height=100, background="bisque")
        self.menu_area.pack(side="bottom", fill="both", expand=True)

        self.quit_button = tk.Button(self.menu_area, text="Quit", command=self.quitGame)
        self.quit_button.pack(fill="both")

        self.reset_button = tk.Button(self.menu_area, text="Reset Game", command=self.resetGame)
        self.reset_button.pack(fill="both")

        self.score_label = tk.Label(self.menu_area, text="Black: 2, White: 2")
        self.score_label.pack()

        self.game_over_message = tk.Label(self.menu_area, text="")
        self.game_over_message.pack()


    """Callback for reset button"""
    def resetGame(self):
        self.game.start()
        self.game_over_message.config(text="")
        self.canvas.bind("<Button-1>", self.clickMove)


    """Callback for quit button"""
    def quitGame(self):
        self.game.game_over = True
        self.endGame()


    """Ends the game, players cannot move and the game over message appears"""
    def endGame(self):
        #self.canvas.unbind("<Configure>")
        self.canvas.unbind("<Button-1>")
        if(self.game.black_score > self.game.white_score):
            self.game_over_message.config(text = "Black Wins!")
        elif(self.game.black_score < self.game.white_score):
            self.game_over_message.config(text = "White Wins!")
        elif(self.game.black_score == self.game.white_score):
            self.game_over_message.config(text = "It's a tie!")


    """Normalizes the x,y window coords to a row, col board comination"""
    def normalizeCoords(self, row, col):
        return row/self.size, col/self.size


    """Event listener for human to place their move"""
    def clickMove(self, event):
        #If on board
        if event.x < (self.size*self.columns) and event.y < (self.size*self.rows):

            #normalize coords
            move = self.normalizeCoords(event.y, event.x)

            #move tile to selected spot
            self.game.setTile(move[0], move[1])
            board_arr = self.game.game_board.boardToVector().tolist()[0]

            #redraw board
            self.refreshBoard(board_arr)


    """Event listener for window size change"""
    def refreshBoardSize(self, event):
        board_arr = self.game.game_board.boardToVector().tolist()[0]

        #set square size as min(x,y)
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)

        #redraw board
        self.refreshBoard(board_arr)


    """Draws a board based on the input board array"""
    def refreshBoard(self, board_arr):
        self.canvas.delete("square")
        self.canvas.delete("piece")

        for i in range(len(board_arr)):
            row = i/8
            col = i%8
            x1 = ((col) * self.size)
            y1 = (row * self.size)
            x2 = x1 + self.size
            y2 = y1 + self.size

            #create board
            if (i/8, i%8) in self.game.game_board.valid_moves.keys():
                #board space with valid move
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="yellow", tags="square")
            else:
                #regular board space
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="lawn green", tags="square")

            #place pieces
            if board_arr[i] == 1:
                self.canvas.create_oval(x1, y1, x2, y2, outline="black", fill="black", tags="piece")
            elif board_arr[i] == -1:
                self.canvas.create_oval(x1, y1, x2, y2, outline="black", fill="white", tags="piece")

        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

        #update score
        self.score_label.config(text =("Black: " + str(self.game.black_score) + ", White: " + str(self.game.white_score)))


    """Play a game with the gui"""
    def play(self):
        self.pack(side="top", fill="both", expand="true", padx=4, pady=4)
        while True:
            if not self.game.game_over:
                self.game.isGameOver()
                if not self.game.game_over:
                    if self.game.game_board.black_turn:
                        self.black_player.makeMove()
                        board_arr = self.game.game_board.boardToVector().tolist()[0]

                        # if self.black_player.type.find("human") == -1:
                        #     time.sleep(2)
                        self.refreshBoard(board_arr)
                        self.game.isGameOver()
                    else:
                        self.white_player.makeMove()
                        board_arr = self.game.game_board.boardToVector().tolist()[0]
                        # if self.white_player.type.find("human") == -1:
                        #     time.sleep(2)
                        self.refreshBoard(board_arr)
                        self.game.isGameOver()
                else:
                    self.endGame()
            self.parent.update_idletasks()
            self.parent.update()
