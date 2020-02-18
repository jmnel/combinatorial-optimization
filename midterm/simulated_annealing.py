from typing import Type, Tuple
import random
from time import perf_counter
import numpy as np
from temp_schedule import TempSchedule
from time_utils import time_human_readible


class SAStats:
    traj_history = list()
    traj_ema_history = list()
    temp_history = list()
    elapsed_time = 0.0

    ema = None


def sa_solve(grid: np.array,
             temp_schedule: Type[TempSchedule],
             initial_state: Tuple[int, int],
             adaptive: bool = True,
             log_interval: int = 500,
             ema_interval: int = 50,
             ema_gamma: float = 0.002):

    # Record start time to profiling.
    t_start = perf_counter()

    # Initialize starting state sₖ calculate its f(sₖ).
    state = initial_state

    # Record intial best f ⃰ for adaptive term.
    f_best = grid[state]

    # Initialize epoch counter to 0.
    epoch = 0

    # Create structure to hold statistics.
    stats = SAStats()

    # Run simulated annealing main loop.
    while True:

        # Calculate f(sₖ) for current state.
        f_state = grid[state]

        mu = 1.0
        if adaptive:
            # Calculate 1 < μ < 2 for adaptive schedule.
            mu = 1.0 + np.abs((f_state - f_best) / f_state)
            mu = np.clip(mu, 1.0, 2.0)

        # Update best score f ⃰ encountered so far.
        f_best = max(f_best, f_state)

        # Get temperature from cooling schedule, and
        # multiply with adaptive term μ.
        temperature = mu * temp_schedule.step()

        # Append current temperature to statistics.
        stats.temp_history.append(temperature)

        # Append current state to trajectory statistics.
        stats.traj_history.append(state)

        # Decompose state into i and j for convenience.
        i, j = state

        # Calcluate EMA.
        if epoch == 0:
            ema = (i, j)
        else:
            ema = (ema_gamma * i + (1 - ema_gamma) * ema[0],
                   ema_gamma * j + (1 - ema_gamma) * ema[1])

        # Append EMA to statistics on interval.
        if epoch % ema_interval == 0:
            stats.traj_ema_history.append(ema)

        # Do verbose log outputing.
        if epoch % log_interval == 0:
            print(f'Epoch {epoch}: T = {temperature}.')
            print(f'  f ⃰ = {f_best}')
            print(f'  f(sₖ) = {f_state}')

        # Check termination condition: temperature has reached final temperature.
        if temperature <= temp_schedule.final_temp():
            elapsed_time = perf_counter() - t_start
            print('Solution found after {} cycles in {}.'.format(
                temp_schedule.k(), time_human_readible(elapsed_time)))

            # Return optimum state, f(sₖ), and statistics to caller.
            return (state, f_state, stats)

        # Enumerate available states.
        avail_states = [(i - 1, j),
                        (i, j - 1),
                        (i + 1, j),
                        (i, j + 1),
                        (i - 1, j - 1),
                        (i + 1, j - 1),
                        (i + 1, j + 1),
                        (i - 1, j + 1)]

        # Remove states outside grid.
        avail_states = tuple(filter(
            lambda s: (s[0] >= 0 and
                       s[1] >= 0 and
                       s[0] < grid.shape[0] and
                       s[1] < grid.shape[1]),
            avail_states))

        # Randomly pick from available states.
        next_state = random.choice(avail_states)

        # Calculate energy of new state.
        f_next = grid[next_state]

        # Calculate ΔE between new and old states.
        f_delta = f_next - f_state

        # If new state is at lower energy,
        if f_delta > 0.0:

            # transition to new state.
            state = next_state

        else:
            # Calculate probability: P(transition| T, ΔE).
            p_transistion = np.exp(f_delta / temperature)

            # Transition to new state with above probability.
            if random.random() < p_transistion:
                state = next_state

        # Increment epoch counter.
        epoch += 1
