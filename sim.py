from engine.agent import Human, RandomAgent, Agent, MCTSAgent
import numpy as np
from engine.board import Board
from engine.env import Env
from IPython.display import display, clear_output


def play(player1: Agent, player2: Agent, game_env: Env, display=False):
    
    if display is False or None:
        while not game_env.board.is_terminal_state()[0]:
            player1.update_game_env(game_env=game_env)
            player2.update_game_env(game_env=game_env)
    
            move1 = player1.select_move()
            game_env.board.make_move(move1, player_to_move=1)

            player1.update_game_env(game_env=game_env)
            player2.update_game_env(game_env=game_env)
            
            if game_env.board.is_terminal_state()[0]:
                break

            move2 = player2.select_move()
            game_env.board.make_move(move2, player_to_move=-1)



    elif display is True:
        while not game_env.board.is_terminal_state()[0]:
            player1.update_game_env(game_env=game_env)
            player2.update_game_env(game_env=game_env)
        
            move1 = player1.select_move()
            clear_output(wait=True)
            game_env.board.make_move(move1, player_to_move=1)
            print(game_env.board.board)

            player1.update_game_env(game_env=game_env)
            player2.update_game_env(game_env=game_env)

            if game_env.board.is_terminal_state()[0]:
                break

            move2 = player2.select_move()
            clear_output(wait=True)
            game_env.board.make_move(move2, player_to_move=-1)
            print(game_env.board.board)


    print('GAME OVER, termination: ', game_env.board.is_terminal_state()[1])
