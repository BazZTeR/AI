from csp import *

class kenken(CSP):
	def __init__(self,input):
		self.gridSize = 0
		self.variables = []
		self.groups = []
		self.domains = {}
		self.neighbors = {}
		self.load_input(input)

		# fill variables
		for i in range(self.gridSize):
			for j in range(self.gridSize):
				self.variables.append((i,j))

		# create domain list
		domainList = []
		for i in range(self.gridSize):
			domainList.append(i+1)
		# fill domains
		for i in self.variables:
			self.domains[i] = domainList.copy()

		# fill neighbors
		for i in self.variables:
			neighbors = []
			# neighbors in the same column
			for j in range(self.gridSize):
				if(i[0] != j):
					neighbors.append((j,i[1]))
			# neighbors in the same row
			for j in range(self.gridSize):
				if(i[1] != j):
					neighbors.append((i[0],j))
			# neighbors in the same clique
			for group in self.groups:
				if(i in group):
					for var in group[:-2]:
						if(var!=i):
							neighbors.append(var)
			self.neighbors[i] = neighbors

		CSP.__init__(self,self.variables,self.domains,self.neighbors,self.constraints)

	def load_input(self,input):
		# set grid size
		self.gridSize = int(input[0])
		print("grid size = " ,self.gridSize)
		input = input[3:]
		# set domains values
		group = []
		for i in input.split():
			if '.' in i:
				# varbiable format: X.X
				group.append((int(i[0]),int(i[2])))
			elif(i=="null" or i=="+" or i=="-" or i=="*" or i=="/"):
				group.append(i)
			else:
				group.append(i)
				self.groups.append(group)
				group = []
		print(self.groups)

	def constraints(self,A,a,B,b):
		print(A,a,B,b)
		assignment = self.infer_assignment()
		print(assignment)
		# check if the two variables are in the same row or column and ensure that they have different values
		if(A[0] == B[0] or A[1] == B[1]):
			if(a==b):
				return False
		# A and B in the same group
		for group in self.groups:
			if(A in group and B in group):
				result = 0
				# check if group operation is valid
				if(group[-2] == '+'):
					result += a + b
					for var in group:
						if(var in assignment):
							result += assignment[var]
					if result == group[-1]:
						return True
					return False
				elif(group[-2] == '-'):
					if(a > b):
						return a-b == group[-1]
					else:
						return b-a == group[-1]
				elif(group[-2] == '*'):
					result = a * b
					for var in group:
						result *= assignment[var]
					if result == group[-1]:
						return True
					return False
				elif(group[-2] == '/'):
					if(a > b):
						return a/b == group[-1]
					else:
						return b/a == group[-1]
				else:
					# null operator
					return a == group[-1]
			else:
				# A and B are not in the same group
				return True
	def kenken_display(self,assignment):
		for i in list(range(self.gridSize)):
			for j in sorted(assignment.items()):
				if j[0][0] == i:
					print(j[1], end=" ")
			print('\n',end="")
			
# inputs
easy =	'''3x3
0.0 null 1
1.0 1.1 + 5
2.0 2.1 / 3
0.1 0.2 - 1
1.2 2.2 - 1'''

easy2 = '''3x3
0.0 1.0 1.1 + 5
0.1 null 2
0.2 1.2 + 5
2.0 2.1 + 5
2.2 null 1'''

medium =	'''6x6
			0.0 1.0 + 11
			0.1 0.2 / 2
			0.3 1.3 * 20
			0.4 0.5 1.5 2.5 * 6
			1.1 1.2 - 3
			1.4 2.4 / 3
			2.0 2.1 3.0 3.1 * 240
			2.2 2.3 * 6
			4.0 4.1 * 6
			3.2 4.2 * 6
			3.3 4.3 4.4 + 7
			3.4 3.5 * 30
			5.0 5.1 5.2 + 8
			5.3 5.4 / 2
			4.5 5.5 + 9'''

input = easy
k = kenken(input)

# BT
print("____________________")
print("_________BT_________")
res = backtracking_search(k)
k.kenken_display(res)

# BT+MRV
print("____________________")
print("_______BT+MRV_______")
res = backtracking_search(k, select_unassigned_variable=mrv)
k.kenken_display(res)

# FC
print("____________________")
print("_________FC_________")
res = backtracking_search(k, inference=forward_checking)
k.kenken_display(res)

# FC+MRV
print("____________________")
print("_______FC+MRV_______")
res = backtracking_search(k, select_unassigned_variable=mrv,inference=forward_checking)
k.kenken_display(res)

# MAC
print("____________________")
print("_________MAC________")
res = backtracking_search(k, inference=mac)
k.kenken_display(res)

# MinConflicts
print("____________________")
print("____MinConflicts____")
res = min_conflicts(k)
k.kenken_display(res)