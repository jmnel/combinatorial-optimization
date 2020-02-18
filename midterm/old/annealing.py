import numpy as np
import random
import matplotlib.pyplot as plt


def simulated_annealing(grid):

    def temp_schedule(t):
        return max(0., 100. * np.exp(-0.01 * t))

    n = (0, 0)
    t = 0

    while True:

        print(f'iteration {t}')

        temp = temp_schedule(t)

        e_current = grid[n]
        i, j = n
        if temp <= 0.:
            print('Solution found:')
            print('  x* = ({}, {})'.format(i, j))
            print('  f(x*) = {}'.format(e_current))
            return (n, grid[n])

        children = [(i-1, j),
                    (i, j-1),
                    (i+1, j),
                    (i, j+1)]

        children = tuple(filter(
            lambda c: c[0] >= 0 and c[1] >= 0 and c[0] < grid.shape[0] and c[1] < grid.shape[1], children))

        successor = children[random.randint(0, len(children) - 1)]
        print(successor)

        e_successor = grid[successor]
        e_delta = e_successor - e_current
        if e_delta > 0.0:
            n = successor
        else:
            jump_prob = np.exp(e_delta / temp)
            if np.random.uniform(0., 1.) < jump_prob:
                n = successor

        t += 1


# grid2 = np.array([[0., 0., 0., 1., 4.],
#                  [0., 0., 2., 8., 10.],
#                  [0., 2., 4., 8., 16.],
#                  [1., 4., 8., 16., 32.]])

# simulated_annealing(grid2)


a, b, c, d = -2, 2, -1, 3


def f(x, y): return -(1-x)**2 - 100*(y-x**2)**2


grid3 = np.array([
    [f(a + i*(b-a)/99., c + j*(d-c)/99.) for j in range(100)]
    for i in range(100)])

simulated_annealing(grid3)

fig = plt.figure()
#ax = fig.gca(projection='3d')
#x = np.arange(a, b, (b-a)/99.)
#y = np.arange(c, d, (d-c)/99.)
#x, y = np.meshgrid(x, y)

#surf = ax.plot(x, y, grid3, cmap=cm.coolwarm)

plt.imshow(grid3)
plt.show()
