import numpy as np
import itertools

start = np.zeros((4, 7))
work = np.zeros((4, 7))
padd = np.zeros((4, 7))

pmin = [750, 1000, 1200, 1800]

start[0, 0] = 0.0
start[0, 1] = 1.0
start[0, 2] = 0.0
start[0, 3] = 3.0000000000000004
start[0, 4] = 0.0
start[0, 5] = 0.0
start[0, 6] = 0.0
start[1, 0] = 0.0
start[1, 1] = 0.0
start[1, 2] = 0.0
start[1, 3] = 0.0
start[1, 4] = 0.0
start[1, 5] = 0.0
start[1, 6] = 0.0
start[2, 0] = 0.0
start[2, 1] = 6.0
start[2, 2] = 0.0
start[2, 3] = 0.0
start[2, 4] = 0.0
start[2, 5] = 0.0
start[2, 6] = 0.0
start[3, 0] = 0.0
start[3, 1] = 3.0
start[3, 2] = 0.0
start[3, 3] = 1.9999999999999998
start[3, 4] = 0.0
start[3, 5] = 1.9999999999999998
start[3, 6] = 0.0
work[0, 0] = 3.0
work[0, 1] = 4.0
work[0, 2] = 4.0
work[0, 3] = 7.0
work[0, 4] = 3.0
work[0, 5] = 3.0
work[0, 6] = 3.0
work[1, 0] = 4.0
work[1, 1] = 4.0
work[1, 2] = 4.0
work[1, 3] = 4.0
work[1, 4] = 4.0
work[1, 5] = 4.0
work[1, 6] = 4.0
work[2, 0] = 1.9999999999999998
work[2, 1] = 7.999999999999999
work[2, 2] = 7.999999999999999
work[2, 3] = 7.999999999999999
work[2, 4] = 7.999999999999999
work[2, 5] = 7.999999999999999
work[2, 6] = 3.9999999999999996
work[3, 0] = 0.0
work[3, 1] = 3.0
work[3, 2] = 1.0
work[3, 3] = 3.0
work[3, 4] = 1.0
work[3, 5] = 3.0
work[3, 6] = 1.0
padd[0, 0] = 0.0
padd[0, 1] = 1600.0000000000002
padd[0, 2] = 0.0
padd[0, 3] = 3350.000000000001
padd[0, 4] = 0.0
padd[0, 5] = 350.0000000000015
padd[0, 6] = 0.0
padd[1, 0] = 1750.0000000000002
padd[1, 1] = 2000.0000000000007
padd[1, 2] = 200.0000000000012
padd[1, 3] = 2000.0000000000007
padd[1, 4] = 950.0000000000024
padd[1, 5] = 2000.0000000000007
padd[1, 6] = 1950.0000000000018
padd[2, 0] = 1599.9999999999998
padd[2, 1] = 6399.999999999999
padd[2, 2] = 6399.999999999999
padd[2, 3] = 6399.999999999999
padd[2, 4] = 6399.999999999999
padd[2, 5] = 6399.999999999999
padd[2, 6] = 3199.9999999999995
padd[3, 0] = 0.0
padd[3, 1] = 0.0
padd[3, 2] = 0.0
padd[3, 3] = 0.0
padd[3, 4] = 0.0
padd[3, 5] = 0.0
padd[3, 6] = 0.0

report = np.zeros((4, 7, 3))

for i, j in itertools.product(range(4), range(7)):
    report[i, j, 0] += work[i, j]
    report[i, j, 1] += work[i, j] * pmin[i] + padd[i, j]
    report[i, j, 2] += padd[i, j]

txt = ''
for i in range(4):
    txt += f'{i+1} & No. used & '
    txt += ' & '.join('{:0.0f}'.format(report[i, j, 0]) for j in range(7))
    txt += '\\\\\n'
    txt += ' & Tot. output & '
    txt += ' & '.join('{:.0f}'.format(report[i, j, 1]) for j in range(7))
    txt += '\\\\\n'
    txt += ' & Add. output & '
    txt += ' & '.join('{:.0f}'.format(report[i, j, 2]) for j in range(7))
    txt += '\\\\\n'

print(txt)
