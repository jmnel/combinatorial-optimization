import numpy as np
import matplotlib
matplotlib.use('GTK3Cairo')
import matplotlib.pyplot as plt
from temp_schedule import EASchedule
from simulated_annealing import sa_solve

a, b, c, d = -2, 2, -1, 3


def f_obj(x, y): return -(1 - x)**2 - 100 * (y - x**2)**2


grid3 = np.array([
    [f_obj(a + i * (b - a) / 99., c + j * (d - c) / 99.) for j in range(100)]
    for i in range(100)])

# Create exponential additive cooling schedule
cooling_sched = EASchedule(initial_temp=10,
                           final_temp=0,
                           num_cycles=5000)

# Find global maximum with simulated annealing.
optim_state, f_max, stats = sa_solve(grid3,
                                     temp_schedule=cooling_sched,
                                     initial_state=(0, 0),
                                     log_interval=5000)

# Transform state trajectory from grid to ℝ².
s_traj = np.array([[a + (p[0]) * (b - a) / 99. for p in stats.traj_history],
                   [c + (p[1]) * (d - c) / 99. for p in stats.traj_history]])

# Transform EMA of state trajectory from grid to ℝ².
ema_traj = np.array([[a + (p[0]) * (b - a) / 99. for p in stats.traj_ema_history],
                     [c + (p[1]) * (d - c) / 99. for p in stats.traj_ema_history]])

# Sample f₃(x, y) on 100 x 100 grid.
x = np.linspace(a, b, 100)
y = np.linspace(c, d, 100)
x, y = np.meshgrid(x, y)
z = np.zeros(x.shape)
for i in range(x.shape[0]):
    for j in range(x.shape[1]):
        z[i, j] = f_obj(x[i, j], y[i, j])

# Create figure 2.a.
fig, ax = plt.subplots()
ax.contourf(x, y, -np.log(-z), cmap='viridis', zorder=-40)
plt_ema = ax.plot(ema_traj[0], ema_traj[1], linewidth=1.5,
                  c='white', zorder=-30)
plt_ema[0].set_label('EMA trajectory')

plt_f_actual = ax.scatter([1], [1], c='red', s=400, marker='+', zorder=3)
plt_f_actual.set_label('Analytical solution')

plt_f_sol = ax.scatter(s_traj[0, -1], s_traj[1, -1], s=400,
                       marker='+', c='blue', zorder=4)
plt_f_sol.set_label('SA solution')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend()

# Save figure 2.a to file.
plt.savefig(fname='figures/figure2-1.svg')

# plt.show()

# Create figure 2.b.
plt.cla()
ax.plot(stats.temp_history[:8000])
ax.set_xlabel('Cycle k')
ax.set_ylabel('Temperature T')

plt.show()

# Save figure 2.b to file.
plt.savefig(fname='figures/figure2-2.svg')
