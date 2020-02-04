#!/usr/bin/env python3

import astar
import numpy as np


def solve_pancakes_problem():
    """
    Sets up and solves the Pancake Sorting problem.

    Problem state is encoded by labeling pancakes from smallest to largest.
    Profiling metrics are returned to caller.
    """

    # Initialize initial state for A* algorithm.
    init_state = (1, 0, 3, 5, 2, 4)
    N = len(init_state)
    goal_state = tuple(reversed(range(N)))

    def flip_state(pos: int, state: tuple):
        """
        Creates new state by flipping all pancakes above index pos
        """

        N = len(state)

        if pos < 0 or pos + 1 >= N:
            raise IndexError('Invalid index to flip.')

        flipped_state = np.zeros(N)

        def flip_helper(i):
            if i < pos:
                return state[i]
            else:
                return state[N - i + pos - 1]
        flipped_state = tuple(flip_helper(i) for i in range(6))

        return flipped_state

    def h(state: tuple):
        """
        h(x) heuristic function which sums the distance of out-of-place
        pancakes from their correct position in goal-state.
        """
        N = len(state)
        return sum(
            abs(state[i] - (N - i - 1)) for i in range(N)
        )

    def expand_fn(state: tuple):
        """
        Generates child nodes by enumerating all possible flips at current
        state.
        """
        return list(flip_state(pos, state) for pos in range(5))

    # Call A* search algorithm and return profiling metrics.
    return astar.astar_search(init_state=init_state,
                              expand_fn=expand_fn,
                              heuristic_fn=h)
