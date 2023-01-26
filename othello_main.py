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

def toggle_widgets(hints_checkbox,
                   depth_label,
                   depth_spinbox,
                   eval_dropdown,
                   eval_label,
                   move_ord_checkbox,
                   selected_type):
    state_1 = DISABLED
    state_2 = NORMAL
    if selected_type.get() == "human":
        state_1 = NORMAL
        state_2 = DISABLED
    hints_checkbox["state"] = state_1
    depth_label["state"] = state_2
    depth_spinbox["state"] = state_2
    eval_dropdown["state"] = state_2
    eval_label["state"] = state_2
    move_ord_checkbox["state"] = state_2


def save_game_data(root,
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

    BOARD_SIZE = board_size.get()
    BLACK_PLAYER_TYPE = black_type.get()
    WHITE_PLAYER_TYPE = white_type.get()
    BLACK_HINTS = black_hints.get()
    WHITE_HINTS = white_hints.get()
    BLACK_DEPTH = black_depth.get()
    WHITE_DEPTH = white_depth.get()
    BLACK_EVALUATION_FN = black_eval_fn.get()
    WHITE_EVALUATION_FN = white_eval_fn.get()
    BLACK_MOVE_ORDERING = black_move_ordering.get()
    WHITE_MOVE_ORDERING = white_move_ordering.get()
    root.destroy()


def reset_game_data(root,
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
    board_size.set(BOARD_SIZE)
    black_type.set(BLACK_PLAYER_TYPE)
    white_type.set(WHITE_PLAYER_TYPE)
    black_hints.set(BLACK_HINTS)
    white_hints.set(WHITE_HINTS)
    black_depth.set(BLACK_DEPTH)
    white_depth.set(WHITE_DEPTH)
    black_eval_fn.set(BLACK_EVALUATION_FN)
    white_eval_fn.set(WHITE_EVALUATION_FN)
    black_move_ordering.set(BLACK_MOVE_ORDERING)
    white_move_ordering.set(WHITE_MOVE_ORDERING)
    if root is not None:
        root.destroy()

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
    add_menu_widget(root,
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
                    white_move_ordering)
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


def add_menu_widget(root,
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
    menu_bar = Menu(root)
    game_menu = Menu(menu_bar, tearoff=0)
    game_menu.add_command(label="New Game", command=lambda: start_game(root,
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
    game_menu.add_separator()
    root.config(menu=menu_bar)


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

    add_menu_widget(root,
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
                    white_move_ordering)

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
