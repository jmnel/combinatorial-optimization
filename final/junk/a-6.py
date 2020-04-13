"""
A-6 Production of electricity
"""

# Length of time periods.
LEN = [6, 3, 3, 2, 4, 4, 2]

# Forecasted demand of time periods.
DEM = [12000, 32000, 25000, 36000, 25000, 30000, 18000]

# Get number of time periods.
NT = len(LEN)

# Enumerate time periods {0, ..., 
TIME = list(range(NT))
TYPES = list(range(4))

# Generators have minimum output power when running.
PMIN = [750, 1000, 1200, 1800]

# Generators have maximum output capacity.
PMAX = [1750, 1500, 2000, 3500]

# Cost to start a generator.
CSTART = [5000, 1600, 2400, 1200]

# Cost to run generator at minimum output.
CMIN = [2250, 1800, 3750, 4800]

# Cost for additional power output past base ouput.
CADD = [2.7, 2.2, 1.8, 3.8]

# Number of generators available for each type.
AVAIL = [10, 4, 8, 3]

# Double index enumerating type and time.
TYPE_TIME = Index([(p, t) for p in TYPES for t in TIME])

# Integer decision variable; indicates generators of type p started in period t.
start = Variable(vartype='integer', index=TYPE_TIME)

# Integer decision variable; indicates generators of type p working in period t.
work = Variable(vartype='integer', index=TYPE_TIME)

# Real decision variable; indicates scalable power output on top of base output.
padd = Variable(vartype='real', index=TYPE_TIME)

# Cost is sum of startup cost + fixed running cost + scalable additional capacity cost.
cost_fn = Objective(sum(CSTART[p]*start[p, t] + LEN[t]*(CMIN[p]*work[p, t] + CADD[p]*padd[p, t]) for p, t in TYPE_TIME))

# Double index; same as other index, but excludes first time period.
TYPE_TIME_E = Index([(p, t) for p in TYPES for t in TIME[1:]])

# Constraints governing relationship between started and working generators.
cstr1 = Constraint([start[p, t] >= work[p, t] - work[p, t-1] for p, t in TYPE_TIME_E], index=TYPE_TIME_E)
cstr2 = Constraint([start[p, 0] >= work[p, 0] - work[p, NT-1] for p in TYPES], index=TYPES)

# Limit additional scalable output.
cstr3 = Constraint([padd[p, t] <= (PMAX[p] - PMIN[p])*work[p, t] for p, t in TYPE_TIME], index=TYPE_TIME)

# Demand must be met by base + scalable power for all times.
cstr4 = Constraint([sum(PMIN[p]*work[p, t] + padd[p, t] for p in TYPES) >= DEM[t] for t in TIME], index=TIME)

# Maximum available power must exceed demand with 20% safety margin.
cstr5 = Constraint([sum(PMAX[p]*work[p, t] for p in TYPES) >= 1.2*DEM[t] for t in TIME], index=TIME)

# Limit number of available generators.
cstr6 = Constraint([work[p, t] <= AVAIL[p] for p, t in TYPE_TIME], index=TYPE_TIME)

# Decision variables must be non-negative.
cstr7 = Constraint([work[p, t] >= 0 for p, t in TYPE_TIME], index=TYPE_TIME)
cstr8 = Constraint([start[p, t] >= 0 for p, t in TYPE_TIME], index=TYPE_TIME)
cstr9 = Constraint([padd[p, t] >= 0.0 for p, t in TYPE_TIME], index=TYPE_TIME)

# Setup and solve model.
electricity_model = Problem([start, work, padd], 
							  cost_fn, 
							  [cstr1, cstr2, cstr3, cstr4, cstr5, cstr6, cstr7, cstr8, cstr9])
cbc_minimize(electricity_model)

