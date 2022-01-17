import random

TILE_NUMBERS = list(range(0, 36))

try:
    with open("high_score.txt") as data:
        HIGH_SCORE = int(data.read())
except FileNotFoundError:
    HIGH_SCORE = 1


class GameBrain:

    def __init__(self):
        self.level = 1
        self.high_score = HIGH_SCORE
        self.tile_sequence = []

    def extend_sequence(self):
        next_tile = random.choice(TILE_NUMBERS)
        TILE_NUMBERS.remove(next_tile)
        self.tile_sequence.append(next_tile)

    def reset_sequence(self):
        self.tile_sequence = []

    def reset_level(self):
        self.level = 1

    def check_tile(self, user_input):
        if user_input in self.tile_sequence:
            return True
        else:
            return False

    def check_sequence(self, player_sequence):
        if player_sequence.sort() == self.tile_sequence.sort():
            self.level += 1
            return True
        else:
            return False

    def update_high_score(self):
        if self.level > self.high_score:
            self.high_score = self.level
            with open("high_score.txt", mode="w") as game_data:
                game_data.write(f"{self.high_score}")
