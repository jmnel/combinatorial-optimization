from time import perf_counter
from typing import Callable, Tuple
from common.util import argmax
from common.ticktack import *


def negamax_search(init_state: Tuple[int, ...],
                   util_fn: Callable[[Tuple[int, ...]], float],
                   expand_fn: Callable[[Tuple[int, ...]], Tuple[int, ...]]):
    """
    Finds optimal child state using negamax algorithm.

    Args:
        init_state:         initial state from which to search
        util_fn:            callable which calculates a given state's score
        expand_fn:          callable which gives state's children

    Returns:
        Tuple containing optimal node, its value, and profiling statistics.

    """

    # Initialize profiling counter.
    stats = {'negamax_calls': 0, 'util_fn_evals': 0}

    # Start profiling counter.
    t_start = perf_counter()

    state = init_state

    def _negamax(state, flip):
        """
        Inner recursive helper function.
        """

        # Update profiling statistics counter.
        stats['negamax_calls'] += 1
        stats['util_fn_evals'] += 1

        # Get score of current state.
        score = util_fn(state)

        # Return flipped score if it is terminal.
        if score is not None:
            return score * flip

        # Expand node's children.
        children = expand_fn(state)

        # Call helper on children.
        v = (-_negamax(child, -flip) for child in children)

        # Return highest score.
        return max(v)

    # We calculate flip based on current length of state.
    flip = 1 if len(state) % 2 == 0 else -1

    # Expand root state's children.
    children = expand_fn(state)

    # Calculate v scores for children.
    v_children = tuple((-_negamax(child, -flip), child) for child in children)

    # Find child with best score.
    vc_best = (float('-inf'),)
    for v_child in v_children:
        if v_child > vc_best:
            vc_best = v_child

    # Determine elapsed time.
    stats['elapsed_time'] = perf_counter() - t_start

    # Return optimal state, its score, and profiling statistics to caller.
    return (vc_best[1], vc_best[0], stats)
