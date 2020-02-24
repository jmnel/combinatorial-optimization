from alpha_beta import alpha_beta_search


def state_to_board(state):
    board = [' '] * 9

    mark = 'x'
    for mv in state:
        board[mv] = mark
        mark = 'o' if mark == 'x' else 'x'

    return board


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


def expand(state):
    assert(len(state) < 9)
    n = tuple(set(range(9)) - set(state))
    c = tuple(state + (q,) for q in n)
    return c


s = ()
print(state_to_str(s))

while True:

    scr = score(s)
    if scr is None:
        s, _, stats = alpha_beta_search(s,
                                        util_fn=score,
                                        expand_fn=expand,
                                        randomize=True)
        print(state_to_str(s))
    elif scr > 0:
        print('Player x wins!')
        break
    elif scr < 0:
        print('Player o wins!')
        break
    else:
        print('Draw!')
        break
