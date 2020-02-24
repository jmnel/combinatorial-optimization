from time import perf_counter
from random import shuffle
from typing import Callable, Tuple


def minimax_search(state: Tuple[int, ...],
                   util_fn: Callable[[Tuple[int, ...]], float],
                   expand_fn: Callable[[Tuple[int, ...]], Tuple[int, ...]],
                   randomize: bool = False):
    """
    Picks optimal child state using minimax algorithm.

    Args:
        state:      initial state from which to search
        util_fn:    utility function
        expand_fn:  function which enumerates children
        randomize:  enables random shuffle

    Returns:
        tuple:      tuple of optimal state, best estimate of utility, and internal statistics

    """

    # This counter tracks number of calls to internal helper function.
    stats = {'minimax_calls': 0}

    # Start profiling timer.
    t_start = perf_counter()

    # This helper function is called recursively to estimate bounds of score for a state's chidren.
    # This is the heart of the α-β prunning algorithm.
    def _minimax(state: Tuple[int, ...], is_max_turn: bool):

        # Increment helper call statistics.
        nonlocal stats
        stats['minimax_calls'] += 1

        # Determine utility of current state.
        score = util_fn(state)

        # Utility function returns value for terminal leaves in search tree.
        if score != None:
            return (score, None)

        # Expand current node.
        actions = expand_fn(state)

        # Shuffle children if randomize is enabled.
        if randomize:
            actions_l = list(actions)
            shuffle(actions_l)
            actions = tuple(actions_l)

        # Keep track of best v score and associated child action.
        best_v = float('-inf') if is_max_turn else float('inf')
        best_action = None

        # Loop through children.
        for a in actions:

            # Call recursive helper on child.
            child_v, child_action = _minimax(
                a, not is_max_turn)

            # If it's max's turn and better child found, do the following:
            if is_max_turn and best_v < child_v:
                best_v = child_v
                best_action = a

            # If it's min's turn and better child found, do the following:
            elif not is_max_turn and best_v > child_v:
                best_v = child_v
                best_action = a

        return (best_v, best_action)

    # Max goes 1st, then min, then so forth...
    is_max_turn = len(state) % 2 == 0

    # Call helper on current state.
    best_v, best_action = _minimax(state, is_max_turn)

    # Update elapsed time performance timer.
    stats['t_elapsed'] = perf_counter() - t_start

    # Return optimal choice, its score, and statistics to caller.
    return (best_action, best_v, stats)
