from typing import Tuple


def state_to_board(state: Tuple[int, ...]):
    board = [' '] * 9

    mark = 'x'
    for mv in state:
        board[mv] = mark
        mark = 'o' if mark == 'x' else 'x'

    return board


def state_to_str(state: Tuple[int, ...]):
    board = state_to_board(state)
    s_str = ' {} │ {} │ {} \n'
    s_str += '───┼───┼───\n'
    s_str += ' {} │ {} │ {} \n'
    s_str += '───┼───┼───\n'
    s_str += ' {} │ {} │ {} \n'
    return s_str.format(*board)


def score_weighted(state: Tuple[int, ...]):
    """
    Score function which results positive score for P1 win and negative for P2 win.
    The score is weighted to favour earlier wins.
    """

    # Convert set of moves to board form.
    board = state_to_board(state)

    # Take slices of board by rows.
    rows = tuple(tuple(board[3 * i: 3 * (i + 1)]) for i in range(3))

    # Take slices of board by columns.
    cols = tuple(tuple(board[i:9:3]) for i in range(3))

    # Take slices of 2 diagonals.
    diag1 = tuple(board[0:9:4])
    diag2 = tuple(board[2:7:2])

    # Collect all 3-sequences to check for winning combinations.
    win_seq = (*rows, *cols, diag1, diag2)

    # Check if any sequence wins for player x or player o.
    p1_win = any(s == ('x',) * 3 for s in win_seq)
    p2_win = any(s == ('o',) * 3 for s in win_seq)

    if p1_win:
        # x win results in positive score; discounted by number of moves.
        return (10. - len(state))

    elif p2_win:
        # o win results in negative score; discounted by number of moves.
        return -(10. - len(state))

    if len(state) == 9:
        # A draw results in score of 0.
        return 0.

    else:
        # Otherwise, a terminal state has not been reached.
        return None


def score_mcts(state: Tuple[int, ...]):
    """
    Score function which results positive score for P1 win and negative for P2 win.
    The score lies in range [0, 1].
    """

    # Convert set of moves to board form.
    board = state_to_board(state)

    # Take slices of board by rows.
    rows = tuple(tuple(board[3 * i: 3 * (i + 1)]) for i in range(3))

    # Take slices of board by columns.
    cols = tuple(tuple(board[i:9:3]) for i in range(3))

    # Take slices of 2 diagonals.
    diag1 = tuple(board[0:9:4])
    diag2 = tuple(board[2:7:2])

    # Collect all 3-sequences to check for winning combinations.
    win_seq = (*rows, *cols, diag1, diag2)

    # Check if any sequence wins for player x or player o.
    p1_win = any(s == ('x',) * 3 for s in win_seq)
    p2_win = any(s == ('o',) * 3 for s in win_seq)

    if p1_win:
        # x win results in positive score; discounted by number of moves.
        return 1.0

    elif p2_win:
        # o win results in negative score; discounted by number of moves.
        return 0.0

    if len(state) == 9:
        # A draw results in score of 0.
        return 0.5

    else:
        # Otherwise, a terminal state has not been reached.
        return None


def two_player_score(state: Tuple[int, ...]):
    """Calculates two player in range [0,1]."""
    scr = score_mcts(state)
    if len(state) % 2 == 1:
        if scr is not None:
            scr = 1. - scr

    return scr


def expand_basic(state):
    """
    Simple function which returns child states by appending an available move to 
    current state.
    """
    assert(len(state) < 9)

    # Calculte set difference to get remaining moves.
    n = tuple(set(range(9)) - set(state))

    # Create tuple of available new states and return to caller.
    c = tuple(state + (q,) for q in n)
    return c
