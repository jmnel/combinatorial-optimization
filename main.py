#!/usr/bin/env python3

import pancakes
import missionaries
import hanoi


def main():

    # Run solver for Pancake Sorting problem.
    print('Solving Pancake Sort problem...')
    pancake_res = pancakes.solve_pancakes_problem()
    print('Done.\n')

    # Run solver for Missionaries and Canibals problem.
    print('Solving Missionaries and Canibals problem...')
    missionaries_res = missionaries.solve_missionaries_cannibals_prob()
    print('Done.\n')

    # Run solver for Towers of Hanoi problem.
    print('Solving Towers of Hanoi problem...')
    hanoi_res = hanoi.solve_hanoi_problem()
    print('Done.\n')

    # Convert h-evaluation time to human-readible format.
    pancake_res.h_eval_time = '{0:.2f} ms'.format(
        pancake_res.h_eval_time * 10e3)
    missionaries_res.h_eval_time = '{0:.1f} μs'.format(
        missionaries_res.h_eval_time * 10e6)
    hanoi_res.h_eval_time = '{0:.2f} s'.format(
        hanoi_res.h_eval_time)

    # Convert p-queue time cost to human-readible format.
    pancake_res.fringe_cost_t = '{0:.2f} ms'.format(
        pancake_res.fringe_cost_t * 10e3)
    missionaries_res.fringe_cost_t = '{0:.2f} μs'.format(
        missionaries_res.fringe_cost_t * 10e6)
    hanoi_res.fringe_cost_t = '{0:.2f} s'.format(
        hanoi_res.fringe_cost_t)

    # Convert total runtime to human-readible format.
    pancake_res.total_time = '{0:.2f} ms'.format(
        pancake_res.total_time * 10e3)
    missionaries_res.total_time = '{0:.2f} ms'.format(
        missionaries_res.total_time * 10e3)
    hanoi_res.total_time = '{0:.1f} s'.format(
        hanoi_res.total_time)

    # Attach problem titles to profiling metrics.
    results = {
        'Pancake Sort': pancake_res,
        'Missionaries and Canibals': missionaries_res,
        'Towers of Hanoi': hanoi_res
    }

    print('\n\n')
    print('RESULTS'.center(74))
    print()

    # Print Table 1 showing space complexity of various problems.
    print('┌────────────────────────────────────────────────────────────────────────┐')
    print('│' + 'Table 1: Space complexity'.center(72) + '│')
    print('├────────────────────────────────────────────────────────────────────────┤')
    row = '│ Problem'.ljust(28)
    row += ' │ fringe sz'.ljust(13)
    row += ' │ closed-set sz'.ljust(18)
    row += ' │ child skip'.ljust(13)
    row += ' |'
    print(row)
    print('├────────────────────────────────────────────────────────────────────────┤')

    for n, r in results.items():
        row = '│ {} '.format(n).ljust(28)
        row += ' │ {}'.format(r.fringe_max_size).ljust(13)
        row += ' │ {}'.format(r.closed_set_size).ljust(18)
        row += ' │ {}'.format(r.child_skip_count).ljust(13)
        row += ' │'
        print(row)
    print('└────────────────────────────────────────────────────────────────────────┘')

    print('\n\n')

    # Print Table 2 showing time complexity for various problems.
    print('┌────────────────────────────────────────────────────────────────────────────────┐')
    print('│' + 'Table 2: Time complexity'.center(80) + '│')
    print('├────────────────────────────────────────────────────────────────────────────────┤')
    row = '│ Problem'.ljust(28)
    row += ' │ h-count'.ljust(13)
    row += ' │ h-time'.ljust(11)
    row += ' │ p-queue time'.ljust(15)
    row += ' │ total time'.ljust(13)
    row += ' │'
    print(row)
    print('├────────────────────────────────────────────────────────────────────────────────┤')

    for n, r in results.items():
        row = '│ {} '.format(n).ljust(28)
        row += ' │ {}'.format(r.h_eval_count).ljust(13)
        row += ' │ {}'.format(r.h_eval_time).ljust(11)
        row += ' │ {}'.format(r.fringe_cost_t).ljust(15)
        row += ' │ {}'.format(r.total_time).ljust(13)
        row += ' │'
        print(row)
    print('└────────────────────────────────────────────────────────────────────────────────┘')


# Program entry point
if __name__ == '__main__':
    main()
