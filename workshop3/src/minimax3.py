from typing import Tuple
from ast import literal_eval as make_tuple
from time import perf_counter
from time_utils import time_hr

from ticktack import *
from util import argmax


def minimax_decision(moves: Tuple[int, ...], player):

    max_calls = 0
    min_calls = 0

    t_start = perf_counter()

    def max_value(moves: Tuple[int, ...]):
        nonlocal max_calls
        max_calls += 1
        done, score = calc_score(moves, player)
        if done:
            return score
        v = float('-inf')

        actions = transitions_fn(moves)
        for a in actions:
            v = max(v, min_value(a))

        return v

    def min_value(moves: Tuple[int, ...]):
        nonlocal min_calls
        min_calls += 1
        done, score = calc_score(moves, player)
        if done:
            return score
        v = float('inf')

        actions = transitions_fn(moves)
        for a in actions:
            v = min(v, max_value(a))

        return v

    actions = transitions_fn(moves)

    v = tuple(min_value(a) for a in actions)

    i_best = argmax(v)

    print('minimax: {}\n\t{} min_value calls\n\t{} max_value calls\n'.format(
        time_hr(perf_counter() - t_start), min_calls, max_calls))

    return actions[i_best]


s = tuple()

print(board_to_str(s))

for turn in range(9):

    if turn % 2 == 1:
        print('Computer\'s turn:\n')
        s = minimax_decision(s, 'o')

    else:
        print('Human\'s turn:\n')

        choice = make_tuple(input())

        assert(isinstance(choice, tuple))
        assert(len(choice) == 2)
        m = choice[0] * 3 + choice[1]
        assert(m >= 0)
        assert(m < 9)
        assert(s.count(m) == 0)

        s = s + (m,)

    print(board_to_str(s))

    done, score = calc_score(s, 'o')
    if done:
        break

_, score = calc_score(s, 'o')
if score > 0:
    print('Computer wins!')
elif score == 0:
    print('Draw!')
else:
    print('Human wins!')
