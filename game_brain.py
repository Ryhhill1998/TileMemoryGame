class GameBrain:

    def __init__(self):
        self.game_board = [""] * 9
        self.markers = ['X', 'O']
        self.round = 0

    def split_up_board(self):
        board = self.game_board
        return {
            "cols": [board[:3], board[3:6], board[6:]],
            "rows": [board[:7:3], board[1:8:3], board[2:9:3]],
            "diags": [board[:9:4], board[2:7:2]]
        }

    def determine_marker(self):
        if self.round % 2 == 0:
            self.round += 1
            return self.markers[0]
        else:
            self.round += 1
            return self.markers[1]

    def check_position_free(self, user_input):
        if self.game_board[user_input] == "":
            return True
        else:
            return False

    def add_position(self, marker, user_input):
        self.game_board[user_input] = marker

    def check_winner(self, marker):
        marker_wins = False
        split_board = self.split_up_board()
        for board_sections in split_board.values():
            for section in board_sections:
                if section.count(marker) == 3:
                    marker_wins = True
        return marker_wins

    def check_board_full(self):
        if "" in self.game_board:
            return False
        else:
            return True

    def reset_game_board(self):
        self.game_board = [""] * 9
        self.round = 0
