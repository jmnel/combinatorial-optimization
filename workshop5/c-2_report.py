import numpy as np
import itertools

produce = np.zeros((6, 12))
store = np.zeros((6, 12))
#padd = np.zeros((4, 7))


produce[0, 0] = 0.0
produce[0, 1] = 0.0
produce[0, 2] = 11.000000000000002
produce[0, 3] = 34.0
produce[0, 4] = 29.0
produce[0, 5] = 7.0
produce[0, 6] = 23.000000000000004
produce[0, 7] = 21.000000000000004
produce[0, 8] = 29.0
produce[0, 9] = 29.0
produce[0, 10] = 29.0
produce[0, 11] = 41.00000000000001
produce[1, 0] = 7.0
produce[1, 1] = 21.000000000000004
produce[1, 2] = 14.0
produce[1, 3] = 17.0
produce[1, 4] = 11.000000000000002
produce[1, 5] = 10.0
produce[1, 6] = 12.0
produce[1, 7] = 34.0
produce[1, 8] = 21.000000000000004
produce[1, 9] = 23.000000000000004
produce[1, 10] = 30.0
produce[1, 11] = 22.000000000000004
produce[2, 0] = 18.0
produce[2, 1] = 35.0
produce[2, 2] = 17.0
produce[2, 3] = 11.000000000000002
produce[2, 4] = 8.0
produce[2, 5] = 21.0
produce[2, 6] = 23.000000000000004
produce[2, 7] = 15.0
produce[2, 8] = 10.0
produce[2, 9] = 0.0
produce[2, 10] = 13.0
produce[2, 11] = 27.0
produce[3, 0] = 16.0
produce[3, 1] = 45.00000000000001
produce[3, 2] = 24.0
produce[3, 3] = 38.0
produce[3, 4] = 41.0
produce[3, 5] = 20.0
produce[3, 6] = 20.0
produce[3, 7] = 36.0
produce[3, 8] = 29.0
produce[3, 9] = 11.000000000000002
produce[3, 10] = 31.0
produce[3, 11] = 46.00000000000001
produce[4, 0] = 47.00000000000001
produce[4, 1] = 16.0
produce[4, 2] = 34.0
produce[4, 3] = 14.0
produce[4, 4] = 23.0
produce[4, 5] = 24.0
produce[4, 6] = 43.00000000000001
produce[4, 7] = 0.0
produce[4, 8] = 26.0
produce[4, 9] = 4.0
produce[4, 10] = 0.0
produce[4, 11] = 0.0
produce[5, 0] = 13.999999999999998
produce[5, 1] = 17.0
produce[5, 2] = 20.0
produce[5, 3] = 18.0
produce[5, 4] = 18.0
produce[5, 5] = 35.0
produce[5, 6] = 0.9999999999999999
produce[5, 7] = 26.999999999999996
produce[5, 8] = 11.999999999999998
produce[5, 9] = 48.99999999999999
produce[5, 10] = 27.999999999999996
produce[5, 11] = 6.999999999999999
store[0, 0] = 30.0
store[0, 1] = 8.0
store[0, 2] = 1.0
store[0, 3] = 0.0
store[0, 4] = 12.0
store[0, 5] = 0.0
store[0, 6] = 0.0
store[0, 7] = 1.0
store[0, 8] = 1.0
store[0, 9] = 0.0
store[0, 10] = 1.0
store[0, 11] = 10.0
store[1, 0] = 10.0
store[1, 1] = 12.0
store[1, 2] = 3.0
store[1, 3] = 0.0
store[1, 4] = 0.0
store[1, 5] = 0.0
store[1, 6] = 0.0
store[1, 7] = 0.0
store[1, 8] = 0.0
store[1, 9] = 0.0
store[1, 10] = 0.0
store[1, 11] = 10.0
store[2, 0] = 0.0
store[2, 1] = 0.0
store[2, 2] = 0.0
store[2, 3] = 1.0
store[2, 4] = 0.0
store[2, 5] = 0.0
store[2, 6] = 0.0
store[2, 7] = 0.0
store[2, 8] = 0.0
store[2, 9] = 0.0
store[2, 10] = 0.0
store[2, 11] = 9.999999999999998
store[3, 0] = 0.0
store[3, 1] = 0.0
store[3, 2] = 0.0
store[3, 3] = 0.0
store[3, 4] = 0.0
store[3, 5] = 0.0
store[3, 6] = 1.0
store[3, 7] = 0.0
store[3, 8] = 1.0
store[3, 9] = 0.0
store[3, 10] = 1.0
store[3, 11] = 10.0
store[4, 0] = 24.0
store[4, 1] = 20.0
store[4, 2] = 30.999999999999996
store[4, 3] = 29.999999999999996
store[4, 4] = 43.0
store[4, 5] = 44.99999999999999
store[4, 6] = 70.0
store[4, 7] = 40.0
store[4, 8] = 38.0
store[4, 9] = 35.0
store[4, 10] = 20.0
store[4, 11] = 10.0
store[5, 0] = 2.0
store[5, 1] = 1.0
store[5, 2] = 1.0
store[5, 3] = 0.0
store[5, 4] = 0.0
store[5, 5] = 0.0
store[5, 6] = 1.0
store[5, 7] = 0.0
store[5, 8] = 0.0
store[5, 9] = 19.0
store[5, 10] = 26.0
store[5, 11] = 10.0

txt = ''
for i in range(6):
    txt += f'\\textbf{{{i+1}}} & Prod. & '
    txt += ' & '.join('{:.0f}'.format(produce[i, j]) for j in range(12))
    txt += '\\\\\n'
    txt += '& Store & '
    txt += ' & '.join('{:.0f}'.format(store[i, j]) for j in range(12))
    txt += '\\\\\n'

print(txt)