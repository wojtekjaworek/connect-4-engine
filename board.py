"""
Board class to handle game actions.

"""

import numpy as np

class Board():
    
    def __init__(self):
        self.board = np.zeros((6,7)) # 6 rows, 7 cols
        return None

    def is_move_legal(self, col) -> bool: # while making move, player picks only desired column!!!
        return self.board[0, col] == 0 


    def make_move(self, col, player_to_move):
        if self.is_move_legal(col) == True:
            for row in reversed(range(6)):
                if self.board[row, col] == 0:
                    self.board[row, col] = player_to_move # player_to_move is either 1(player nr 1, who started game) or -1(second player)
                    break
        else: # if move is not legal
            print('illegal move!')



    def generate_legal_moves(self) -> list: # list of columns with available cells
        legal_moves = []
        for col in range(7):
            if self.board[0, col] == 0:
                legal_moves.append(col)
        return legal_moves