M = 16
N = 3
B = Index(list(range(M)))
W = Index(list(range(N)))

BW = Index([(b, w) for b in B for w in W])

C = 100

MU = [	34, 6, 8, 17, 16, 5, 13, 21,
		25, 31, 14, 13, 33, 9, 25, 25 ]

x = Variable(vartype='binary', index=BW)
m = Variable(vartype='integer')

obj = Objective(m)

cstr1 = Constraint([sum(x[b, w] for w in W) == 1 for b in B], index=B)
cstr2 = Constraint([m >= sum(MU[b]*x[b, w] for b in B) for w in W], index=W)
cstr3 = Constraint([sum( MU[b]*x[b,w] for b in B) <= C for w in W], index=W)
cstr4 = Constraint(m >= 0)

model_d1 = Problem([x, m], obj, [cstr1, cstr2, cstr3, cstr4])

cbc_minimize(model_d1)

packing = {w: list() for w in W}
for w in W:
	for b in B:
		if x[b, w].value > 0.5:
			packing[w].append(b)

wagon_weights = {w: sum(MU[v] for v in packing[w]) for w in W} 


print(packing)
print(wagon_weights)