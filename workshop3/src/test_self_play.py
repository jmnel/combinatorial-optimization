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

    # Initiliaze empty board.
    state = (0, 4, 2)
    print(state_to_str(state))

    # Run main loop.
    while True:

        # Get score of current game state.
        score = two_player_score(state)

        # If game is not finished, perform search for best next move for current
        # player.
        if score is None:

            print('Thinking...\n')
            # Call MCTS search function.
            state, v, stats = uct_search(state,
                                         util_fn=score_2,
                                         selection_criteria='max',
                                         max_epochs=200)
            print('Monte Carlo UCT algorithm found move with v={} in {}.\n'.format(
                v, time_hr(stats['t_elapsed'])))

            print(state_to_str(state))

            return

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


mcts_self_play()
