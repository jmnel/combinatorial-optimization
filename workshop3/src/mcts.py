from typing import Tuple


def state_to_board(state):


def state_to_str(state):
    board = state_to_board(state)
    s_str = ' {} │ {} │ {} \n'
    s_str += '───┼───┼───\n'
    s_str += ' {} │ {} │ {} \n'
    s_str += '───┼───┼───\n'
    s_str += ' {} │ {} │ {} \n'
    return s_str.format(*board)


def score(state):
    board = state_to_board(state)
    rows = tuple(tuple(board[3 * i: 3 * (i + 1)]) for i in range(3))
    cols = tuple(tuple(board[i:9:3]) for i in range(3))
    diag1 = tuple(board[0:9:4])
    diag2 = tuple(board[2:7:2])

    win_seq = (*rows, *cols, diag1, diag2)
    p1_win = any(s == ('x',) * 3 for s in win_seq)
    p2_win = any(s == ('o',) * 3 for s in win_seq)

    if p1_win:
        return (10 - len(state))
    elif p2_win:
        return -(10 - len(state))

    if len(state) == 9:
        return 0
    else:
        return None


def non_terminal(state):
    return len(state) < 9


class MctsState:
    moves = tuple()

    def __init__(self, moves: Tuple = tuple()):
        self.moves = moves

    def __repr__(self):
    board = [' '] * 9

    mark = 'x'
    for mv in state:
        board[mv] = mark
        mark = 'o' if mark == 'x' else 'x'

    return board
        board = state_to_board(state)
        s_str = ' {} │ {} │ {} \n'
        s_str += '───┼───┼───\n'
        s_str += ' {} │ {} │ {} \n'
        s_str += '───┼───┼───\n'
        s_str += ' {} │ {} │ {} \n'
        return s_str.format(*board)


class MctsNode:
    parent = None
    expanded_children = list()
    collapsed_children = list()
    state = None

    def __init__(self, parent, state):
        self.parent = parent
        self.state = state


def actions(state: MctsState):
    played_moves = (

def expand(node):
    pass
#    assert(len(state) < 9)
#    n = tuple(set(range(9)) - set(state))
#    c = tuple(state + (q,) for q in n)
#    return c


def tree_policy(note: MctsNode):
    pass


def mcts_search(init_state):

    root=MctsNode(state=init_state, parent=None)
