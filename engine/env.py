from engine.board import Board


class Env():

    def __init__(self, player_to_start=1):
        self.player_to_start = player_to_start
        self.board = Board(player_to_start=player_to_start)

    def reset(self):
        del self.board
        self.board = Board()

