n = 3
M = Index(n)
k = 4
L = Index(k)
L_E = Index(k-1)

C = [[30, 25, 40, 60],
	[25, 40, 45, 50],
	[40, 20, 50, 45]]

T = [[0, 5, 12],
	[8, 0, 10],
	[15, 10, 0]]


q = 20

ML = Index([(m, l) for m in range(n) for l in range(k)])

MM = Index([(i, j) for i in range(n) for j in range(n)])

mml = tuple(tuple(tuple( (i, j, l) for l in range(k)) for j in range(n)) for i in range(n))

mml = list()
for i in range(n):
	for j in range(n):
		for l in range(k):
			mml.append((i,j,l))

MML = Index(mml)

mml_e = list()
for i in range(n):
	for j in range(n):
		for l in range(k-1):
			mml_e.append((i,j,l))
MML_E = Index(mml_e)

x = Variable(index=ML, vartype='binary')
y = Variable(index=MML, vartype='binary')

obj = Objective((q*sum(C[m][l]*x[m, l] for m, l in ML) + q*sum( T[j][i]*y[i,j,l] for i, j, l in MML_E )))

cstr1 = Constraint([sum( x[m, l] for m in M ) == 1 for l in L], index=L)
cstr2 = Constraint([sum( y[i, j, l] for i, j in MM ) == 1 for l in L_E], index=L_E)
cstr3 = Constraint([x[i,l]+x[j,l+1] >= 2*y[i,j,l] for i, j, l in MML_E], index=MML_E)

model = Problem([x, y], obj, [cstr1, cstr2, cstr3])
print(model)
minimize_cbc(model)
