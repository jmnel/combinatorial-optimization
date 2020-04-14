from math import sqrt

n = 10
A = Index(n)


X = [0, 20, 18, 30, 35, 33, 5, 5, 11, 2]
Y = [0, 20, 10, 12, 0, 25, 27, 10, 0, 15]

REQ = Parameter([10, 6, 8, 11, 9, 7, 15, 7, 9, 12], index=A) 
STO = Parameter([8, 13, 4, 8, 12, 2, 14, 11, 15, 7], index=A)

FLO = [STO[j].value - REQ[j].value for j in A]

print(sum(FLO))

print(FLO) 

AA = Index([(i, j) for i in A for j in A])

DIST = Parameter([ sqrt((X[i]-X[j])**2 + (Y[i]-Y[j])**2) for i in range(n) for j in range(n) ], index=AA)


foo = list()
bar = list()
for a in A:
	if REQ[a].value < STO[a].value:
		foo.append(a)
	elif REQ[a].value > STO[a].value:
		bar.append(a)

#print(foo)
#print(bar)

E = Index(foo)
N = Index(bar)

EN = Index([(i, j) for i in foo for j in bar])

x = Variable(index=EN, vartype='integer')

obj = Objective(sum(0.5*1.3*DIST[i, j]*x[i,j] for i, j in EN))

cstr1 = Constraint([sum(x[i,j] for i in E) == STO[j] - REQ[j] for j in N], index=N)
cstr2 = Constraint([sum(x[i,j] for j in N) == STO[i] - REQ[i] for i in E], index=E)
cstr5 = Constraint([x[i,j] >= 0 for i, j in EN], index=EN)

model = Problem([x], obj, [cstr1, cstr2, cstr5])

#print(model)

#minimize_linprog(model)