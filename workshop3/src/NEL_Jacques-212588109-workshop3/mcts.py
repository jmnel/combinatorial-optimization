from __future__ import annotations
from typing import Tuple, List
from random import randint
from time import perf_counter
import numpy as np
from common.util import argmax
from common.ticktack import *


class Node:
    parent: Node = None                 # node's parent
    state: Tuple[int, ...] = None       # state of node
    q: float = 0.0                      # simulated reward of node
    n: int = 0                          # visit count of node
    a_incoming: int = None              # incoming action which created node
    a_collapsed: List[int] = list()     # unexplored actions at node
    children: List[Node] = list()       # explored children of node

    def __init__(self,
                 state: Tuple[int, ...],
                 parent: type(self) = None,
                 a_incoming: int = None):
        """Constructs node for MCTS tree."""

        self.parent = parent
        self.state = state
        self.a_incoming = a_incoming
        self.children = list()

        # Unexplored actions are the set difference {0,...9} - {x for x in state}.
        self.a_collapsed = list([a for a in set(range(9)) - set(state)])

    def __str__(self):
        s = 'Node object:\n'
        s += f'  parent={self.parent.__repr__()}\n'
        s += f'  state={self.state}\n'
        s += f'  a_incoming={self.a_incoming}\n'
        s += f'  a_collapsed={self.a_collapsed}\n'
        s += f'  children={len(self.children)}\n'
        s += f'  q={self.q}\n'

        return s


def uct_search(init_state,
               util_fn: Callable[[Tuple[int, ...]], float],
               selection_criteria: str = 'max_child',
               exploration_bias: float = 1. / np.sqrt(2.),
               max_epochs: int = 200,
               max_robust_min_epochs: int = 20):
    """
    Performs Monte Carlo tree search using UCT method to find optimal next state.

    Args:
        init_state:             initial root state from which to make choice
        util_fn:                score calculation function
        selection_criteria:     choice of 'max_child', 'robust_child', 'max_rebust_child',
                                or 'secure_child'
        exploration_bias:       bias which determines propensity to expand nodes
        max_epochs:             maximum number of epochs to perform
        max_robust_min_epochs:  number of epochs before testing max-robust selection criteria;
                                only applies to max-robust method

    Returns:
        Tuple with optimal state, estimated score, and profiling statistics

    """

    # This will store some profiling statistics.
    stats = {'explored_count': 0,
             'visit_count': 0,
             'util_fn_evals': 0,
             'simulation_time': 0}

    # Start profiling timer.
    t_start = perf_counter()

    def tree_policy(v: Node) -> Node:
        """
        Traverses tree by expanding unexplored nodes, and / or selects children with maximal
        UCT until terminal state is encountered.
        """

        # Loop while v is non-terminal.
        while len(v.state) < 9:

            # Expand and return v if it is unexplored.
            if len(v.a_collapsed) > 0:
                return expand(v)

            # Otherwise, return v's most promising child.
            else:
                v = best_child(v, exploration_bias)

        return v

    def default_policy(state: Tuple[int, ...]):
        while True:

            # Evaluate utility function.
            scr = util_fn(state)

            # Update profiling statistics.
            stats['util_fn_evals'] += 1

            if scr != None:
                break

            a = tuple(set(range(9)) - set(state))[randint(0, 8 - len(state))]
            state = state + (a,)

        return scr

    def expand(v):
        """
        Expands a given node with available action and adds new child to parent.
        """

        # Update profiling statistics.
        stats['explored_count'] += 1

        assert(len(v.a_collapsed) > 0)

        # Pick a unexplored action from v.
        a = v.a_collapsed.pop(0)

        # Create new child for v with action a.
        v_new = Node(state=v.state + (a,),
                     parent=v,
                     a_incoming=a)

        # Append new node to parent's list of children.
        v.children.append(v_new)

        return v_new

    def best_child(v: Node, c):
        """Selects child node which maximises UCT function."""

        best_uct_child = (float('-inf'), None)
        for child in v.children:

            # Calculate average expected reward for child.
            q_bar = child.q / child.n

            # Calculate UCT function for child.
            uct = q_bar + c * np.sqrt(2.0 * np.log(v.n) / child.n)

            # Update best child.
            if (uct,) > best_uct_child:
                best_uct_child = (uct, child)

        return best_uct_child[1]

    def backup(v: Node, delta):
        """Traverses tree from child to parent, propogating count and score."""

        # Iterate until root node is encountered.
        while v is not None:

            # Increment visit count.
            v.n += 1

            # Update profiling statistics.
            stats['visit_count'] += 1

            # Propogate score.
            v.q += delta

            # Go to parent next.
            v = v.parent

    # Handle selection criteria a.1 max-child, a.2 robust-child, and a.3 secure-child.
    if selection_criteria == 'max' or 'robust' or 'secure':

        root = Node(state=init_state)

        # Perform MCTS algorithm main loop.
        for epoch in range(max_epochs):

            vl = tree_policy(root)

            sim_t_start = perf_counter()
            delta = default_policy(vl.state)
            stats['simulation_time'] += perf_counter() - sim_t_start

            backup(vl, delta)

        # This helper extracts appropriate value from child depending on selection criteria.
        def crit_selector(crit: str, child: Node):

            if crit == 'max':
                # Return reward for max-child criteria.
                return child.q

            elif crit == 'robust':
                # Return visit-count for robust-child criteria.
                return child.n

            else:
                # Calculate and return UCT for secure-child criteria.
                uct = child.q / child.n + exploration_bias * \
                    np.sqrt(2. * np.log(root.n) / child.n)
                return uct

        # Return state of optimal child to caller.
        optim_child = root.children[
            argmax(
                (crit_selector(selection_criteria, c)
                 for c in root.children))
        ]

        optim_score = crit_selector(selection_criteria, optim_child)
        stats['t_elapsed'] = t_start - perf_counter()

        return (optim_child.state, optim_score, stats)

    # Handle selection criteria b max-robust-child.
    elif selection_criteria == 'max_robust':

        root = Node(state=init_state)

        # Perform MCTS algorithm main loop; max-robust variant.
        for epoch in range(max_epochs):

            vl = tree_policy(root)
            delta = 1.0 - default_policy(vl.state)
            backup(vl, delta)

            # Start testing max-robust selection criteria after minimum epochs.
            if epoch > max_robust_min_epochs:

                # Determine index of child with maximum reward.
                q_max = argmax((c.q for c in root.children))

                # Determine index of child with maximum visit count.
                n_max = argmax((c.n for c in root.children))

                # If above 2 indices agree, return state of optimal node to caller.
                if q_max == n_max:

                    optim_child = root.children[q_max]
                    optim_score = (optim_child.q, optim_child.n)
                    stats['t_elapsed'] = t_start - perf_counter()

                    return (optim_child.state, optim_score, stats)

    # Selection criteria is invalid.
    else:
        # Throw exception.
        raise ValueError(
            'selection_criteria must be one of \'max\', \'robust\', \'max_robust\', or \'secure\'.')
