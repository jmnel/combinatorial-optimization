from typing import Tuple, Callable
import numpy as np
from time import perf_counter
import matplotlib
matplotlib.use('GTK3Cairo')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def hill_climb(initial_state: Tuple[int, int],
               grid: np.array,
               max_epochs,
               log_interval=2):
    """Finds maximum value on discrete grid using hill climbing algorithm.

    Args:
        initial_state: the starting state.
        grid: discrete grid of function values.
        max_epochs: maximum number of iterations.
        log_interval: frequency of verbose output.

    Returns:
        tuple: Tuple containing index of max value and max value.

    """

    # Get profiling timer start.
    t_start = perf_counter()

    i, j = initial_state
    m_rows, n_cols = grid.shape

    # Main loop of algorithm.
    for epoch in range(0, max_epochs):

        # Enumerate all candidiates for neighboring states.
        candidiates = ((i - 1, j),      # adjacent below
                       (i, j - 1),      # adjacent left
                       (i + 1, j),      # adjacent above
                       (i, j + 1),      # adjacent right
                       (i - 1, j - 1),  # diagonal down-left
                       (i + 1, j - 1),  # diagonal up-left
                       (i + 1, j + 1),  # diagonal up-right
                       (i - 1, j + 1))  # diagonal down-right

        # Evaluate f at current state.
        f_curr = grid[i, j]

        # Do verbose log output printing.
        if epoch % log_interval == 0:
            print(f'Epoch {epoch}:')
            print(f'  x = ({i}, {i})')
            print(f'  f(x) = {f_curr}\n')

        # Wrap candidiate neighbor coordinates to grid size.
        candidiates = tuple((i % m_rows, j % n_cols) for i, j in candidiates)

        # Evaluate f at neighboring states.
        f_cand = tuple(grid[i, j] for i, j in candidiates)

        # Get index of best neighbor.
        c_best_i = np.argmax(f_cand)

        # Get f value at best neighbor.
        f_best = f_cand[c_best_i]

        # TERMINATION: If current state is better than neighbors,
        if f_curr >= f_best:

            # print results, and
            print('Solution found after {} iterations in {:.0f}μs.'.format(
                epoch + 1, (perf_counter() - t_start) * 1e6))
            print(f'  x* = ({i}, {j})')
            print(f'  f(x*) = {f_curr}\n')

            # return solution state and maximum value to callee.
            return ((i, j), f_curr)

        # State becomes best neighbor.
        i, j = candidiates[c_best_i]


# Set function f values for grid1.
grid1 = np.array([[3., 7., 2., 8.],
                  [5., 2., 9., 1.],
                  [5., 3., 3., 1.]])

# Perform hill climb for grid1.
hill_climb((0, 0), grid1, 10)

# Set function f values for grid2.
grid2 = np.array([[0., 0., 0., 1., 4.],
                  [0., 0., 2., 8., 10.],
                  [0., 2., 4., 8., 16.],
                  [1., 4., 8., 16., 32.]])

# Perform hill climb for grid2.
hill_climb((0, 0), grid2, 10)


def make_grid3():
    """Generates points for grid3."""

    def f(x, y):
        return -(1 - x)**2 - 100 * (y - x**2)**2

    # Set [x-min, x-max] x [y-min, y-max] for grid3.
    a, b, c, d = -2, 2, -1, 3

    return np.array([
        [f(a + i * (b - a) / 99., c + j * (d - c) / 99.) for j in range(100)]
        for i in range(100)])


# Perform hill climb on grid3.
hill_climb((0, 0), make_grid3(), max_epochs=300)

fig = plt.figure()
ax = fig.gca(projection='3d')

x = np.linspace(-2.0, 2.0, 100)
y = np.linspace(-1.0, 3.0, 100)
x, y = np.meshgrid(x, y)
z = -(1 - x)**2 - 100 * (y - x**2)**2

surf = ax.plot_surface(x, y, z, cmap='viridis')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('f(x,y)')
plt.savefig('figures/figure1-1.svg')

fig = plt.figure()
ax = fig.gca()
root_plt = ax.contourf(x, y, np.power(-z, 1 / 8), cmap='viridis')
#root_plt.set_label('f(x, y)^(1/8)')
# ax.legend()
plt.savefig('figures/figure1-2.svg')

plt.show()
