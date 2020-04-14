import numpy as np
from pprint import pprint

m=5
C = Index(m)

n = 2

Q = [[0, 500, 1000, 300, 1500],
[1500, 0, 250, 630 , 1140],
[400, 510, 0, 460 , 490],
[300, 600, 810, 0 , 310],
#[400, 100, 420, 730, 970],
[350, 1020, 260, 380, 0]]

cities = {'atlanta':0, 'boston':1, 'chicago':2, 'marseille':3, 'paris':4}

city2city = {
	('atlanta','boston'):945,
	('atlanta', 'chicago'):605,
	('atlanta', 'marseille'):4667,
	#('atlanta', 'nice'):4749,
	('atlanta', 'paris'):4394,
	('boston','chicago'):605,
	('boston','marseille'):3726,
	#('boston','nice'):3806,
	('boston','paris'):3448,
	('chicago','marseille'):4471,
	#('chicago','nice'):4541,
	('chicago','paris'):4152,
	#('marseille','nice'):109,
	('marseille','paris'):415,
	#('nice','paris'):431}
}

DIST = np.zeros((m, m))

for c1c2, dist in city2city.items():
	c1, c2 = c1c2
	assert(c1 in cities)
	assert(c2 in cities)
	
	idx1, idx2 = cities[c1], cities[c2]
	
	DIST[idx1][idx2] = dist
	DIST[idx2][idx1] = dist


DISCOUNT = 0.8

COST = np.zeros((m, m, m, m))

for i in range(m):
	for j in range(m):
		for k in range(m):
			for l in range(m):
				COST[i,j,k,l] = DIST[i, k] + DISCOUNT * DIST[k, l] + DIST[l, j]

cccc = list()
for i in range(m):
	for j in range(m):
		for k in range(m):
			for l in range(m):
				cccc.append((i,j,k,l))

CCCC = Index(cccc)


x = Variable(vartype='binary', index=CCCC)
y = Variable(vartype='binary', index=C)

print(len(cccc))
print(x)

foo = sum( x[i, j, k, l] for i, j, k, l in cccc )

