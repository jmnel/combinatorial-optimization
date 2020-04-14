from pprint import pprint
import json



N = 19
TASKS = Index(list(range(N-1)))
TASKS_D = Index(list(range(N)))

TT = Index([(i, j) for i in TASKS_D for j in TASKS_D])



DUR = [	
	2,
	16,
	9,
	8,
	10,
	6,
	2,
	2,
	9,
	5,
	3,
	2,
	1,
	7,
	4,
	3,
	9,
	1,
	0 ]

PRED = [ 	
	list(),		
	[0,],
	[1,],
	[1,],
	[2,],
	[3, 4],
	[3,],
	[5,],
	[3, 5],
	[3,],
	[5,],
	[8,],
	[6,],
	[1,],
	[3, 13],
	[7, 10, 13],
	[11,],
	[16,],
	[9, 12, 14, 17, 15]]

ARCS = [[1 if j in PRED[i] else 0 for j in range(N)] for i in range(N)]

MAX_REDUCT = [	
	0,
	3,
	1,
	2,
	2,
	1,
	1,
	0,
	2,
	1,
	1,
	0,
	2,
	1,
	1,
	0,
	0,
	2,
	2,
	1,
	3,
	0,
	0 ]

ADD_COST = [
	0,
	30,
	26,
	12,
	17,
	15,
	8,
	0,
	42,
	21,
	18,
	0,
	0,
	22,
	12,
	6,
	16,
	0,
	0 ]
				

x = Variable(index=TASKS_D, vartype='integer')

obj_done = Objective(x[N-1])

cstr1 = Constraint([x[i] >= ARCS[i][j]*(x[j] + DUR[j]) for i, j in TT], index=TT)
cstr2 = Constraint([x[t] >= 0 for t in TASKS_D], index=TASKS_D)

model_b1_q1 = Problem([x], obj_done, [cstr1, cstr2])

cbc_minimize(model_b1_q1)


# Dump results to JSON file for graphing and further use in report.
results = {'obj_value':obj_done.value,
			'x':[x[i].value for i in TASKS_D] }

results_path = 'C:\\Users\\jacques\\repos\\jmnel\\combinatorial-optimization\\final\\results\\problem1_b2_q1_results.json'
with open(results_path, 'w') as f:
	f.write(json.dumps(results))