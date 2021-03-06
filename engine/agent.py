import numpy as np
from engine.env import Env
import time
import random
from engine.mcts import MCTS, MCTSNode
import copy
from engine.neural_network import NeuralNetwork

class Agent():

    def __init__(self, game_env: Env, player_to_move):
        self.player_to_move = player_to_move
        self.game_env = game_env

    def update_game_env(self, game_env: Env):
        self.game_env = game_env


class Human(Agent):

    def __init__(self, game_env: Env, player_to_move):
        super().__init__(game_env, player_to_move)
        return None

    def select_move(self):
        
        move = input('Your move (select col numer, starting from 0): ')

    
        while (not move.isdigit()) or (not self.game_env.board.is_move_legal(int(move))):
            move = input('It is not a valid move. Please select legal move: ')
        
        return int(move)




class RandomAgent(Agent):

    def __init__(self, game_env: Env, player_to_move):    
        super().__init__(game_env, player_to_move)  
        return None

    def select_move(self):
        legal_moves = self.game_env.board.generate_legal_moves()
        return int(random.choice(legal_moves))



class MCTSAgent(Agent):

    def __init__(self, game_env: Env, player_to_move, search_depth=1000):
        """
        search_depth default value is 1000
        """
        self.search_depth = search_depth
        super().__init__(game_env, player_to_move)

    def select_move(self):
        # move = input('Your move (or type M for MCTS move): ')
        move = 'M'


        if move == 'M':
            search_env = copy.deepcopy(self.game_env)
            search_player_to_move = copy.deepcopy(self.player_to_move)
            mcts = MCTS(game_env=search_env, player_to_move=search_player_to_move, search_depth=self.search_depth)
            move = mcts.search()[1]

        else:
            move = int(move)


        return move



class NNAgent(Agent):

    def __init__(self, game_env: Env, neural_network: NeuralNetwork, player_to_move, ):
        super().__init__(game_env, player_to_move)

    def select_move(self):
        move = 1


        return move