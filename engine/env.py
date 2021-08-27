from engine.board import Board


class Env():

    def __init__(self):
        self.board = Board()

    def reset(self):
        del self.board
        self.board = Board()

