from engine.agent import Human, RandomAgent
import numpy as np
from engine.board import Board
from engine.env import Env


game_env = Env()

player1 = Human(game_env=game_env, player_to_move=1)
player2 = RandomAgent(game_env=game_env, player_to_move=-1)




while not game_env.board.is_terminal_state()[0]:
    player1.update_game_env(game_env=game_env)
    player2.update_game_env(game_env=game_env)
    
    move1 = player1.select_move()
    game_env.board.make_move(move1, player_to_move=1)
    print(game_env.board.board)

    player1.update_game_env(game_env=game_env)
    player2.update_game_env(game_env=game_env)

    move2 = player2.select_move()
    game_env.board.make_move(move2, player_to_move=-1)
    print(game_env.board.board)

print('GAME OVER')
