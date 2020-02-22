from typing import Tuple
import numpy as np
import copy

init_state = list(
    [0, 0, 0,
     0, 0, 0,
     0, 0, 0])
#    [1, 0, 2,
#     0, 1, 2,
#     0, 0, 1])
#init_state = list([i for i in range(1, 10)])

print(init_state)


def calc_score(s):
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

    for p in range(1, 3):
        w = [p, p, p]

        for c in q:
            if c == w:
                print(f'player {p} wins')
                return (True, 10 * (1 if p == 1 else -1))

    return (False, 0)


def transitions_fn(s, player):
    actions = list()
    for i in range(9):
        if s[i] == 0:
            a = copy.deepcopy(s)
            a[i] = player
            actions.append(a)
    return actions


def max_value(s):
    print(f'max s =\n')
    print(f'{s}')
    done, score = calc_score(s)
    if done:
        return score

    v = float('-inf')

    for a in transitions_fn(s, 2):
        v = max(v, min_value(a))
    return v


def min_value(s):
    print(f'min s =\n')
    print(f'{s}')
    done, score = calc_score(s)
    if done:
        return score
    v = float('inf')

    for a in transitions_fn(s, 1):
        v = min(v, max_value(a))
    return v


def minimax(s):
    s_a = list([min_value(a) for a in transitions_fn(s, 1)])

    for a in s_a:
        print(s_a)

    return 'asfd'


minimax(init_state)
