from tkinter import *
from tkmacosx import Button
from game_brain import GameBrain

COLUMNS = [0, 1, 2, 3, 4, 5]
ROWS = [1, 2, 3, 4, 5, 6]
FONT = ("Arial", 15, "normal")


class GameBoard:

    def __init__(self, game_brain: GameBrain):

        self.game_brain = game_brain

        self.root = Tk()
        self.root.title("Tile Memory Game")
        self.root.config(padx=15, pady=10)

        self.game_tiles = []
        self.create_tiles()

        self.level_label = Label(text=f"Level: {self.game_brain.level}", pady=5, font=FONT)
        self.level_label.grid(column=0, row=0, columnspan=2)

        self.high_score_label = Label(text=f"High score: {self.game_brain.high_score}", pady=5, font=FONT)
        self.high_score_label.grid(column=4, row=0, columnspan=2)

        self.start_button = Button(text="Start", bg="green", fg="white", command=self.next_level)
        self.start_button.config(padx=5, pady=5, font=FONT)
        self.start_button.grid(column=1, row=7, columnspan=2)

        self.reset_button = Button(text="Reset", bg="red", fg="white", command=self.reset_game)
        self.reset_button.config(padx=5, pady=5, font=FONT)
        self.reset_button.grid(column=3, row=7, columnspan=2)

        self.player_sequence = []

        self.root.mainloop()

    def create_tiles(self):
        i = 0
        for col in COLUMNS:
            for row in ROWS:
                tile = Button(width=50, height=50, command=lambda t=i: self.tile_pressed(t))
                tile.grid(column=col, row=row)
                self.game_tiles.append(tile)
                i += 1

    def reset_tiles(self):
        for tile in self.game_tiles:
            tile.config(bg="white")

    def flash_tile(self, tile):
        tile.config(bg="red")
        tile.after(1500, self.reset_tiles)

    def show_tile_sequence(self):
        self.game_brain.extend_sequence()
        tile_indices = self.game_brain.tile_sequence
        for index in tile_indices:
            new_tile = self.game_tiles[index]
            self.flash_tile(new_tile)

    def tile_pressed(self, t):
        tile = self.game_tiles[t]
        self.player_sequence.append(t)
        answer_correct = self.game_brain.check_tile(t)
        if answer_correct:
            tile.config(bg="green")
            if len(self.player_sequence) == len(self.game_brain.tile_sequence):
                sequence_correct = self.game_brain.check_sequence(self.player_sequence)
                if sequence_correct:
                    self.root.after(1000, self.next_level)
        else:
            tile.config(bg="red")
            self.game_over()

    def next_level(self):
        self.reset_tiles()
        self.level_label.config(text=f"Level: {self.game_brain.level}")
        self.player_sequence = []
        self.show_tile_sequence()

    def game_over(self):
        for game_tile in self.game_tiles:
            game_tile.config(state="disabled")
        self.game_brain.update_high_score()

    def recreate_tiles(self):
        for tile in self.game_tiles:
            tile.destroy()
        self.game_tiles = []
        self.create_tiles()

    def recreate_start_button(self):
        self.start_button.destroy()
        self.start_button = Button(text="Start", bg="green", fg="white", command=self.next_level)
        self.start_button.config(padx=5, pady=5, font=FONT)
        self.start_button.grid(column=1, row=7, columnspan=2)

    def reset_game(self):
        self.recreate_tiles()
        self.recreate_start_button()
        self.game_brain.reset_sequence()
        self.game_brain.reset_level()
        self.level_label.config(text=f"Level: {self.game_brain.level}")
        with open("high_score.txt") as data:
            high_score = data.read()
        self.high_score_label.config(text=f"High score: {high_score}")
