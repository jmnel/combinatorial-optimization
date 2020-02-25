from time import perf_counter
from typing import Tuple
from random import shuffle
from alpha_beta import alpha_beta_search
from common.time_utils import time_hr
from common.ticktack import *
from common_ab import *


def alpha_beta_random_state():

    def two_player_score(state: Tuple[int, ...]):
        scr = score(state)
        if len(state) % 2 == 1:
            if scr is not None:
                scr = 1. - scr

        return scr

    num_trials = 20
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

            _, _, stats = alpha_beta_search(init_state,
                                            util_fn=two_player_score,
                                            expand_fn=expand,
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


alpha_beta_random_state()
