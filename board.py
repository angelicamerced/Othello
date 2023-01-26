from tkinter import *
import numpy as np
import PIL.Image
import PIL.ImageTk
import math
from othello import Othello
from ai import AI
from global_var import WHITE_TILE, BLACK_TILE, NEXT_MOVE_IMG, WHITE, BLACK, VALID_MOVE, GAME_IN_PROGRESS, LAST_MOVE


class Board(Frame):
    def __init__(self,
                 parent,
                 n,
                 size,
                 color,
                 black_player_type,
                 white_player_type,
                 black_hints,
                 white_hints,
                 black_depth,
                 white_depth,
                 black_evaluation_fn,
                 white_evaluation_fn,
                 black_move_ordering,
                 white_move_ordering):
        # Initialize agents
        self.black = AI(BLACK,
                           black_player_type,
                           black_hints,
                           black_depth,
                           black_evaluation_fn,
                           black_move_ordering)
        self.white = AI(WHITE,
                           white_player_type,
                           white_hints,
                           white_depth,
                           white_evaluation_fn,
                           white_move_ordering)
        # Initialize game object
        self.game = Othello(n)
        # Pass turn to black as black always starts first
        self.current_player = self.black
        # Initialize board parameters
        n = 2 ** math.ceil(math.log2(n))
        self.n = n
        self.size = size
        self.color = color
        # Initialize images
        self.image_size = math.floor(size * 0.75)
        image = PIL.Image.open(WHITE_TILE)
        image = image.resize((self.image_size, self.image_size))
        self.white_img = PIL.ImageTk.PhotoImage(image)
        image = PIL.Image.open(BLACK_TILE)
        image = image.resize((self.image_size, self.image_size))
        self.black_img = PIL.ImageTk.PhotoImage(image)
        image = PIL.Image.open(NEXT_MOVE_IMG)
        image = image.resize((self.image_size, self.image_size))
        self.next_move_img = PIL.ImageTk.PhotoImage(image)
        # Initialize widgets (board, scoreboard)
        Frame.__init__(self, parent, bg="#D4F1F4")
        self.black_score_var = IntVar(value=self.game.black_score)
        self.white_score_var = IntVar(value=self.game.white_score)

        self.canvas = Canvas(self, borderwidth=0, highlightthickness=0, width=n * size, height=n * size, bg="#D4F1F4")
        self.score_board = Canvas(self, width=n * size, height=20, bg="#D4F1F4", highlightthickness=0)
        self.black_score_widget = Label(self.score_board, compound=LEFT, image=self.black_img,
                                        text=self.game.black_score, bg="#D4F1F4", padx=20,
                                        textvariable=self.black_score_var, font='Roboto 15 bold')
        self.white_score_widget = Label(self.score_board, compound=RIGHT, image=self.white_img,
                                        text=self.game.white_score, bg="#D4F1F4", padx=20,
                                        textvariable=self.white_score_var, font='Roboto 15 bold')
        self.black_score_widget.image = self.black_img
        self.white_score_widget.image = self.white_img
        self.moves_btns = []
        # Render widgets
        self.canvas.pack(side="top", fill="both", expand=True, padx=4, pady=4)
        self.score_board.pack(side="bottom", fill="both", expand=True, padx=4, pady=4)
        self.black_score_widget.pack(side="left")
        self.white_score_widget.pack(side="right")

        self.canvas.bind("<Destroy>", self.quit)
        self.window_destroyed = False
        self.initialize_board()
        if self.current_player.agent_type == "computer":
            self.canvas.after(1000, self.run_player_move)
        else:
            self.run_player_move()

    def run_player_move(self, move=None):
        pass_turn_to_computer = False
        if self.current_player.agent_type == "human":
            if move is not None:
                self.game.apply_move(self.current_player.identifier, move)
                self.current_player = self.black if self.current_player.identifier == WHITE else self.white
            event = self.game.status()
            if event == GAME_IN_PROGRESS:
                if self.current_player.agent_type == "human":
                    moves = self.game.move_generator(self.current_player.identifier)
                    if len(moves) == 0:  # If a player doesn't have a move, pass the play to the other player
                        self.current_player = self.black if self.current_player.identifier == WHITE else self.white
                        moves = self.game.move_generator(self.current_player.identifier)
                        if len(moves) == 0:
                            self.current_player = self.black if self.current_player.identifier == WHITE else self.white
                            event = self.game.status()
                elif self.current_player.agent_type == "computer":
                    pass_turn_to_computer = True
            self.black_score_var.set(self.game.black_score)
            self.white_score_var.set(self.game.white_score)
            self.refresh()
            if pass_turn_to_computer and event == GAME_IN_PROGRESS:
                self.canvas.after(0, self.run_player_move)
        elif self.current_player.agent_type == "computer":
            player_move = self.current_player.get_move(self.game, self.current_player.identifier)
            if player_move is not None:
                self.game.apply_move(self.current_player.identifier, player_move)
            self.current_player = self.black if self.current_player.identifier == WHITE else self.white
            event = self.game.status()
            if event == GAME_IN_PROGRESS:
                if self.current_player.agent_type == "human":
                    moves = self.game.move_generator(self.current_player.identifier)
                    if len(moves) == 0:  # If a player doesn't have a move, pass the play to the other player
                        self.current_player = self.black if self.current_player.identifier == WHITE else self.white
                        pass_turn_to_computer = True
                elif self.current_player.agent_type == "computer":
                    pass_turn_to_computer = True
            self.black_score_var.set(self.game.black_score)
            self.white_score_var.set(self.game.white_score)
            self.refresh()
            if pass_turn_to_computer and event == GAME_IN_PROGRESS:
                self.canvas.after(0, self.run_player_move)

    def add_piece(self, kind, row, column, hints=False):
        x0 = (column * self.size) + int(self.size / 2)
        y0 = (row * self.size) + int(self.size / 2)
        if kind == WHITE:
            self.canvas.create_image(x0, y0, image=self.white_img, tags="piece", anchor=CENTER)
        elif kind == BLACK:
            self.canvas.create_image(x0, y0, image=self.black_img, tags="piece", anchor=CENTER)
        elif kind == VALID_MOVE:
            move_btn = Button(self, bg=self.color, activebackground=self.color, relief=FLAT, overrelief=FLAT,
                              command=lambda: self.run_player_move([row, column]), anchor=CENTER)
            if hints:
                move_btn.configure(image=self.next_move_img)
            self.moves_btns.append(move_btn)
            self.canvas.create_window(x0, y0, anchor=CENTER, window=move_btn, height=self.size - 1, width=self.size - 1,
                                      tags="move")
        elif kind == LAST_MOVE:
            self.canvas.create_oval(x0-5, y0-5, x0+5, y0+5, fill="red", tags="last_move", )

    def update_images(self):
        self.image_size = math.floor(self.size * 0.75)
        image = PIL.Image.open(WHITE_TILE)
        image = image.resize((self.image_size, self.image_size))
        self.white_img = PIL.ImageTk.PhotoImage(image)
        image = PIL.Image.open(BLACK_TILE)
        image = image.resize((self.image_size, self.image_size))
        self.black_img = PIL.ImageTk.PhotoImage(image)
        image = PIL.Image.open(NEXT_MOVE_IMG)
        image = image.resize((self.image_size, self.image_size))
        self.next_move_img = PIL.ImageTk.PhotoImage(image)

    def refresh(self):
        if self.window_destroyed:
            return
        self.canvas.delete("last_move")
        self.canvas.delete("piece")
        self.canvas.delete("move")
        for btn in self.moves_btns:
            btn.destroy()
            del btn
        white_pieces_indices = np.argwhere(self.game.state == WHITE)
        black_pieces_indices = np.argwhere(self.game.state == BLACK)
        next_move_indices = np.argwhere(self.game.state == VALID_MOVE)
        last_move_index = None
        if self.game.last_move is not None:
            last_move_index = self.game.last_move
        for index in white_pieces_indices:
            self.add_piece(WHITE, index[0], index[1])
        for index in black_pieces_indices:
            self.add_piece(BLACK, index[0], index[1])
        if self.current_player.agent_type == "human":
            for index in next_move_indices:
                self.add_piece(VALID_MOVE, index[0], index[1], self.current_player.hints)
        if last_move_index is not None:
            self.add_piece(LAST_MOVE, last_move_index.x, last_move_index.y)
        self.canvas.tag_raise("move")
        self.canvas.tag_raise("piece")
        self.canvas.tag_raise("last_move")
        self.canvas.tag_lower("square")
        self.canvas.update()

    def initialize_board(self):
        for row in range(self.n):
            for col in range(self.n):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=self.color, tags="square")
        white_pieces_indices = np.argwhere(self.game.state == WHITE)
        black_pieces_indices = np.argwhere(self.game.state == BLACK)
        next_move_indices = np.argwhere(self.game.state == VALID_MOVE)
        for index in white_pieces_indices:
            self.add_piece(WHITE, index[0], index[1])
        for index in black_pieces_indices:
            self.add_piece(BLACK, index[0], index[1])
        if self.current_player.agent_type == "human":
            for index in next_move_indices:
                self.add_piece(VALID_MOVE, index[0], index[1], self.current_player.hints)
        self.canvas.tag_raise("move")
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")
        self.canvas.update()

    def quit(self, event=None):
        self.window_destroyed = True
        self.destroy()