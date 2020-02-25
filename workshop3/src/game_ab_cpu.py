from typing import Tuple
from common.ticktack import *
from alpha_beta import alpha_beta_search
from common_ab import *

"""
This program demonstrates the implementation of alpha-beta search by self-playing.
You will observe that no matter which player starts, the result is always a draw.
"""

# Initial state is empty board.
s = ()
print(state_to_str(s))

# Run main game loop.
while True:

    # Get score of current game state.
    score = score_weighted(s)

    # If game is not in finished, perform search for best next move for current
    # player.
    if score is None:

        # Call alpha-beta search function.
        s, _, stats = alpha_beta_search(s,
                                        util_fn=score_weighted,
                                        expand_fn=expand_basic,
                                        randomize=True)
        print(state_to_str(s))

    # Check for game end states.
    elif score > 0.:
        print('Player x wins!')
        break

    elif score < 0.:
        print('Player o wins!')
        break

    else:
        print('Draw!')
        break
