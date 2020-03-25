"""
F-1 Flight connections at a hub
"""

# This index enumerates the 6 incomming / outgoing flights.
PLANES = list(range(6))

# Lookup table to map index to origin city;
ORIGINS = {	
	0: 'Bordeaux',				# Bordeaux 			~ 0
	1: 'Clermon-Ferrand',		# Clermon-Ferrand	~ 1
	2: 'Marseille',			# Marseille 		~ 2
	3: 'Nantes',				# Nantes 			~ 3
	4: 'Nice',					# Nice 				~ 4
	5: 'Toulouse'}				# Toulouse 			~ 5

# Lookup table to map index to destination city;
DESTINATIONS = {
	0: 'Berlin',				# Berlin			~ 0
	1: 'Bern',					# Bern				~ 1
	2: 'Brussels',				# Brussels			~ 2
	3: 'London',				# London			~ 3
	4: 'Rome',					# Rome				~ 4
	5: 'Vienna'}				# Vienna			~ 5

# Each flight has passengers with various final destinations.
PASS = [
	[ 35,	 12, 	 16, 	38, 	5, 		2],
	[ 25,	 8,		 9, 	24, 	6, 		8],
	[ 12,	 8,		 11, 	27, 	3, 		2],
	[ 38,	 15, 	 14, 	30, 	2, 		9],
	[-1000,	 9,  	 8, 	25, 	10, 	5],
	[-1000,	-1000,	-1000,	14,		6,		7]]

# Double index enumerates all origin-destination combinations.
PP = Index([(i, j) for i in PLANES for j in PLANES])

# Decision variable: 1 if plane from i continues to j; 0 otherwise.
cont = Variable(index=PP, vartype='binary')

# The objective function is maximized by maximum number of passengers remaining on plane; ie. the least
# number of passengers have to board a different plane.
transfers_obj = Objective(sum(PASS[i][j]*cont[i, j] for i, j in PP), direction='maximize')

# Each plane must be assigned to one incomming and one outgoing flight only.
cstr1 = Constraint([sum(cont[i, j] for j in PLANES) == 1 for i in PLANES], index=PLANES)
cstr2 = Constraint([sum(cont[i, j] for i in PLANES) == 1 for j in PLANES], index=PLANES)

# Create model and solve.
planes_model = Problem([cont], transfers_obj, [cstr1, cstr2])
cbc_minimize(planes_model)

# Translate binary decision variable to 'origin' -> 'destination' form.
mapping = dict()
for i, j in PP:
	if cont[i, j].value == 1.0:
		assert(ORIGINS[i] not in mapping)
		mapping[ORIGINS[i]] = (DESTINATIONS[j], PASS[i][j])

# Print optimal plane-flight connections. 
for orig, dest in mapping.items():
	print(f'{orig}\t--->\t{dest[0]}\t{dest[1]}')  