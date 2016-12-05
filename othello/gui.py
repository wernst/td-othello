import Tkinter as tk
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
        # self.board = tk.Canvas(self.canvas, borderwidth=0, highlightthickness=0,
        #                         width=canvas_width, height=canvas_height, background="red")
        # self.board.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refreshBoardSize)
        self.canvas.bind("<Button-1>", self.refreshBoard)

    def normalizeCoords(self, row, col):
        return row/self.size, col/self.size

    def refreshBoard(self, event):
        if event.x < (self.size*self.columns) and event.y < (self.size*self.rows):
            move = self.normalizeCoords(event.y, event.x)
            print(move)
            self.game.setTile(move[0], move[1])
            board_arr = self.game.game_board.boardToVector().tolist()[0]
            print(event.x, event.y)
            self.canvas.delete("square")
            for i in range(len(board_arr)):
                row = i/8
                col = i%8
                x1 = ((col) * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                color = "black" if board_arr[i] == 1 else "white" if board_arr[i] == -1 else "lawn green"
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
            for name in self.pieces:
                self.placepiece(name, self.pieces[name][0], self.pieces[name][1])
            self.canvas.tag_raise("piece")
            self.canvas.tag_lower("square")

    def refreshBoardSize(self, event):
        board_arr = self.game.game_board.boardToVector().tolist()[0]
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        for i in range(len(board_arr)):
            row = i/8
            col = i%8
            x1 = ((col) * self.size)
            y1 = (row * self.size)
            x2 = x1 + self.size
            y2 = y1 + self.size
            color = "black" if board_arr[i] == 1 else "white" if board_arr[i] == -1 else "lawn green"
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
        for name in self.pieces:
            self.placepiece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

    def addpiece(self, name, image, row=0, column=0):
        '''Add a piece to the playing board'''
        self.canvas.create_image(0,0, image=image, tags=(name, "piece"), anchor="c")
        self.placepiece(name, row, column)

    def placepiece(self, name, row, column):
        '''Place a piece at the given row/column'''
        self.pieces[name] = (row, column)
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        self.canvas.coords(name, x0, y0)

    def refresh(self, event):
        '''Redraw the board, possibly in response to window being resized'''
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2
        for name in self.pieces:
            self.placepiece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

    def key(self, event):
        print("char pressed")
        #print("pressed", repr(event.char))

    def callback(self, event):
        #frame.focus_set()
        #print("clicked at", event.x, event.y)
        print("clicked")

    def play(self):
        self.pack(side="top", fill="both", expand="true", padx=4, pady=4)
        self.parent.mainloop()
