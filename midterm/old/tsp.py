from typing import Tuple

import numpy as np
import matplotlib
matplotlib.use('GTK3Cairo')
import matplotlib.pyplot as plt
import random
from time import perf_counter
from functools import lru_cache

from dj38_loader import DJ38Loader

num_cities = 100
cities = np.array([np.random.randn(2) for i in range(num_cities)])

cities = DJ38Loader().dataset
num_cities = len(cities)

print(f'num_cites={num_cities}')
print(cities[0])

lru_cache_size = 1024

random.seed(0)

# cities = np.array([[np.cos(i * 2 * np.pi / num_cities),
#                    np.sin(i * 2 * np.pi / num_cities)] for i in range(num_cities)])

tour = tuple(i for i in range(num_cities))
tour = tour + (0,)


def two_opt(tour, i, k):
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


# Prebuild list of possible 2-opt (i, k) pairs.
perms = list()
for i in range(1, num_cities):
    for k in range(2, num_cities - i + 1):

        # Exclude case which only reverses tour.
        if not (i == 1 and k + 1 == num_cities):
            perms.append((i, k))

# shuffle few times.
# for i in range(50002):
#    p = perms[random.randint(0, len(perms) - 1)]
#    tour = two_opt(tour, p[0], p[1])


@lru_cache(maxsize=lru_cache_size)
def city_dist(ci0, ci1):
    p0 = cities[ci0]
    p1 = cities[ci1]
    r = p0 - p1
    return np.linalg.norm(r)
#    return np.dot(r, r)


def tour_dist(tour):
    return sum((city_dist(tour[i], tour[i + 1]) for i in tour))


state_f = tour_dist(tour)

tour_plot = np.array([cities[i] for i in tour])

# plt.plot(tour_plot[:, 0], tour_plot[:, 1], 'red', zorder=-30)
plt.scatter(cities[:, 0], cities[:, 1])
# plt.show()

t_start = perf_counter()

# 2-Opt alogirithm main loop.
epoch = 0
while True:
    # for epoch in range(int('inf')):

    # Enumerate all neighbor states { sₖ }.
    neighbor_tours = tuple(two_opt(tour, p[0], p[1]) for p in perms)

    log_interval = 5
    if epoch % log_interval == 0:
        print(f'Epoch {epoch}:')
        print(' f(sₖ) = {:.4f}'.format(state_f))

    # Calculate f(sₖ) for all neighbor states.
    neighbor_f = tuple(tour_dist(t) for t in neighbor_tours)

    # Calculate Δf = f(sₖ) - f ⃰ for neighbors.
    delta_f = tuple(fd - state_f for fd in neighbor_f)

    # Find neighbor state index k which minimizes Δf.
    k_min = np.argmin(delta_f)

    fd_least = delta_f[k_min]

    # Check termination condition.
    if fd_least >= 0.0:
        t_elapsed = perf_counter() - t_start
        print('Solution found after {} epochs in {:.1f}s.'.format(
            epoch, t_elapsed))
        print('  Optimal tour length = {:.0f}'.format(
            state_f))
        break

    # Transition to new state and record new f(sₖ).
    tour = neighbor_tours[k_min]
    state_f = neighbor_f[k_min]

    epoch += 1


tour_plot = np.array([cities[i] for i in tour])

plt.scatter(cities[:, 0], cities[:, 1])
plt.plot(tour_plot[:, 0], tour_plot[:, 1], linewidth=0.5)
plt.show()
