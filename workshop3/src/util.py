from typing import Sequence


def argmax(seq: Sequence):
    v_max = float('-inf')
    i_max = 0
    for i, v in enumerate(seq):
        if v > v_max:
            v_max = v
            i_max = i

    return i_max
