from engine.agent import Human, RandomAgent, Agent, MCTSAgent
import numpy as np
from engine.board import Board
from engine.env import Env
from IPython.display import display, clear_output
from typing import List



# def play(player1: Agent, player2: Agent, player: List[Agent] , game_env: Env, display=False):
def play(players: List[Agent] , game_env: Env, display=False):

    player_to_start = players[0].player_to_move
    
    if display is False or None:
        while not game_env.board.is_terminal_state()[0]:
            for player in players:
                player.update_game_env(game_env=game_env)

            if game_env.board.player_to_move == player_to_start:
                move1 = players[0].select_move()
                game_env.board.make_move(move1, player_to_move=players[0].player_to_move)
            else:
                move1 = players[1].select_move()
                game_env.board.make_move(move1, player_to_move=players[1].player_to_move)

            for player in players:
                player.update_game_env(game_env=game_env)
            
            if game_env.board.is_terminal_state()[0]:
                break

            if game_env.board.player_to_move == player_to_start:
                move2 = players[0].select_move()
                game_env.board.make_move(move2, player_to_move=players[0].player_to_move)
            else:
                move2 = players[1].select_move()
                game_env.board.make_move(move2, player_to_move=players[1].player_to_move)





    elif display is True:
        while not game_env.board.is_terminal_state()[0]:

            for player in players:
                player.update_game_env(game_env=game_env)

            if game_env.board.player_to_move == player_to_start:
                print('now it is turn for player: ', players[0].player_to_move)
                move1 = players[0].select_move()
                # clear_output(wait=True)
                game_env.board.make_move(move1, player_to_move=players[0].player_to_move)
            else:
                print('now it is turn for player: ', players[1].player_to_move)
                move1 = players[1].select_move()
                # clear_output(wait=True)
                game_env.board.make_move(move1, player_to_move=players[1].player_to_move)
            print(game_env.board.board)

            for player in players:
                player.update_game_env(game_env=game_env)
            
            if game_env.board.is_terminal_state()[0]:
                break

            if game_env.board.player_to_move == player_to_start:
                print('now it is turn for player: ', players[0].player_to_move)
                move2 = players[0].select_move()
                # clear_output(wait=True)
                game_env.board.make_move(move2, player_to_move=players[0].player_to_move)
            else:
                print('now it is turn for player: ', players[1].player_to_move)
                move2 = players[1].select_move()
                # clear_output(wait=True)
                game_env.board.make_move(move2, player_to_move=players[1].player_to_move)
            print(game_env.board.board)
            clear_output(wait=True)



    return game_env.board.is_terminal_state()[1]
