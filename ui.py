from tkinter import *
from tkinter import messagebox
from tkmacosx import Button
from game_brain import GameBrain

COLUMNS = [0, 1, 2]
ROWS = [0, 1, 2]
FONT = ("Arial", 20, "normal")


class GameInterface:

    def __init__(self, game_brain: GameBrain):

        self.game_brain = game_brain

        self.root = Tk()
        self.root.title("TicTacToe")
        self.root.config(padx=15, pady=15)

        self.game_tiles = []
        self.create_game_tiles()

        self.reset_button = Button(text="Reset", bg="red", fg="white", font=FONT)
        self.reset_button.config(width=150, height=50, command=self.reset_game)
        self.reset_button.grid(column=0, row=3, columnspan=3)

        self.root.mainloop()

    def create_game_tiles(self):
        i = 0
        for col in COLUMNS:
            for row in ROWS:
                new_tile = Button(font=("Arial", 100, "normal"))
                new_tile.config(width=100, height=100, command=lambda t=i: self.tile_clicked(t))
                new_tile.grid(column=col, row=row)
                self.game_tiles.append(new_tile)
                i += 1

    def tile_clicked(self, t):
        position_free = self.game_brain.check_position_free(t)
        if not position_free:
            messagebox.showinfo(message="That position is already taken!\n\nPlease try another square.")
        else:
            marker = self.game_brain.determine_marker()
            self.input_marker(marker, t)
            self.game_brain.add_position(marker, t)
            marker_wins = self.game_brain.check_winner(marker)
            if marker_wins:
                messagebox.showinfo(message=f"{marker} WINS!")
                self.end_game()
            else:
                board_full = self.game_brain.check_board_full()
                if board_full:
                    messagebox.showinfo(message="It's a DRAW")
                    self.end_game()

    def input_marker(self, marker, position):
        selected_tile = self.game_tiles[position]
        selected_tile.config(text=marker)

    def end_game(self):
        for tile in self.game_tiles:
            tile.config(state="disabled")

    def reset_game(self):
        for tile in self.game_tiles:
            tile.destroy()
        self.game_tiles = []
        self.create_game_tiles()
        self.game_brain.reset_game_board()
