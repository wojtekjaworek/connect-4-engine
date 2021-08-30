import numpy as np
from numpy.lib.utils import who
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
        self.score = 0
        self.ucb1 = 0
        self.untried_actions = self.game_env.board.generate_legal_moves()
        self.children = []
        self.is_fully_expanded = self.check_if_fully_expanded()
        self.is_terminal = self.check_if_terminal()
        return None


    def check_if_fully_expanded(self) -> bool:
        return len(self.untried_actions) == 0

    def check_if_terminal(self) -> bool:
        return self.game_env.board.is_terminal_state()[0]



class MCTS():
    def __init__(self, game_env: Env, player_to_move, search_depth, ):
        #game_env.board.player_to_move zawsze jest zgodne z player_to_move !! 
        self.player_to_move = player_to_move
        self.game_env = game_env
        self.search_depth = search_depth
        # zmiana w razie player_to_move = -1 :
         # TODO: sda 
        if player_to_move == -1:
            self.player_to_move = -self.player_to_move
            self.game_env.board.player_to_move = -self.game_env.board.player_to_move
            self.game_env.board.board = np.multiply(self.game_env.board.board, -1)

        return None




    def search(self):

        self.root = MCTSNode(game_env=self.game_env, parent=None, parent_action=None, player_to_move=self.player_to_move)



        is_win, who_win, winning_move = self.is_mate_in_one(self.root.game_env) # if in current position MCTSAgent can mate opponent, then make winning move :)
        if is_win is True:
            return winning_move, winning_move

        for i in range(self.search_depth):
            node = self.selection(self.root)
            score, moves_until_terminal = self.rollout(node)
            
                # self.print_info(node)
            self.backpropagate(node, score, moves_until_terminal)


    # TODO: pick desired moves
        most_visited_node = self.most_visited_node(self.root)
        highest_score_node = self.highest_score_node(self.root)

        
        i = 0
        for child in self.root.children:
            print(f'child {i} === player to move: {child.player_to_move} === parent action: {child.parent_action} === ucb: {child.ucb1} === visits: {child.visits} === score: {child.score}')
            i += 1

        print(f'PICKED MOVE: ----highest score move: {highest_score_node.parent_action}')


        return most_visited_node.parent_action, highest_score_node.parent_action


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





    def is_mate_in_one(self, game_env: Env):
        """
        returns:
                is_win -> boolean
                who_win -> 1 or -1
                action -> this action in current position mates 
        """
        actions = game_env.board.generate_legal_moves()
        new_env = copy.deepcopy(game_env)
        for action in actions:
            new_env.board.make_move(action, new_env.board.player_to_move)
            is_win, who_win = new_env.board.is_terminal_state()
            if is_win is True: return is_win, who_win, action
            new_env = copy.deepcopy(game_env)
        return is_win, who_win, action


    def is_mate_for_opponent(self, game_env: Env):
        actions = game_env.board.generate_legal_moves()
        new_env = copy.deepcopy(game_env)
        for action in actions:
            new_env.board.make_move(action, new_env.board.player_to_move)
            is_win, who_win = new_env.board.is_terminal_state()
            if is_win is True: return is_win, who_win, action
            new_env = copy.deepcopy(game_env)
        return is_win, who_win, action

        




    def rollout(self, node: MCTSNode):
        rollout_env = copy.deepcopy(node.game_env)
        result = self.player_to_move # initial value for result points at positive outcome of the game for current player, it is due to issues with algorithm facing termination in 1 ply.
        moves_until_terminal = 0
        # print('current state')
        # print(node.game_env.board.board)


        if node.parent.parent is None: # only if we're dealing with self.root children:

            is_win, who_win, winning_move = self.is_mate_in_one(node.game_env) # in this case, we check wether opponent can mate us
            if is_win is True and who_win == -self.player_to_move: 
                # print(f'debug: is_win: {is_win}, who_win: {who_win},  winning_move: {winning_move}')
                return who_win * 10000000, 1 # if opponent can mate us, that means node's action is terrible choice and we return -1000000 score 

            

        while not rollout_env.board.is_terminal_state()[0]:
            moves_until_terminal += 1
            actions = rollout_env.board.generate_legal_moves()
            action = random.choice(actions)
            rollout_env.board.make_move(action, rollout_env.board.player_to_move)
            result = rollout_env.board.is_terminal_state()[1]
            if moves_until_terminal == 1 and node.parent.parent is None: # if the parent of this node is initial root
                return result * 20, moves_until_terminal # enhance result value if the move is mate in one

        return result, moves_until_terminal






    def backpropagate(self, node: MCTSNode, score, moves_until_terminal):
        node.visits += 1

        temp = np.abs(-1 * np.log(moves_until_terminal + 0.1) + 4)


        if score == self.player_to_move:
            node.score += score
        else:
            node.score += score
        
        if node.parent is not None:
            self.backpropagate(node=node.parent, score=score, moves_until_terminal=moves_until_terminal)

        return None



    def UCB1(self, node: MCTSNode, c_param=5):
        best_score= float('-inf')
        best_moves = []
        
        for child in node.children:
            move_score = child.score/child.visits + c_param * np.sqrt(np.log(node.visits)/child.visits)

            if move_score > best_score:
                best_score = move_score
                best_moves = [child]
            elif move_score == best_score:
                best_moves.append(child)


        return random.choice(best_moves)



    def highest_score_node(self, node: MCTSNode):
        best_score_node = node.children[0]
        i = 0
        for child in node.children:
            if child.score > best_score_node.score:
                best_score_node = child
            i += 1
        
        return best_score_node


    def most_visited_node(self, node: MCTSNode):
        most_visited_node = node.children[0]
        i = 0
        for child in node.children:
            if child.visits > most_visited_node.visits:
                most_visited_node = child
            i += 1
        
        return most_visited_node