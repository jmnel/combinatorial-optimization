from minimax import minimax_search
from alpha_beta import alpha_beta_search
from negamax import negamax_search
from mcts import uct_search
from common.ticktack import *
from common.time_utils import time_hr


def minimax_self_play():

    print('Running self play with minimax algorithm...')
    print('\tUsing weighted score\n')

    # Initiliaze empty board.
    state = ()
    print(state_to_str(state))

    # Run main loop.
    while True:

        # Get score of current game state.
        score = score_weighted(state)

        # If game is not in finished, perform search for best next move for current
        # player.
        if score is None:

            print('Thinking...\n')
            # Call alpha-beta search function.
            state, v, stats = minimax_search(state,
                                             util_fn=score_weighted,
                                             expand_fn=expand_basic,
                                             randomize=True)
            print('minimax algorithm found move with v={} in {}.\n'.format(
                v, time_hr(stats['t_elapsed'])))

            print(state_to_str(state))

        # Check for game end states.
        else:
            print(f'Result score: {score} -> ', end='')
            if score > 0.:
                print('Player x wins!')
                break

            elif score < 0.:
                print('Player o wins!')
                break

            else:
                print('Draw!')
                break


def alpha_beta_self_play():

    print('Running self play with α-β pruning algorithm...')
    print('\tUsing weighted score score\n\trandomization enabled\n')

    # Initiliaze empty board.
    state = ()
    print(state_to_str(state))

    # Run main loop.
    while True:

        # Get score of current game state.
        score = score_weighted(state)

        # If game is not in finished, perform search for best next move for current
        # player.
        if score is None:

            print('Thinking...\n')
            # Call alpha-beta search function.
            state, v, stats = alpha_beta_search(state,
                                                util_fn=score_weighted,
                                                expand_fn=expand_basic,
                                                randomize=True)
            print('α-β pruning algorithm found move with v={} in {}.\n'.format(
                v, time_hr(stats['t_elapsed'])))

            print(state_to_str(state))

        # Check for game end states.
        else:
            print(f'Result score: {score} -> ', end='')
            if score > 0.:
                print('Player x wins!')
                break

            elif score < 0.:
                print('Player o wins!')
                break

            else:
                print('Draw!')
                break


def negamax_self_play():

    print('Running self play with negamax algorithm...')
    print('\tUsing weigthed score\n')

    # Initiliaze empty board.
    state = ()
    print(state_to_str(state))

    # Run main loop.
    while True:

        # Get score of current game state.
        score = score_weighted(state)

        # If game is not in finished, perform search for best next move for current
        # player.
        if score is None:

            print('Thinking...\n')
            # Call alpha-beta search function.
            state, v, stats = alpha_beta_search(state,
                                                util_fn=score_weighted,
                                                expand_fn=expand_basic,
                                                randomize=True)
            print('negamax algorithm found move with v={} in {}.\n'.format(
                v, time_hr(stats['t_elapsed'])))

            print(state_to_str(state))

        # Check for game end states.
        else:
            print(f'Result score: {score} -> ', end='')
            if score > 0.:
                print('Player x wins!')
                break

            elif score < 0.:
                print('Player o wins!')
                break

            else:
                print('Draw!')
                break


def mcts_self_play():

    print('Running self play with Monte Carlo UCT algorithm...')
    print('\tUsing 2-player score\n\tusing max-child criteria\n\t200 epochs\n')

    def score2(state: Tuple[int, ...]):
        board = state_to_board(state)
        rows = tuple(tuple(board[3 * i: 3 * (i + 1)]) for i in range(3))
        cols = tuple(tuple(board[i:9:3]) for i in range(3))
        diag1 = tuple(board[0:9:4])
        diag2 = tuple(board[2:7:2])

        win_seq = (*rows, *cols, diag1, diag2)
        p1_win = any(s == ('x',) * 3 for s in win_seq)
        p2_win = any(s == ('o',) * 3 for s in win_seq)

        if p1_win:
            return 1.
        elif p2_win:
            return -1.
        elif len(state) == 9:
            return 0.0
        else:
            return None

    def two_player_score2(state: Tuple[int, ...]):
        scr = score2(state)
        if len(state) % 2 == 1:
            if scr is not None:
                scr = 1. - scr

        return scr

    # Initiliaze empty board.
    state = ()
    print(state_to_str(state))

    # Run main loop.
    while True:

        # Get score of current game state.
        score = score2(state)

        # If game is not finished, perform search for best next move for current
        # player.
        if score is None:

            print('Thinking...\n')
            # Call MCTS search function.
            state, v, stats = uct_search(state,
                                         util_fn=score2,
                                         selection_criteria='max-robust',
                                         max_epochs=20000)
            print('Monte Carlo UCT algorithm found move with v={} in {}.\n'.format(
                v, time_hr(stats['t_elapsed'])))

            print(state_to_str(state))

        # Check for game end states.
        else:
            print(f'Result score: {score} -> ', end='')
            if score > 0.:
                print('Player x wins!')
                break

            elif score < 0.:
                print('Player o wins!')
                break

            else:
                print('Draw!')
                break
