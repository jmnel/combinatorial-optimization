from math import ceil

loss = [43, 26, 37, 28, 13, 54, 62, 49, 19, 28, 30]
life_span = [8, 8, 2, 8, 4, 8, 8, 8, 6, 8, 8] 

nw = len(loss)
nl = 3
wagons = list(range(nw))

ns = ceil(nw / nl)

slots = list(range(ns))



sw = Index([(w, s) for w in wagons for s in slots])

process = Variable(index=sw, vartype='binary')

print('foo')

#w = 0

#q = Constraint( [ sum(process[w, s] for s in slots) == 1 for w in wagons ], index=wagons )
#print(q)1

#foo = list()

#for w in wagons:

	#c = Constraint( sum(process[w, s] for s in slots) == 1 )
	#foo.append(c)

#for c in foo:
#	print(c)

#print(process)
