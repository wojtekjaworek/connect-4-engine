import numpy as np

class Board():
    
    def __init__(self):
        self.board = np.zeros((6,7),dtype=int) # 6 rows, 7 cols
        self.player_to_move = 1 # 1 always starts the game
        return None

    def is_move_legal(self, col) -> bool: # while making move, player picks only desired column!!!
        if col >= 0 and col < 7: return self.board[0, col] == 0 
        else: return False


    def make_move(self, col, player_to_move):
        if self.is_move_legal(col) == True:
            for row in reversed(range(6)):
                if self.board[row, col] == 0:
                    self.board[row, col] = player_to_move # player_to_move is either 1(player nr 1, who started game) or -1(second player)
                    self.player_to_move = -self.player_to_move # now it is opposite player turn
                    break
        else: # if move is not legal
            print('illegal move!')



    def generate_legal_moves(self) -> list: # list of columns with available cells
        legal_moves = []
        for col in range(7):
            if self.board[0, col] == 0:
                legal_moves.append(col)
        return legal_moves


    def is_fully_expanded(self) -> bool:
        for col in range(7):
            for row in range(6):
                if self.board[row, col] == 0: return False
        return True



    def is_terminal_state(self) -> bool:
        """
        returns: is_terminal(bool), player_to_win
        """
        for player_type in [-1, 1]:
            # horizontal 
            for col in range(7-3): # -3 due to forward-oriented searching for terminal state on the board
                for row in range(6):
                    if self.board[row, col] == player_type and self.board[row, col+1] == player_type and self.board[row, col+2] == player_type and self.board[row, col+3] == player_type:
                        return True, player_type # there is a terminal state

            # vertical 
            for col in range(7): 
                for row in range(6-3):
                    if self.board[row, col] == player_type and self.board[row+1, col] == player_type and self.board[row+2, col] == player_type and self.board[row+3, col] == player_type:
                        return True, player_type 

            # diagonal with positive slope
            for col in range(7-3): 
                for row in range(6-3):
                    if self.board[row, col] == player_type and self.board[row+1, col+1] == player_type and self.board[row+2, col+2] == player_type and self.board[row+3, col+3] == player_type:
                        return True, player_type

            # diagonal with negative slope
            for col in range(7-3): 
                for row in range(3, 6):
                    if self.board[row, col] == player_type and self.board[row-1, col+1] == player_type and self.board[row-2, col+2] == player_type and self.board[row-3, col+3] == player_type:
                        return True, player_type


        if self.is_fully_expanded() is True: return True, 0 # 0 means draw

        
        return False, 0 # no terminal state found
                        

 