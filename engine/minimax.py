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
        self.total_moves_until_terminal = 0 # accessor to calculate mean nr of moves until terminal
        self.mean_number_of_moves_until_terminal = 9999
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
    def __init__(self, game_env: Env, player_to_move, search_depth):
        print('debug: ', game_env.board.player_to_move, player_to_move)
        self.player_to_move = player_to_move
        self.game_env = game_env
        if self.player_to_move == -1: # switch signs to calculate as it was 1
            self.game_env.board.player_to_move = -self.game_env.board.player_to_move # switch player to move sign
            self.game_env.board.board = np.multiply(self.game_env.board.board, -1)
            self.player_to_move = -self.player_to_move
        print(f'game setting: game_env player to move: {self.game_env.board.player_to_move} ===== ')
        print(f'board state: \n {self.game_env.board.board}')
        print(f'self.player_to_move: {self.player_to_move}')

        self.search_depth = search_depth
        return None

    
    def search(self):
        """
        returns three moves: 
                            picked_move_UCB - based on highest ucb1 score
                            picked_move_visits - based on highest number of visits
                            picked_move_score - based on highest score
        """
        self.root = MCTSNode(game_env=self.game_env, parent=None, parent_action=None, player_to_move=self.player_to_move) # player to move is passed in MCTSAgent select_move method, because it will vary due to game specific innitialization
        

        for i in range(self.search_depth):
            node = self.selection(self.root)
            score, moves_until_terminal = self.rollout(node)
            self.backpropagate(node, score, moves_until_terminal)



        picked_move_UCB = self.UCB1(self.root)
        picked_move_visits = self.most_visited_node(self.root)
        picked_move_score = self.highest_score_node(self.root)
        

        i = 0
        for child in self.root.children:
            print(f'child {i} === player to move: {child.player_to_move} === parent action: {child.parent_action} === ucb: {child.ucb1} === visits: {child.visits} === score: {child.score}')
            i += 1

        
    

        return picked_move_UCB.parent_action, picked_move_visits.parent_action, picked_move_score.parent_action


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
        # print('initial')
        # print(rollout_env.board.board)
        moves_until_terminal = 0

        while not rollout_env.board.is_terminal_state()[0]:
            # print('start')
            moves_until_terminal += 1
            actions = rollout_env.board.generate_legal_moves()
            action = random.choice(actions)
            rollout_env.board.make_move(action, rollout_env.board.player_to_move)
            result = rollout_env.board.is_terminal_state()[1]
            # print('print')
            # print(rollout_env.board.board)
            # print('end')
        

        return result, moves_until_terminal

    


    def backpropagate(self, node: MCTSNode, score, moves_until_terminal):
        node.visits += 1
        
        node.score += score 
        node.total_moves_until_terminal += moves_until_terminal
        node.mean_number_of_moves_until_terminal = node.total_moves_until_terminal / node.visits
        if node.parent is not None:
            self.backpropagate(node=node.parent, score=score, moves_until_terminal=moves_until_terminal)
        
        return None


    def UCB1(self, node: MCTSNode, c_param=2) ->MCTSNode:

        
        player_coeff = 1
        best_score =  float('-inf')
        best_moves = []

        for child in node.children:
            move_score =  child.score/child.visits + player_coeff * c_param * np.sqrt(np.log(node.visits)/child.visits)
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


    def highest_score_node(self, node: MCTSNode):
        best_score = node.children[0]
        i = 0
        for child in node.children:
            if child.score > best_score.score:
                best_score = child
            i += 1

        return best_score


    def lowest_score_node(self, node: MCTSNode):
            best_score = node.children[0]
            i = 0
            for child in node.children:
                if child.score < best_score.score:
                    best_score = child
                i += 1

            return best_score

