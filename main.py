import numpy as np
from board import *

board = Board()


board.make_move(3,1)
board.make_move(3,-1)
board.make_move(3,1)
board.make_move(3,-1)
board.make_move(3,1)
board.make_move(3,-1)
board.make_move(3,1)
board.make_move(3,-1)
board.make_move(3,1)
board.make_move(3,-1)
print(board.board)
print(board.generate_legal_moves())