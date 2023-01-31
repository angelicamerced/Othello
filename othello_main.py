from tkinter import *
from board import Board
from global_var import CELL_SIZE

BOARD_SIZE = 8
BLACK_PLAYER_TYPE = "human"
WHITE_PLAYER_TYPE = "computer"
BLACK_HINTS = True
WHITE_HINTS = True
BLACK_MOVE_ORDERING = True
WHITE_MOVE_ORDERING = True
BLACK_EVALUATION_FN = "simple"
WHITE_EVALUATION_FN = "simple"
BLACK_DEPTH = 4
WHITE_DEPTH = 4


def get_cell_size(n):
    factor = n / 8
    return CELL_SIZE / factor

def start_game(root,
               board_size,
               black_type,
               white_type,
               black_hints,
               white_hints,
               black_depth,
               white_depth,
               black_eval_fn,
               white_eval_fn,
               black_move_ordering,
               white_move_ordering):
    for widget in root.winfo_children():
        widget.destroy()
    root.geometry("")
    board = Board(root,
                  BOARD_SIZE,
                  get_cell_size(BOARD_SIZE),
                  "#189AB4",
                  BLACK_PLAYER_TYPE,
                  WHITE_PLAYER_TYPE,
                  BLACK_HINTS,
                  WHITE_HINTS,
                  int(BLACK_DEPTH),
                  int(WHITE_DEPTH),
                  BLACK_EVALUATION_FN,
                  WHITE_EVALUATION_FN,
                  BLACK_MOVE_ORDERING,
                  WHITE_MOVE_ORDERING)
    board.pack(side="top", padx=4, pady=4)


def main():
    root = Tk()
    root.title("Othello")
    root.geometry("300x300")
    root.resizable(False, False)

    global BOARD_SIZE, \
        BLACK_PLAYER_TYPE, \
        WHITE_PLAYER_TYPE, \
        BLACK_HINTS, \
        WHITE_HINTS, \
        BLACK_DEPTH, \
        WHITE_DEPTH, \
        BLACK_EVALUATION_FN, \
        WHITE_EVALUATION_FN, \
        BLACK_MOVE_ORDERING, \
        WHITE_MOVE_ORDERING

    board_size = IntVar(value=BOARD_SIZE)
    black_type = StringVar(value=BLACK_PLAYER_TYPE)
    white_type = StringVar(value=WHITE_PLAYER_TYPE)
    black_hints = BooleanVar(value=BLACK_HINTS)
    white_hints = BooleanVar(value=WHITE_HINTS)
    black_depth = StringVar(value=BLACK_DEPTH)
    white_depth = StringVar(value=WHITE_DEPTH)
    black_eval_fn = StringVar(value=BLACK_EVALUATION_FN)
    white_eval_fn = StringVar(value=WHITE_EVALUATION_FN)
    black_move_ordering = BooleanVar(value=BLACK_MOVE_ORDERING)
    white_move_ordering = BooleanVar(value=WHITE_MOVE_ORDERING)


    start_btn = Button(root, height=2, width=10, text="Start",
                       font='Roboto 12 bold', command=lambda: start_game(root,
                                                                              board_size,
                                                                              black_type,
                                                                              white_type,
                                                                              black_hints,
                                                                              white_hints,
                                                                              black_depth,
                                                                              white_depth,
                                                                              black_eval_fn,
                                                                              white_eval_fn,
                                                                              black_move_ordering,
                                                                              white_move_ordering))

    start_btn.place(relx=0.5, rely=0.3, anchor=CENTER)
    root.mainloop()


if __name__ == "__main__":
    main()
