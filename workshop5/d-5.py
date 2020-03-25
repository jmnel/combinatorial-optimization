"""
D-5 Cutting sheet metal
"""

# Shape size yields for different patterns.
CUT = {
'36x50': [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
'24x36': [2, 1, 0, 2, 1, 0, 3, 2, 1, 0, 5, 4, 3, 2, 1, 0],
'20x60': [0, 0, 0, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
'18x30': [0, 1, 3, 0, 1, 3, 0, 2, 3, 5, 0, 1, 3, 5, 6, 8]
}

# Demand for each of the 4 different sizes.
DEM = {'36x50': 8, '24x36': 13, '20x60': 5, '18x30': 15}

# Enumerate 4 sizes.
SIZES = ['36x50', '24x36', '20x60', '18x30']

# Enumerate 16 different cutting patterns.
PATTERNS = list(range(16))

# Double index for size-shape.
SP = Index([(s, p) for s in SIZES for p in PATTERNS])

# Integer decision variable; indicates use of cutting pattern.
use = Variable(index=PATTERNS, vartype='integer')

# The cost is 1 for each cutting pattern; determined by number of raw blanks used.
COST = [1 for _ in PATTERNS]

# Cost function is simply count of number of raw blanks used.
sheets_cost_fn = Objective(sum(COST[p]*use[p] for p in PATTERNS))

# Production must meet demand.
cstr1 = Constraint([sum(CUT[s][p]*use[p] for p in PATTERNS) >= DEM[s] for s in SIZES], index=SIZES)

# The 'use' decision variable must be a non-negative integer.
cstr2 = Constraint([use[p] >= 0 for p in PATTERNS], index=PATTERNS)

# Define and solve model.
min_sheets_model = Problem([use], sheets_cost_fn, [cstr1, cstr2])
cbc_minimize(min_sheets_model)