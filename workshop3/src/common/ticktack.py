from typing import Tuple


def make_board(moves: Tuple[int, ...]):
    board = [0, ] * 9

    p = -1
    for m in moves:
        board[m] = p
        p *= -1

    return board


def moves_to_str(moves: Tuple[int, ...]):
    moves_str = (str(m) for m in moves)
    return '->'.join(moves_str)


def board_to_str(moves: Tuple[int, ...]):

    board = make_board(moves)

    s_e = (' ' if e == 0 else 'x' if e == -1 else 'o' for e in board)

    s_str = ' {} │ {} │ {} \n'
    s_str += '───┼───┼───\n'
    s_str += ' {} │ {} │ {} \n'
    s_str += '───┼───┼───\n'
    s_str += ' {} │ {} │ {} \n'

    return s_str.format(*s_e)


def calc_score(moves: Tuple[int, ...], player):

    s = make_board(moves)
    q = list()
    for i in range(3):
        r = s[i * 3:i * 3 + 3]
        c = s[i:9:3]
        q.append(r)
        q.append(c)
    d1 = s[0:9:4]
    d2 = s[2:7:2]
    q.append(d1)
    q.append(d2)

    f = 1 if player == 'x' else -1

    for p in (-1, 1):
        w = [p, p, p]

        for c in q:
            if c == w:
                return (True, (20 - len(moves)) * p * f)

    return (s.count(0) == 0, 0)


def transitions_fn(moves: Tuple[int, ...]):
    n = tuple(set(range(9)) - set(moves))

    c = tuple(moves + (q,) for q in n)
    return c
