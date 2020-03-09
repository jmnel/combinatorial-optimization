import numpy as np
import matplotlib
matplotlib.use('Qt5Cairo')
import matplotlib.pyplot as plt
from dj38_loader import DJ38Loader
from tsp_solver import tsp_solve


def solve_dj38():
    """Solves TSP for 'dj38' dataset."""

    print('Solving TSP with \'dj38\' dataset...')

    # Download and get citiy coordinates form dataset.
    cities = DJ38Loader().dataset
    num_cities = len(cities)

    print(f'  Found {num_cities} cities.')

    # Create initial tour by enumerating cities and append first element.
    initial_tour = tuple(i for i in range(num_cities)) + (0,)

    print('  Running 2-opt TSP solver...\n')
    optim_tour, _ = tsp_solve(cities)

    initial_tour_points = np.array([cities[i] for i in initial_tour])
    optim_tour_points = np.array([cities[i] for i in optim_tour])

    fig, ax = plt.subplots()
#    ax.plot(initial_tour_points[:, 0], initial_tour_points[:, 1], 'red',
#            linewidth=0.8, zorder=-30)
    ax.scatter(cities[:, 0], cities[:, 1], c='blue')
    ax.set_xlabel('x')
    ax.set_ylabel('y')

#    plt.show()
#    plt.savefig(fname='figures/figure4-1.svg')

#    plt.cla()
    ax.plot(optim_tour_points[:, 0], optim_tour_points[:, 1], 'red',
            linewidth=0.8, zorder=-30)
    ax.scatter(cities[:, 0], cities[:, 1], c='blue')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
#    plt.savefig(fname='figures/figure4-2.svg')

    plt.show()


solve_dj38()
