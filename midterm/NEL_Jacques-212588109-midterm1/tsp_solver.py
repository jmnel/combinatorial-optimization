from typing import Tuple
from functools import lru_cache
from time import perf_counter
import numpy as np


def tsp_solve(cities: np.array,
              initial_tour: Tuple[int, ...] = None,
              log_interval=5,
              lru_cache_size=128):
    """
    Solves the Traveling Salesman Problem using 2-opt edge swaps.

    Args:
        cities:             (x, y) coordinate pairs of cities.
        initial_tour:       starting tour (optional)
        log_interval:       verbose printing interval
        lru_cache_size:     LRU cache size 

    Returns:
        tuple:              tuple of optimum tour and length

    """

    # Verify that cities is n x 2 numpy array.
    if len(cities.shape) != 2 or cities.shape[1] != 2:
        raise ValueError('cities must by n x 2 np.array')

    num_cities = len(cities)

    # Generate initial tour by enumerating cities and concating 0.
    if initial_tour is None:
        initial_tour = tuple(i for i in range(num_cities)) + (0,)

    else:

        # Check for correct initial tour length.
        if len(initial_tour) != num_cities + 1:
            raise ValueError('initial_tour must by tuple of length n + 1')

    # Prebuild list of possible 2-opt (i, k) pairs.
    perms = list()
    for i in range(1, num_cities):
        for k in range(2, num_cities - i + 1):

            # Exclude case which only reverses tour.
            if not (i == 1 and k + 1 == num_cities):
                perms.append((i, k))

    def two_opt(tour, i, k):
        """Permutes tour by 2-opt permutation at position i of length k."""
        if i <= 0:
            raise ValueError('i must be > 0. Origin must be invariant.')
        if i + k >= len(tour):
            raise ValueError(
                'i + k must be < len(tour). Destination must be invariant.')
        if k < 2:
            raise ValueError(
                'k must be >= 2. k == 1 does not produce new tour.')
        if i == 1 and k + 2 == len(tour):
            raise ValueError(
                'i == 1 and k + 2 == len(tour) only reverses tour.')
        t = tour[0:i] + tuple(reversed(tour[i:i + k])) + tour[i + k:]

        return t

    @lru_cache(maxsize=lru_cache_size)  # LRU cached; 6x speedup
    def city_dist(ci0, ci1):
        """Calculates euclidean distances between 2 cities."""
        p0 = cities[ci0]
        p1 = cities[ci1]
        r = p0 - p1
        return np.linalg.norm(r)

        # d^2 not used, because it changes results.
    #    return np.dot(r, r)

    def tour_dist(tour):
        """Calculates total tour length by summing edges."""
        return sum((city_dist(tour[i], tour[i + 1]) for i in tour))

    # Initialize state and calculate f(sₖ).
    tour = initial_tour
    state_f = tour_dist(tour)

    # Start profiling timer.
    t_start = perf_counter()

    # 2-opt algorithm main loop.
    epoch = 0
    while True:

        # Enumerate all neighbor states { sₖ }.
        neighbor_tours = tuple(two_opt(tour, p[0], p[1]) for p in perms)

        # Do verbose log printing.
        log_interval = 5
        if epoch % log_interval == 0:
            print(f'Epoch {epoch}:')
            print(' f(sₖ) = {:.0f}'.format(state_f))

        # Calculate f(sₖ) for all neighbor states.
        neighbor_f = tuple(tour_dist(t) for t in neighbor_tours)

        # Calculate Δf = f(sₖ) - f ⃰ for neighbors.
        delta_f = tuple(fd - state_f for fd in neighbor_f)

        # Find neighbor state index k which minimizes Δf.
        k_min = np.argmin(delta_f)

        # Check termination condition; return on no improvement in Δf.
        if delta_f[k_min] >= 0.0:

            # Calculate elapsed time.
            t_elapsed = perf_counter() - t_start

            # Print solution.
            print('Solution found after {} epochs in {:.0f}ms.'.format(
                epoch, t_elapsed * 1e3))
            print('  Optimal tour length = {:.0f}'.format(
                state_f))

            # Return tuple of optimum tour and length to caller.
            return (tour, state_f)

        # Transition to new state and record new f(sₖ).
        tour = neighbor_tours[k_min]
        state_f = neighbor_f[k_min]

        # Increment epoch counter.
        epoch += 1
