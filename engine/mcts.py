import numpy as np
from engine.env import Env
import copy
import random

class MCTSNode():
    def __init__(self, game_env: Env, player_to_move, parent=None, parent_action=None):
        self.game_env = game_env
        self.parent = parent
        self.parent_action = parent_action
        self.player_to_move = player_to_move
        self.visits = 0
        self.ucb1 = float('-inf')
        self.score = 0
        self.untried_actions = self.game_env.board.generate_legal_moves() # list
        self.children = []
        self.is_fully_expanded = self.check_if_fully_expanded()
        self.is_terminal = self.check_if_terminal()
        return None


    def check_if_fully_expanded(self) -> bool:
        return len(self.untried_actions) == 0

    def check_if_terminal(self) -> bool:
        return self.game_env.board.is_terminal_state()[0]

    

class MCTS():
    def __init__(self, game_env: Env, player_to_move):
        self.game_env = game_env
        self.player_to_move = player_to_move
        return None

    
    def search(self):
        """
        returns two moves: 
                            picked_move_UCB - based on highest ucb1 score
                            picked_move_visits - based on highest number of visits
        """
        self.root = MCTSNode(game_env=self.game_env, parent=None, parent_action=None, player_to_move=self.player_to_move) # player to move is passed in MCTSAgent select_move method, because it will vary due to game specific innitialization
        

        for i in range(200):
            node = self.selection(self.root)
            score = self.rollout(node)
            self.backpropagate(node, score)



        picked_move_UCB = self.UCB1(self.root)
        picked_move_visits = self.most_visited_node(self.root)
        
        return picked_move_UCB.parent_action, picked_move_visits.parent_action


    def selection(self, node: MCTSNode):
        
        while node.is_terminal is False:
            if node.is_fully_expanded is False:
                return self.expansion(node)
            else:
                node = self.UCB1(node)

        return node




    def expansion(self, node: MCTSNode):
        action = node.untried_actions.pop()
        new_env = copy.deepcopy(node.game_env)
        new_env.board.make_move(action, node.player_to_move)
        child_node = MCTSNode(game_env=new_env, parent=node, parent_action=action, player_to_move=-node.player_to_move)
        node.children.append(child_node)
        node.is_fully_expanded = node.check_if_fully_expanded()
        return child_node


    def rollout(self, node: MCTSNode):
        rollout_env = copy.deepcopy(node.game_env)
        result = 0

        while not rollout_env.board.is_terminal_state()[0]:
            actions = rollout_env.board.generate_legal_moves()
            action = random.choice(actions)
            rollout_env.board.make_move(action, node.player_to_move)
            result = rollout_env.board.is_terminal_state()[1]
        
        return result

    


    def backpropagate(self, node: MCTSNode, score):
        node.visits += 1
        node.score += score
        if node.parent is not None:
            self.backpropagate(node=node.parent, score=score)
        
        return None


    def UCB1(self, node: MCTSNode, c_param=2) ->MCTSNode:
        best_score = float('-inf')
        best_moves = []

        if node.player_to_move == 1:
            player_coeff = 1
        else:
            player_coeff = -1

        for child in node.children:
            move_score = player_coeff * child.score/child.visits + c_param * np.sqrt(np.log(node.visits)/child.visits)
            child.ucb1 = move_score


            if move_score > best_score:
                best_score = move_score
                best_moves = [child]
            elif move_score == best_score:
                best_moves.append(child)



        return random.choice(best_moves)


            
    
    def most_visited_node(self, node: MCTSNode):
        most_visited = node.children[0]
        i = 0
        for child in node.children:
            if child.visits > most_visited.visits:
                most_visited = child
            i += 1

    
        return most_visited




















