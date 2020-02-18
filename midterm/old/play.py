from mpl_toolkits.mplot3d import Axes3D

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import random

a, b, c, d = -2, 2, -1, 3


def f(x, y): return -(1-x)**2 - 100*(y-x**2)**2


fig = plt.figure()
# ax = fig.gca(projection='3d')
ax = fig.gca()

x = np.arange(-2, 2, 0.1)
y = np.arange(-1, 3, 0.1)
x, y = np.meshgrid(x, y)
r = np.sqrt(x**2 + y**2)

# zline = np.linspace(100.0, 100.0, 100)
# xline = np.linspace(-2.0, 2.0, 100)
# yline = np.linspace(-2.0, 2.0, 100)

z = np.zeros(x.shape)
for i in range(x.shape[0]):
    for j in range(x.shape[1]):
        z[i, j] = -(1.-x[i, j])**2 - 100.*(y[i, j]-x[i, j]**2)**2


ax.contourf(x, y, -np.power(-z, 1/5), cmap='gnuplot2')
# ax.plot(xline, yline, 'blue')
ax.scatter([1.0], [1.0], c='red')


grid3 = np.array([
    [f(a + i*(b-a)/99., c + j*(d-c)/99.) for j in range(100)]
    for i in range(100)])


class TempScheduler:

    def __init__(self, temp0):
        self.temp0 = temp0
        self.temp = temp0
        self.k = 0
        self.alpha = 4.01
        self.n = 10000

    def step(self):
        #        self.temp = self.temp0 / (1. + self.alpha + np.log(1. + self.k))
        self.temp = self.temp0 * ((self.n - self.k) / self.n)**2
#        self.temp = max(0, self.temp0 - 0.1 * self.k)
        self.k += 1
        return self.temp

    def temp_final(self):
        return 0.0


def simulated_annealing(grid):

    #    def temp_schedule(t):
    #        return max(0., 100. * np.exp(-0.005 * t))

    temp_scheduler = TempScheduler(80.0)
    n = (0, 0)
#    t = 0

#    te
#    temp0 = 10.

    history = list()

#    temp = temp0
#    temp_final = 0.6

    while True:

        temp = temp_scheduler.step()
        history.append(n)
#        print(f'iteration {t}')

#        temp = max(0.999 * temp, 1e-12)

#        alpha = 1.01
#        temp = temp0 / (1. + alpha * np.log(1. + t))

        print(f'temp={temp}')

        e_current = grid[n]
        i, j = n
        if temp <= temp_scheduler.temp_final():
            print('Solution found:')
            print('  x* = ({}, {})'.format(i, j))
            print('  f(x*) = {}'.format(e_current))
            return (n, grid[n], history)

        children = [(i-1, j),
                    (i, j-1),
                    (i+1, j),
                    (i, j+1)]

        children = tuple(filter(
            lambda c: c[0] >= 0 and c[1] >= 0 and c[0] < grid.shape[0] and c[1] < grid.shape[1], children))

        successor = children[random.randint(0, len(children) - 1)]
#        print(successor)

        e_successor = grid[successor]
        e_delta = e_successor - e_current
        if e_delta > 0.0:
            n = successor
        else:
            jump_prob = np.exp(e_delta / temp)
            if np.random.uniform(0., 1.) < jump_prob:
                n = successor

#        t += 1


n_max, f_max, hist = simulated_annealing(grid3)

xline = np.array([a + h[0]*(b-a)/99. for h in hist])
yline = np.array([c + h[1]*(d-c)/99. for h in hist])

grid_max = np.amax(grid3)
grid_ij_max = np.where(grid3 == grid_max)

print(grid_max)
print(grid_ij_max)
grid_xy_max = (a + grid_ij_max[0]*(b-a)/99., c + grid_ij_max[1]*(d-c)/99.)
print(grid_xy_max)

foo_max = (a + n_max[0]*(b-a)/99., c + n_max[1]*(d-c)/99.)
ax.scatter([foo_max[0]], [foo_max[1]])

ax.plot(xline, yline, linewidth=0.5, color='gray')
plt.show()
