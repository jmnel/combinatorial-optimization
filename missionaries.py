#!/usr/bin/env python3

import astar
from enum import Enum


def solve_missionaries_cannibals_prob():
    """
    Solves the Missionaries and Canibals problem.

    The state is encoded by counting the number of missionaries and canibals
    on the left (final) bank. The location of the boat is also tracked by a 1 or 0.
    """

    def h(state: tuple):
        """
        h(x) heuristic which simply counts the number of missionaries and canibals on the
        destination left bank.
        """
        return 6 - state[0] - state[1]

    def mc_expand(state: tuple):
        """
        Generates child nodes by evaluating all possible moves, then filtering by
        rules of the puzzle.
        """

        # Boat state is at index 2 of tuple; 1 indicates boat is on left bank.
        boat = state[2]

        # Missionaries on left bank.
        m_left = state[0]

        # Missionaries on right bank.
        m_right = 3 - m_left

        # Canibals on left bank.
        c_left = state[1]

        # Canibals on right bank.
        c_right = 3 - c_left

        # Next look at all posibilities of missionaries and canibals traveling by boat
        # across river with boat that has capacity for only 2 people.
        children = list()

        # Case 1: boat is on right bank.
        if boat is 0:
            children = [
                (m_left + 2,    c_left,     1),     # 2M go to left bank.
                (m_left + 1,    c_left + 1, 1),     # 1M & 1C go to left bank.
                (m_left,        c_left + 2, 1),     # 2C go to left bank.
                (m_left + 1,    c_left,     1),     # 1M goes to left bank.
                (m_left,        c_left + 1, 1)      # 1C goes to left bank.
            ]

        # Case 2: boat is on left bank.
        else:
            children = [
                (m_left - 2,    c_left,     0),     # 2M go to right bank.
                (m_left - 1,    c_left - 1, 0),     # 1M & 1C go to right bank.
                (m_left,        c_left - 2, 0),     # 2C go to right bank.
                (m_left - 1,    c_left,     0),     # 1M goes to right bank.
                (m_left,        c_left - 1, 0)      # 1C goes to right bank.
            ]

        # Rule A: number of M and C must be non-negative and add up to 3.
        def non_negative_rule(state: tuple):
            return (state[0] >= 0 and
                    state[1] >= 0 and
                    state[0] <= 3 and
                    state[1] <= 3)

        # Rule B: if a bank has M > 0, M >= C otherwise C eats M.
        def dont_eat_me_rule(state: tuple):
            m_left = state[0]
            m_right = 3 - m_left
            c_left = state[1]
            c_right = 3 - c_left
            return ((m_left >= c_left or m_left is 0) and
                    (m_right >= c_right or m_right is 0))

        # Filter to feasible child states by applying rule A and B.
        return list(filter(lambda s: non_negative_rule(s)
                           and dont_eat_me_rule(s),
                           children))

    # Initial state of puzzle is 3 missionaries, 3 canibals, and boat on right bank.
    init_state = (0, 0, 0)

    # Run A* search algorithm and return profiling metrics to caller.
    return astar.astar_search(init_state=init_state,
                              expand_fn=mc_expand,
                              heuristic_fn=h)
