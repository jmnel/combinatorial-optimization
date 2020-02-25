from time import perf_counter
from typing import Tuple
from random import shuffle
from mcts import uct_search
from common.time_utils import time_hr
from common.ticktack import *


def mcts_random_state():

    def score(state: Tuple[int, ...]):
        board = state_to_board(state)
        rows = tuple(tuple(board[3 * i: 3 * (i + 1)]) for i in range(3))
        cols = tuple(tuple(board[i:9:3]) for i in range(3))
        diag1 = tuple(board[0:9:4])
        diag2 = tuple(board[2:7:2])

        win_seq = (*rows, *cols, diag1, diag2)
        p1_win = any(s == ('x',) * 3 for s in win_seq)
        p2_win = any(s == ('o',) * 3 for s in win_seq)

        if p1_win:
            return 1.
        elif p2_win:
            return 0.
        elif len(state) == 9:
            return 0.5
        else:
            return None

    def two_player_score(state: Tuple[int, ...]):
        scr = score(state)
        if len(state) % 2 == 1:
            if scr is not None:
                scr = 1. - scr

        return scr

    num_trials = 100
    epochs = 200

    for n in range(9):

        t_avg = 0.
        explore_count_avg = 0
        visit_count_avg = 0
        util_fn_evals_avg = 0
        sim_time_avg = 0

        for trial in range(num_trials):
            init_state = list(range(9))
            shuffle(init_state)
            init_state = init_state[:n]
            init_state = tuple(init_state)

            t_start = perf_counter()

            _, _, stats = uct_search(init_state,
                                     util_fn=two_player_score,
                                     selection_criteria='max_child',
                                     max_epochs=epochs)

            t_avg += perf_counter() - t_start
            explore_count_avg += stats['explored_count']
            visit_count_avg += stats['visit_count']
            util_fn_evals_avg += stats['util_fn_evals']
            sim_time_avg += stats['simulation_time']

        t_avg /= num_trials
        explore_count_avg /= num_trials
        visit_count_avg /= num_trials
        util_fn_evals_avg /= num_trials
        sim_time_avg /= num_trials

        print(
            f'For n={n} available states, avg. statistics over {num_trials} runs:')
        print(
            f'  running time: {time_hr(t_avg)}, simulation time: {time_hr(sim_time_avg)}')
        print(
            f'  explore count: {explore_count_avg}, visit count: {visit_count_avg},', end='')
        print(f'  util. function evals: {util_fn_evals_avg}\n')


mcts_random_state()
