#!/usr/bin/env python3

import astar
import numpy as np
from copy import deepcopy


def solve_hanoi_problem():
    """
    Sets up and solves 2-color Towers of Hanoi problem.

    Problem state is encoded by enumerating black and white discs by size.
    Black disks are 0-3 and white ones are 4-7. These values are kept in
    a 3-tuple of tuples of varying sizes which denote peg A, B, and via.
    """

    # This is the initial state of the game as depicted on Wikipedia.
    init_state = (
        (4, 1, 6, 3),
        (0, 5, 2, 7),
        ()
    )

    # The goal state is to have black discs in order on left peg, and white
    # discs on middle peg in order.
    goal_state = (
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        ()
    )

    def draw_state(state: tuple):
        """
        Draws a state using unicode block drawing characters.
        """

        print(state)

        s = state[0]

        width = 19
        px = list()

        rows = list()
        for i_row in range(6):
            row = ''
            for j_peg in range(3):

                if i_row < len(state[j_peg]):
                    d = state[j_peg][i_row]
                    char = '█' if d // 4 else '░'
                    sz = 14 - 4 * (d % 4) + 1
                    for k in range((width - sz) // 2):
                        row += ' '
                    for k in range(sz):
                        row += char
                    for k in range((width - sz) // 2):
                        row += ' '
                else:
                    for k in range(width):
                        row += ' '
            rows.append(row)

        rows.reverse()
        rows.append('')
        rows.append('       Peg A              Peg B             Peg Via')
        rows.append('')
        for row in rows:
            print(row)

    def hanoi_disk_dist(state: tuple):
        """
        h(x) heuristic function which sums the sum of out of order disc distances
        and 1 for wrong peg or 0 for correct peg.

        Note: This heuristic does not perform very well, but the solution is found
        after excessive iterations.
        """

        dist = 0
        for i_peg in range(3):
            s_peg = state[i_peg]
            for i_disk in range(len(s_peg)):
                # This is penality for disk on incorrect peg.
                peg_dist = np.sign(abs(s_peg[i_disk] // 4 - i_peg))

                # This is the absolute height distance from a disc to its correct
                # height.
                row_dist = abs(s_peg[i_disk] % 4 - i_disk)

                # The two preceding values are simply summed together.
                dist += peg_dist + row_dist

        return dist

    def hanoi_expand(state: tuple):
        """
        Generates child nodes by evaluating all possible moves at each game
        state, while obeying the rules of the game.
        """

        # Indices to the current state elements.
        perm = tuple([state[i][j] for j in range(len(state[i]))]
                     for i in range(3))

        perms = list()
        for i in range(3):
            # Compute a set of pairwise indices from peg i to j with i != j.
            for j in set(range(3)).difference({i}):
                p = deepcopy(perm)
                # If a peg contains at least one disc,
                if len(p[i]) > 0:

                    # remove the top disc's index,
                    loc = p[i].pop()

                    # and append it to the new peg.
                    p[j].append(loc)

                    # Convert this to a tuple and append to permutations.
                    p = tuple(tuple(v for v in x) for x in p)
                    perms.append(p)

        def size_rule(s: state):
            """
            Helper function to ensure that discs are only stacked on top of larger discs.
            """
            for s_peg in s:
                # If a peg contains a disc,
                if len(s_peg) > 1:
                    # calculate size of top and bottom discs.
                    sz_top = s_peg[-1] % 4
                    sz_below = s_peg[-2] % 4

                    # Otherwise, this state is invalid.
                    if sz_below > sz_top:
                        return False
            return True

        # Use above rule to filter permutation list.
        perms = list(filter(size_rule, perms))

        return perms

    # Sanity check: h(x*) should be 0 for goal state x*.
    assert(hanoi_disk_dist(goal_state) == 0)

    # Run A* search algorithm and return profiling metrics to caller.
    return astar.astar_search(init_state=init_state,
                              expand_fn=hanoi_expand,
                              heuristic_fn=hanoi_disk_dist,
                              epochs=1000000,
                              print_fn=draw_state)


solve_hanoi_problem()
