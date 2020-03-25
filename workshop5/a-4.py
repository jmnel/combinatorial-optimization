"""
Cane sugar production
"""

from math import ceil

# Each lot has an associated hourly loss.
LOSS = [43, 26, 37, 28, 13, 54, 62, 49, 19, 28, 30]

# Remaining lifetime for the product in each lot.
LIFE = [8, 8, 2, 8, 4, 8, 8, 8, 6, 8, 8]

# A given lot takes 2 hours to process.
DUR = 2

# Get the number of wagons.
NW = len(LOSS)

# The refinery has 3 equivalent production lines.
NL = 3

# Enumerate the wagons.
WAGONS = list(range(NW))

# Number of slots is determined by rounding up number of wagons devided by number of lines.
NS = ceil(NW / NL)

# Enumerate slots.
SLOTS = list(range(NS))

# Combined double index with wagon-slot.
WS = Index([(w, s) for w in WAGONS for s in SLOTS])

# Binary decision variable; indicates lot w is processed in slot s.
x = Variable(index=WS, vartype='binary')

# Every lot is assigned to exactly one slot.
cstr1 = Constraint([sum(x[w, s] for s in SLOTS) == 1 for w in WAGONS], index=WAGONS)

# Limit lots per time slot.
cstr2 = Constraint([sum(x[w, s] for w in WAGONS) <= NL for s in SLOTS], index=SLOTS)

# Limit unprocessed product life.
cstr3 = Constraint([sum((s+1) * x[w,s] for s in SLOTS) <= LIFE[w] / DUR for w in WAGONS], index=WAGONS)

# Loss function is simply amount of raw material lost due to fermentation from delay in processing.
loss_fn = Objective( sum( [(s+1) * DUR * LOSS[w] * x[w, s] for w, s in WS]))

# Define and solve problem.
sugar_model = Problem([x], loss_fn, [cstr1, cstr2, cstr3] )
cbc_minimize(sugar_model)