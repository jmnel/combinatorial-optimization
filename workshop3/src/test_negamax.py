from time import perf_counter
from typing import Tuple
from random import shuffle
from negamax import negamax_search
from common.time_utils import time_hr
from common.ticktack import *


def test_negamax_random_state():

    num_trials = 10

    for n in range(9):

        t_avg = 0.
        negamax_calls_avg = 0
        util_fn_evals_avg = 0

        for trial in range(num_trials):
            init_state = list(range(9))
            shuffle(init_state)
            init_state = init_state[:n]
            init_state = tuple(init_state)

            t_start = perf_counter()

            _, _, stats = negamax_search(init_state,
                                         util_fn=score_weighted,
                                         expand_fn=expand_basic)

            t_avg += perf_counter() - t_start
            util_fn_evals_avg += stats['util_fn_evals']
            negamax_calls_avg += stats['negamax_calls']

        t_avg /= num_trials
        util_fn_evals_avg /= num_trials
        negamax_calls_avg /= num_trials

        print(
            f'For n={9-n} available states, avg. statistics over {num_trials} runs:')
        print(f'  running time: {time_hr(t_avg)}')
        print(
            f'  negamax calls: {negamax_calls_avg}, util function calls: {util_fn_evals_avg}\n')
