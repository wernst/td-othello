import Tkinter as tk
import time
class GameBoard(tk.Frame):
    def __init__(self, parent, game, black_player, white_player, rows=8, columns=8, size=32, color1="white", color2="blue"):
        '''size is the size of a square, in pixels'''

        self.parent = parent
        self.game = game
        self.black_player = black_player
        self.white_player = white_player
        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.pieces = {}

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)
        self.menu_area = tk.Frame(self, borderwidth=0, highlightthickness=0,
                                width=100, height=100, background="bisque")
        # label_1 = tk.Label(self.canvas, text="hey")
        # label_1.pack(side="right")
        self.menu_area.pack(side="bottom", fill="both", expand=True)
        self.quit_button = tk.Button(self.menu_area, text="Quit", command=self.quitGame)
        self.quit_button.pack(fill="both")
        self.reset_button = tk.Button(self.menu_area, text="Reset Game", command=self.resetGame)
        self.reset_button.pack(fill="both")
        self.score_label = tk.Label(self.menu_area, text="Black: 2, White: 2")
        self.score_label.pack()
        self.game_over_message = tk.Label(self.menu_area, text="")
        self.game_over_message.pack()


        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refreshBoardSize)
        self.canvas.bind("<Button-1>", self.clickMove)

    def resetGame(self):
        self.game.start()

    def quitGame(self):
        self.game.game_over = True
        #self.canvas.unbind("<Configure>")
        self.canvas.unbind("<Button-1>")
        if(self.game.black_score > self.game.white_score):
            self.game_over_message.config(text = "Black Wins!")
        elif(self.game.black_score < self.game.white_score):
            self.game_over_message.config(text = "White Wins!")
        elif(self.game.black_score == self.game.white_score):
            self.game_over_message.config(text = "It's a tie!")

    def normalizeCoords(self, row, col):
        return row/self.size, col/self.size

    def clickMove(self, event):
        if event.x < (self.size*self.columns) and event.y < (self.size*self.rows):
            move = self.normalizeCoords(event.y, event.x)
            print(move)
            self.game.setTile(move[0], move[1])
            print(event.x, event.y)
            board_arr = self.game.game_board.boardToVector().tolist()[0]
            self.refreshBoard(board_arr)


    def refreshBoardSize(self, event):
        board_arr = self.game.game_board.boardToVector().tolist()[0]
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.refreshBoard(board_arr)


    def refreshBoard(self, board_arr):
        self.canvas.delete("square")
        self.canvas.delete("piece")
        #self.game.game_board.updateValidMoves()
        for i in range(len(board_arr)):
            row = i/8
            col = i%8
            x1 = ((col) * self.size)
            y1 = (row * self.size)
            x2 = x1 + self.size
            y2 = y1 + self.size
            # color = "black" if board_arr[i] == 1 else "white" if board_arr[i] == -1 else "lawn green"
            # self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
            if (i/8, i%8) in self.game.game_board.valid_moves.keys():
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="yellow", tags="square")
            else:
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="lawn green", tags="square")
            if board_arr[i] == 1:
                self.canvas.create_oval(x1, y1, x2, y2, outline="black", fill="black", tags="piece")
            elif board_arr[i] == -1:
                self.canvas.create_oval(x1, y1, x2, y2, outline="black", fill="white", tags="piece")
        # for name in self.pieces:
        #     self.placepiece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")
        self.score_label.config(text =("Black: " + str(self.game.black_score) + ", White: " + str(self.game.white_score)))



    def play(self):
        self.pack(side="top", fill="both", expand="true", padx=4, pady=4)
        # self.parent.mainloop()
        while True:
            if not self.game.game_over:
                self.game.isGameOver()
                if not self.game.game_over:
                    if self.game.game_board.black_turn:
                        # print("Black's Turn")
                        self.black_player.makeMove()
                        board_arr = self.game.game_board.boardToVector().tolist()[0]

                        if self.black_player.type.find("human") == -1:
                            time.sleep(2)
                        self.refreshBoard(board_arr)
                    else:
                        # print("White's Turn")
                        self.white_player.makeMove()
                        board_arr = self.game.game_board.boardToVector().tolist()[0]
                        if self.white_player.type.find("human") == -1:
                            time.sleep(2)
                        self.refreshBoard(board_arr)
            self.parent.update_idletasks()
            self.parent.update()
