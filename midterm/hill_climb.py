from typing import Tuple, Callable
import numpy as np
from time import perf_counter


def f_grid1(ij: Tuple[int, int]):
    data = np.array([[3., 7., 2., 8.],
                     [5., 2., 9., 1.],
                     [5., 3., 3., 1.]])

    i, j = ij
    i = i % data.shape[0]
    j = j % data.shape[1]

    return data[i, j]


def f_grid2(ij: Tuple[int, int]):
    data = np.array([[0., 0., 0., 1., 4.],
                     [0., 0., 2., 8., 10.],
                     [0., 2., 4., 8., 16.],
                     [1., 4., 8., 16., 32.]])

    i, j = ij
    i = i % data.shape[0]
    j = j % data.shape[1]

    return data[i, j]


def f_grid3(ij: Tuple[int, int]):
    a, b, c, d = -2, 2, -1, 3

    def f(x, y): return -(1-x)**2 - 100*(y-x**2)**2

    data = np.array([
        [f(a + i*(b-a)/99., c + j*(d-c)/99.) for j in range(100)]
        for i in range(100)])

    print('max=')
    print(f'{np.argmax(np.array(data))}')

    i, j = ij
    i = i % data.shape[0]
    j = j % data.shape[1]

    return data[i, j]


def hill_climb_max(x0: Tuple[int, int],
                   obj_fn: Callable[[Tuple[int, int]], float],
                   max_epochs: int = 20):

    t_start = perf_counter()

    x = x0

    for epoch in range(0, max_epochs):

        i, j = x
        candidiates = np.array([(i-1, j),
                                (i, j-1),
                                (i+1, j),
                                (i, j+1),
                                (i-1, j-1),
                                (i+1, j-1),
                                (i+1, j+1),
                                (i-1, j+1)])

        current_eval = obj_fn(x)

        if epoch % 1 == 0:
            print(f'Epoch {epoch}:')
            print('  x = ( {}, {} ), f( x ) = {}\n'.format(
                i, j, current_eval))

        cand_evals = np.array([obj_fn(x) for x in candidiates])

        best_candidiate = np.argmax(cand_evals)
        best_eval = cand_evals[best_candidiate]

        if best_eval <= current_eval:
            t_elapsed = (perf_counter() - t_start)*1e6
            print('Solution found after {} iterations in {:.0f}μs:'.format(
                epoch+1, t_elapsed))
            print('  x* = ( {}, {} )'.format(x[0], x[1]))
            print('  f( x* ) = {}\n\n'.format(current_eval))
            return (current_eval, x)

        x = candidiates[best_candidiate]


print('Performing hillclimb for grid1.')
hill_climb_max((0, 0), f_grid1)

print('Performing hillclimb for grid2.')
hill_climb_max((0, 0), f_grid2)

print('Performing hillclimb for grid3.')
hill_climb_max((0, 0), f_grid3)
