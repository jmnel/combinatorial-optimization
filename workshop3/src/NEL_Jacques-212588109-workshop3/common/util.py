from typing import Sequence, Tuple


def argmax(seq: Sequence):

    assert(any(True for _ in seq))

    v_max = float('-inf')
    i_max = 0
    for i, v in enumerate(seq):
        if v > v_max:
            v_max = v
            i_max = i

    return i_max
