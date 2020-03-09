from time import perf_counter
from typing import Tuple
from random import shuffle
from minimax import minimax_search
from common.time_utils import time_hr
from common.ticktack import *


def test_minimax_random_state():

    num_trials = 10
    epochs = 200

    for n in range(9):

        t_avg = 0.
        minimax_calls_avg = 0
        util_fn_evals_avg = 0

        for trial in range(num_trials):
            init_state = list(range(9))
            shuffle(init_state)
            init_state = init_state[:n]
            init_state = tuple(init_state)

            t_start = perf_counter()

            _, _, stats = minimax_search(init_state,
                                         util_fn=score_weighted,
                                         expand_fn=expand_basic,
                                         randomize=True)

            t_avg += perf_counter() - t_start
            util_fn_evals_avg += stats['util_fn_evals']
            minimax_calls_avg += stats['minimax_calls']

        t_avg /= num_trials
        util_fn_evals_avg /= num_trials
        minimax_calls_avg /= num_trials

        print(
            f'For n={n} available states, avg. statistics over {num_trials} runs:')
        print(f'  running time: {time_hr(t_avg)}')
        print(
            f'  minimax calls: {minimax_calls_avg}, util function calls: {util_fn_evals_avg}\n')
