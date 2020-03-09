from test_minimax import *
from test_alpha_beta import *
from test_negamax import *
from test_mcts import *
from test_self_play import *


def main():
    print('Profiling minimax...\n')
    test_minimax_random_state()
    print('\nProfiling alpha-beta...\n')
    test_alpha_beta_random_state()
    print('\nProfiling negamax...\n')
    test_negamax_random_state()
    print('\nProfiling mcts...\n')
    test_mcts_random_state()
    print()

    print('Running self play examples...')
    minimax_self_play()
    alpha_beta_self_play()
    negamax_self_play()
#    mcts_self_play()


if __name__ == '__main__':
    main()
