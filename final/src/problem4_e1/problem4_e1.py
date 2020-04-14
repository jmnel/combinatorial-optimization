from pydoc import help
from math import sqrt
from pprint import pprint

n = 10
AGENCIES = list(range(n))
A = Index(AGENCIES)


X = [0, 20, 18, 30, 35, 33, 5, 5, 11, 2]
Y = [0, 20, 10, 12, 0, 25, 27, 10, 0, 15]


#DIST = [[ sqrt((X[i][0] - X[j][0])**2 + (X[i][1] - X[j][1])**2) for j in AGENCIES] for i in AGENCIES]

REQ = [10, 6, 8, 11, 9, 7, 15, 7, 9, 12]
STO = [8, 13, 4, 8, 12, 2, 14, 11, 15, 7]

C = 0.5
L = 1.3

EXCESS = list(filter(lambda a: REQ[a] < STO[a], AGENCIES))
NEED = list(filter(lambda a: REQ[a] > STO[a], AGENCIES))


DIST = [[ sqrt((X[EXCESS[i]] - X[NEED[j]])**2 + (Y[EXCESS[i]] - Y[NEED[j]])**2) for j in range(len(NEED))] for i in range(len(EXCESS))]
DIST = [[ int(str(f'{i}{j}')) for j in range(len(NEED))] for i in range(len(EXCESS))]

print(DIST)

E = Index(list(range(len(EXCESS))))
N = Index(list(range(len(NEED))))
EN = Index([(i, j) for i in range(len(EXCESS)) for j in range(len(NEED))])
x = Variable(vartype='integer', index=EN)

REQ_E = [REQ[i] for i in EXCESS]
REQ_N = [REQ[i] for i in NEED]
STO_E = [STO[i] for i in EXCESS]
STO_N = [STO[i] for i in NEED]

print(len(DIST))
print(len(DIST[0]))

obj = Objective(sum( [C*L*x[i, j]*DIST[i][j] for i, j in EN]))

print(obj)

print(EN)

cstr1 = Constraint([sum( x[i, j] for i in E) == STO_N[j] - REQ_N[j] for j in N], index=N)
cstr2 = Constraint([sum( x[i, j] for j in N) == STO_E[i] - REQ_E[i] for i in E], index=E)
cstr3 = Constraint([x[i, j] >= 0 for (i, j) in EN], index=EN)

model = Problem([x], obj, [cstr1, cstr2, cstr3])

print(model)


#EN = Index([(i, j) for i in EXCESS for j in NEED])

#x = Variable(vartype='integer', index=EN)

#obj = Objective(sum(sum(C*L*x[i, j] for j #in NEED) for i in EXCESS))

#cstr1 = Constraint([sum(x[i, j] for i in EXCESS) == STO[j] - REQ[j] for j in NEED], index=N)
#cstr2 = Constraint([sum(x[i, j] for j in NEED) == STO[i] - REQ[i] for i in EXCESS], index=E)

#model = Problem([x], obj, [cstr1, cstr2])

minimize_cbc(model)
