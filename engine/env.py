from engine.board import Board


class Env():

    def __init__(self, player_to_start=1):
        self.player_to_start = player_to_start
        self.board = Board(player_to_start=player_to_start)
        self.board_history = [] # stores all board states from beginning to terminal state and outcome of the game, TODO: maybe link mcts prediction and give estimate value for each position

    def reset(self):
        del self.board
        self.board = Board()
        
        del self.board_history
        self.board_history = []

