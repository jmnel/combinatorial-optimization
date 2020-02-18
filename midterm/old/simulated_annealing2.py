from typing import Type, Tuple
import numpy as np
import random
from temp_schedule import EASchedule
# from temp_schedule import QASchedule, LSchedule
from time import perf_counter
import matplotlib
matplotlib.use('GTK3Cairo')
import matplotlib.pyplot as plt


a, b, c, d = -2, 2, -1, 3


def f(x, y): return -(1 - x)**2 - 100 * (y - x**2)**2


grid3 = np.array([
    [f(a + i * (b - a) / 99., c + j * (d - c) / 99.) for j in range(100)]
    for i in range(100)])


quad_add_sched = QASchedule(10, 0, 1000)
linear_sched = LSchedule(1, 0, 1000)
ml_sched = MLSchedule(10, 0.1, 0.01)
ea_sched = EASchedule(10, 0, 5000)
sched = ea_sched
ij, f_max, hist, ema, temp_hist = simulated_annealing(grid3, sched, (0, 0))

x_hist = np.array([a + (p[0]) * (b - a) / 99. for p in hist])
y_hist = np.array([c + (p[1]) * (d - c) / 99. for p in hist])

x_ema = np.array([a + (p[0]) * (b - a) / 99. for p in ema])
y_ema = np.array([c + (p[1]) * (d - c) / 99. for p in ema])

# x_hist_smooth = np.array([x_hist[q*100] for q in range(10)])
# y_hist_smooth = np.array([y_hist[q*100] for q in range(10)])

x = np.linspace(a, b, 100)
y = np.linspace(c, d, 100)
x, y = np.meshgrid(x, y)
z = np.zeros(x.shape)
for i in range(x.shape[0]):
    for j in range(x.shape[1]):
        z[i, j] = -(1 - x[i, j])**2 - 100 * (y[i, j] - x[i, j]**2)**2


fig, ax = plt.subplots()
ax.contourf(x, y, -np.log(-z), cmap='viridis', zorder=-40)
#plt.plot(x_hist, y_hist, linewidth=0.4, c='grey', zorder=-30)
plt_ema = ax.plot(x_ema, y_ema, linewidth=1.5, c='white', zorder=-30)
plt_ema[0].set_label('EMA of path')


plt_true_max = ax.scatter([1], [1], c='red', s=400, marker='+', zorder=3)
plt_true_max.set_label('Actual maximum')

plot_max = ax.scatter(x_hist[-1], y_hist[-1],
                      s=400, marker='+', c='blue', zorder=4)
plot_max.set_label('SA solution')

#ax1.set_title('EMA of path')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend()

plt.savefig(fname='figures/figure3-1.svg')
# axs[0].
# plt.show()
plt.cla()
ax.plot(temp_hist[:8000])
#ax.set_title('Adpative exponential cooling schedule')
ax.set_xlabel('Cycle')
ax.set_ylabel('Temperature')
plt.savefig(fname='figures/figure3-2.svg')
plt.show()
