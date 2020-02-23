from typing import Tuple
import numpy as np
import copy

init_state = list(
    #    [0, 0, 0,
    #     0, 0, 0,
    #     0, 0, 0])
    [-1, 0, 1,
     0, 1, -1,
     0, 0, 0])
#init_state = list([i for i in range(1, 10)])

# print(init_state)


def draw_state(s):

    s_e = list([' ' if e == 0 else 'x' if e == -1 else 'o' for e in s])

    s_str = ' {} │ {} │ {} \n'
    s_str += '───┼───┼───\n'
    s_str += ' {} │ {} │ {} \n'
    s_str += '───┼───┼───\n'
    s_str += ' {} │ {} │ {} \n'

    s_str = s_str.format(*s_e)
    print(s_str)


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

    for p in (-1, 1):
        w = [p, p, p]

        for c in q:
            if c == w:
                #                print(f'player {p} wins')
                return (True, 10 * p)

    return (False, 0)


def transitions_fn(s, player):
    actions = list()
    for i in range(9):
        if s[i] == 0:
            a = copy.deepcopy(s)
            a[i] = player
            actions.append(a)
    return actions


def max_value(s, p):
    #    print(f'max s =\n')
    #    print(f'{s}')
    done, score = calc_score(s)
    if done:
        return score

    v = float('-inf')

    for a in transitions_fn(s, -p):
        v = max(v, min_value(a, p))
    return v


def min_value(s, p):
    #    print(f'min s =\n')
    #    print(f'{s}')
    done, score = calc_score(s)
    if done:
        return score
    v = float('inf')

    for a in transitions_fn(s, -p):
        v = min(v, max_value(a, p))
    return v


def minimax(s, p):

    print(f'Player {p}\'s turn:')

    actions = transitions_fn(s, p)

    s_a = list([(a, min_value(a, p)) for a in actions])
#    s_a = list([(a, min_value(a) if player == 1 else min_value(a))
#                for a in actions])

    for a in s_a:
        print(a[1])
        draw_state(a[0])


print('init state:')
draw_state(init_state)

minimax(init_state, -1)
