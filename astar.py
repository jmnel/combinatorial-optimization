import heapq
import time


class AStarProfStats:
    backtrack_time = 0
    child_skip_count = 0
    closed_set_size = 0
    epochs = 0
    fringe_cost_t = 0
    fringe_max_size = 0
    h_eval_count = 0
    h_eval_time = 0
    total_time = 0


def astar_search(init_state,
                 expand_fn, heuristic_fn,
                 epochs=3000,
                 print_fn=None):

    # Keep track of several profiling metrics.
    prof_t_start = time.perf_counter()

    print('Performing A* search...')

    start_node = (0, 0, 99, init_state, None)

    prof_stats = AStarProfStats()

    fringe = list()
    fringe_t_start = time.perf_counter()
    heapq.heappush(fringe, start_node)
    prof_stats.fringe_cost_t += time.perf_counter() - fringe_t_start

    closed_set = set()

    # Perform A* algorithm main loop.
    for epoch in range(0, epochs):

        prof_stats.fringe_max_size = max(
            prof_stats.fringe_max_size, len(fringe))

        if not fringe:
            raise Exception('Error: Fringe empty, but no solution found after {} iterations'.format(
                epoch
            ))
            return None

        fringe_t_start = time.perf_counter()
        node = heapq.heappop(fringe)
        prof_stats.fringe_cost_t += time.perf_counter() - fringe_t_start

        f, g, h, state, parent = node

        if epoch % 1000 == 1:
            print('Epoch {}'.format(epoch))
            if print_fn is not None:
                print_fn(state)

        if h == 0:
            prof_stats.total_time = time.perf_counter() - prof_t_start
            prof_stats.epochs = epoch
            print('Solution found after {0:d} epochs in {1:.4f}s.'.format(
                epoch, prof_stats.total_time
            ))

            prof_stats.closed_set_size = len(closed_set)

            print('Backtracking...')
            prof_t_back_start = time.perf_counter()
            assert(len(node) is 5)
            n = node
            solution_path = list()
            while n:
                solution_path.append(n[3])
                if n[4]:
                    n = n[4]
                else:
                    break

            solution_path.reverse()

            prof_stats.backtrack_time = time.perf_counter() - prof_t_back_start

            print('Solution path is:')
            for i in range(len(solution_path)):
                print('  {} state = {}'.format(
                    i, solution_path[i]
                ))
                if print_fn is not None:
                    print_fn(solution_path[i])
            return prof_stats

        closed_set.add(state)

        children = expand_fn(state)
        for c_state in children:
            if not c_state in closed_set:

                for a in closed_set:
                    assert(a != c_state)

                g_c = g + 1
                h_eval_start = time.perf_counter()
                h_c = heuristic_fn(c_state)
                prof_stats.h_eval_time += time.perf_counter() - h_eval_start
                prof_stats.h_eval_count += 1
                f_c = g_c + h_c

                fringe_t_start = time.perf_counter()
                heapq.heappush(fringe, (f_c, g_c, h_c, c_state, node))
                prof_stats.fringe_cost_t += time.perf_counter() - fringe_t_start
            else:
                prof_stats.child_skip_count += 1

    else:
        print('Failed to find solution after {} epochs.'.format(epochs))
        return None
