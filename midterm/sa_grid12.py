import numpy as np
from temp_schedule import EASchedule
from simulated_annealing import sa_solve

# Set function f values for grid1.
grid1 = np.array([[3., 7., 2., 8.],
                  [5., 2., 9., 1.],
                  [5., 3., 3., 1.]])


# Set function f values for grid2.
grid2 = np.array([[0., 0., 0., 1., 4.],
                  [0., 0., 2., 8., 10.],
                  [0., 2., 4., 8., 16.],
                  [1., 4., 8., 16., 32.]])

# Create exponential additive cooling schedule
cooling_sched = EASchedule(initial_temp=100,
                           final_temp=0,
                           num_cycles=5)

# Run simulated annealing for grid1.
print('Running simulated annealing for grid1...')
optim_state, f_max, _ = sa_solve(grid1,
                                 temp_schedule=cooling_sched,
                                 initial_state=(0, 0),
                                 log_interval=10)
print('Done.\n\n')

# Create exponential additive cooling schedule
cooling_sched = EASchedule(initial_temp=10,
                           final_temp=0,
                           num_cycles=50)

# Run simulated annealing for grid2.
print('Running simulated annealing for grid2...')
optim_state2, f_max2, _ = sa_solve(grid2,
                                   temp_schedule=cooling_sched,
                                   initial_state=(0, 0),
                                   log_interval=100,
                                   adaptive=False)
print('Done.\n\n')
