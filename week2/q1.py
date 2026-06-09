import json
import copy  # use it for deepcopy if needed
import math  # for math.inf
import logging

logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)

# Global variables in which you need to store player strategies (this is data structure that'll be used for evaluation)
# Mapping from histories (str) to probability distribution over actions
strategy_dict_x = {}
strategy_dict_o = {}


class History:
    def __init__(self, history=None):
        """
        # self.history : Eg: [0, 4, 2, 5]
            keeps track of sequence of actions played since the beginning of the game.
            Each action is an integer between 0-8 representing the square in which the move will be played as shown
            below.
              ___ ___ ____
             |_0_|_1_|_2_|
             |_3_|_4_|_5_|
             |_6_|_7_|_8_|

        # self.board
            empty squares are represented using '0' and occupied squares are either 'x' or 'o'.
            Eg: ['x', '0', 'x', '0', 'o', 'o', '0', '0', '0']
            for board
              ___ ___ ____
             |_x_|___|_x_|
             |___|_o_|_o_|
             |___|___|___|

        # self.player: 'x' or 'o'
            Player whose turn it is at the current history/board

        :param history: list keeps track of sequence of actions played since the beginning of the game.
        """
        if history is not None:
            self.history = history
            self.board = self.get_board()
        else:
            self.history = []
            self.board = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        self.player = self.current_player()

    def current_player(self):
        """ Player function
        Get player whose turn it is at the current history/board
        :return: 'x' or 'o' or None
        """
        total_num_moves = len(self.history)
        if total_num_moves < 9:
            if total_num_moves % 2 == 0:
                return 'x'
            else:
                return 'o'
        else:
            return None

    def get_board(self):
        """ Play out the current self.history and get the board corresponding to the history in self.board.

        :return: list Eg: ['x', '0', 'x', '0', 'o', 'o', '0', '0', '0']
        """
        board = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        for i in range(len(self.history)):
            if i % 2 == 0:
                board[self.history[i]] = 'x'
            else:
                board[self.history[i]] = 'o'
        return board

    def is_win(self):
        board=self.get_board()
        for i in range(3):
            if board[3 * i] == board[3 * i + 1] == board[3 * i + 2] != '0':
                return board[3*i]

            if board[i] == board[i + 3] == board[i + 6] != '0':
                return board[i]

        if board[0] == board[4] == board[8] != '0':
            return board[4]

        if board[2] == board[4] == board[6] != '0':
            return board[4]
        return 0
        # check if the board position is a win for either players
        # Feel free to implement this in anyway if needed
        pass

    def is_draw(self):
        if self.is_win():
            return False
        return True
        # check if the board position is a draw
        # Feel free to implement this in anyway if needed
        pass

    def get_valid_actions(self):
        actions=[]
        board=self.get_board()
        for i in range(len(board)):
            if board[i]=='0':
                actions.append(i)
        return actions
        # get the empty squares from the board
        # Feel free to implement this in anyway if needed
        pass

    def is_terminal_history(self):
        if len(self.history)==9:
            return True
        if self.is_win():
            return True
        return False
        # check if the history is a terminal history
        # Feel free to implement this in anyway if needed
        pass

    def get_utility_given_terminal_history(self):
        
        # Feel free to implement this in anyway if needed
        pass

    def update_history(self, action):
        new_history=copy.deepcopy(self.history)
        new_history.append(action)
        next_history=History(new_history)
        return next_history
        # In case you need to create a deepcopy and update the history obj to get the next history object.
        # Feel free to implement this in anyway if needed
        pass
a=History()

def backward_induction(history_obj):
    """
    :param history_obj: History class object
    :return: best achievable utility (float) for th current history_obj
    """

    global strategy_dict_x, strategy_dict_o
    if history_obj.is_terminal_history():
        if history_obj.is_win()=='x':
            return 1-0.01*len(history_obj.history)
        if history_obj.is_win()=='o':
            return -(1-0.01*len(history_obj.history))
            # if history_obj.current_player()=='x':
            #     strategy_dict_x[''.join(map(str,history_obj.history))]={str(i):0 for i in range(9)}
            #     strategy_dict_x[''.join(map(str,history_obj.history))][history_obj.history[-1]]=1
            return history_obj.is_win()
        if history_obj.is_draw():
            return 0
    if history_obj.current_player()=='x':
        bu=-math.inf
        strategy_dict_x["".join(map(str,history_obj.history))]={str(i):0 for i in range(9)}
        actions=history_obj.get_valid_actions()
        bi=actions[0]
        for i in actions:
            afteraction=history_obj.update_history(i)
            u=backward_induction(afteraction)
            if u>bu:
                bu=u
                bi=i
        strategy_dict_x["".join(map(str,history_obj.history))][str(bi)]=1
        return bu
    if history_obj.current_player()=='o':
        bu=math.inf
        strategy_dict_o["".join(map(str,history_obj.history))]={str(i):0 for i in range(9)}
        actions=history_obj.get_valid_actions()
        bi=actions[0]
        for i in actions:
            afteraction=history_obj.update_history(i)
            u=backward_induction(afteraction)
            if u<bu:
                bu=u
                bi=i
        strategy_dict_o["".join(map(str,history_obj.history))][str(bi)]=1
        return bu
    # TODO implement
    # (1) Implement backward induction for tictactoe
    # (2) Update the global variables strategy_dict_x or strategy_dict_o which are a mapping from histories to
    # probability distribution over actions.
    # (2a)These are dictionary with keys as string representation of the history list e.g. if the history list of the
    # history_obj is [0, 4, 2, 5], then the key is "0425". Each value is in turn a dictionary with keys as actions 0-8
    # (str "0", "1", ..., "8") and each value of this dictionary is a float (representing the probability of
    # choosing that action). Example: {”0452”: {”0”: 0, ”1”: 0, ”2”: 0, ”3”: 0, ”4”: 0, ”5”: 0, ”6”: 1, ”7”: 0, ”8”:
    # 0}}
    # (2b) Note, the strategy for each history in strategy_dict_x and strategy_dict_o is probability distribution over
    # actions. But since tictactoe is a PIEFG, there always exists an optimal deterministic strategy (SPNE). So your
    # policy will be something like this {"0": 1, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0} where
    # "0" was the one of the best actions for the current player/history.
    return -2
    # TODO implement


def solve_tictactoe():
    backward_induction(History())
    with open('./policy_x.json', 'w') as f:
        json.dump(strategy_dict_x, f)
    with open('./policy_o.json', 'w') as f:
        json.dump(strategy_dict_o, f)
    return strategy_dict_x, strategy_dict_o


if __name__ == "__main__":
    logging.info("Start")
    solve_tictactoe()
    logging.info("End")
