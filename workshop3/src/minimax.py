from typing import Tuple, Callable
from time import perf_counter
from time_utils import time_hr

from util import argmax
from ticktack import *


def minimax_search(state,
                   util_fn,
                   termination_fn,
                   transitions_fn):

    def max_value(state):
        if termination_fn(state):
            return util_fn(state)

        v = float('-inf')

        neighbors = transitions_fn(state)
#        print('max_value')
        for n in neighbors:
            v = max(v, min_value(n))
#            print(f'  {v}  :  {n}')

        return v

    def min_value(state):
        if termination_fn(state):
            return util_fn(state)

        v = float('inf')

        neighbors = transitions_fn(state)
#        print('min_value')
        for n in neighbors:
            v = min(v, max_value(n))
#            print(f'  {v}  :  {n}')

        return v

    t_start = perf_counter()

    neighbors = transitions_fn(state)

    v = tuple(max_value(n) for n in neighbors)

    i_optim = argmax(v)

    print('minimax: {}'.format(
        time_hr(perf_counter() - t_start)))

    return neighbors[i_optim]


def util_fn(state):

    board = make_board(state)

    check_seq = list()
    for i in range(3):
        row = board[i * 3:i * 3 + 3]
        col = board[i:9:3]
        check_seq.append(row)
        check_seq.append(col)
    diag1 = board[0:9:4]
    diag2 = board[2:7:2]
    check_seq.append(diag1)
    check_seq.append(diag2)

    for p in (-1, 1):
        w = [p] * 3

        for s in check_seq:
            if s == w:
                return -10. * p

    return 0.


def transitions_fn(state: Tuple[int, ...]):
    nodes = tuple(set(range(9)) - set(state))
    neighbors = tuple(state + (n,) for n in nodes)
    return neighbors


def term_fn(state):
    return len(state) == 9


def util_flip(state):
    return util_fn(state)


s = (0, 2, 4)

print()
print(board_to_str(s))

a = minimax_search(s, util_fn=util_flip,
                   termination_fn=term_fn,
                   transitions_fn=transitions_fn)

print(board_to_str(a))
