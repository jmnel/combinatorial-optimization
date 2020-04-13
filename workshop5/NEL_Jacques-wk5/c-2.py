"""
C-2 Production of drinking glasses
"""

# There are 12 week planning periods.
NT = 12

# Enumerate each of the 12 weeks.
WEEKS = list(range(NT))

# Enumerate 6 different product variants.
PRODS = list(range(6))

# Double index of product and week index.
PROD_WEEK = Index([(p, w) for p in PRODS for w in WEEKS])

# Demand for each product varient in each of the planning periods.
DEM = [
[20, 22, 18, 35, 17, 19, 23, 20, 29, 30, 28, 32],
[17, 19, 23, 20, 11, 10, 12, 34, 21, 23, 30, 12],
[18, 35, 17, 10, 9,  21, 23, 15, 10, 0,  13, 17],
[31, 45, 24, 38, 41, 20, 19, 37, 28, 12, 30, 37],
[23, 20, 23, 15, 10, 22, 18, 30, 28, 7,  15, 10],
[22, 18, 20, 19, 18, 35, 0,  28, 12, 30, 21, 23]]

# Production cost of each product variant.
CPROD = [100, 80, 110, 90, 200, 140]

# Stock inventory cost for each product.
CSTOCK = [25, 28, 25, 27, 10, 20]

# Initial stock quantitiy at the start of first week.
ISTOCK = [ 50, 20, 0, 15, 0, 10]

# Final stock requirements at the end of the 12 weeks.
FSTOCK = [10, 10, 10, 10, 10, 10]

# Worker time required to produce each product variant.
TIMEW = [3, 3, 3, 2, 4, 4]

# Machine time required to produce each product variant.
TIMEM = [2, 1, 4, 8, 11, 9]

# Storage space required for each product variant during production.
SPACE = [4, 5, 5, 6, 4, 9]

# Available worker  time production capacity.
CAPW = 390

# Available machine time production capacity.
CAPM = 850

# Available storage area for production.
CAPS = 1000

# Integer decision variable; indicates number of product p produced in period t.
produce = Variable(index=PROD_WEEK, vartype='integer')

# Integer decision variable; indicates number of product p stored in warehouse in period t.
store = Variable(index=PROD_WEEK, vartype='integer')

# Double index; same as PROD_WEEK but excludes first period.
PROD_WEEK_E = Index([(p, w) for p in PRODS for w in WEEKS[1:]])

# This constraint determines the inventory level after first planning period; uses initial stock level.
cstr1 = Constraint([store[p, 0] == ISTOCK[p] + produce[p, 0] - DEM[p][0] for p in PRODS], index=PRODS)

# Later inventory levels are determined by previous planning period inventory + production - demand.
cstr2 = Constraint([store[p, t] == store[p, t-1] + produce[p, t] - DEM[p][t] for p, t in PROD_WEEK_E], index=PROD_WEEK_E)

# Enforce final stock requirement.
cstr3 = Constraint([store[p, NT-1] >= FSTOCK[p] for p in PRODS], index=PRODS)

# Worker time capacity can not be exceeded.
cstr4 = Constraint([sum(TIMEW[p]*produce[p, t] for p in PRODS) <= CAPW for t in WEEKS], index=WEEKS)

# Machine time capacity can not be exceeded.
cstr5 = Constraint([sum(TIMEM[p]*produce[p, t] for p in PRODS) <= CAPM for t in WEEKS], index=WEEKS)

# Production is limited by storage area.
cstr6 = Constraint([sum(SPACE[p]*produce[p, t] for p in PRODS) <= CAPS for t in WEEKS], index=WEEKS)

# Production decision variable must be non-negative integer for all p and t.
cstr7 = Constraint([produce[p, t] >= 0 for p, t in PROD_WEEK], index=PROD_WEEK)

# Store decision variable must be non-negative integer for all p and t.
cstr8 = Constraint([store[p, t] >= 0 for p, t in PROD_WEEK], index=PROD_WEEK)

# Total cost is sum of production and storage costs over all p and t.
cost_fn = Objective(sum(CPROD[p]*produce[p, t] + CSTOCK[p]*store[p, t] for p, t in PROD_WEEK))

# Define and solve model.
glass_model = Problem([produce, store], cost_fn, [cstr1, cstr2, cstr3, cstr4, cstr5, cstr6, cstr7, cstr8])
cbc_minimize(glass_model)


