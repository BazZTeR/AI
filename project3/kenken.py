from csp import *
import time

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
			# neighbors in the same group
			for group in self.groups:
				if(i in group):
					for var in group[:-2]:
						if(var!=i and var not in neighbors):
							neighbors.append(var)
			self.neighbors[i] = neighbors

		CSP.__init__(self,self.variables,self.domains,self.neighbors,self.constraints)

	def load_input(self,input):
		# set grid size
		self.gridSize = int(input[0])
		input = input[3:]
		# set domains values
		group = []
		for i in input.split():
			if '.' in i:
				# varbiable format: X.Y
				group.append((int(i[0]),int(i[2])))
			elif(i=="null" or i=="+" or i=="-" or i=="*" or i=="/"):
				group.append(i)
			else:
				group.append(int(i))
				self.groups.append(group)
				group = []

	# print result grid
	def print(self,assignment):
		counter = 0
		for i in range(self.gridSize):
			for j in range(self.gridSize):
				print(str(assignment[(i,j)])+"|",end = '')
				counter += 1
				if(counter == self.gridSize):
					counter = 0
					print("")

	def constraints(self,A,a,B,b):
		assignment = self.infer_assignment()
		# check if the two variables are in the same row or column and ensure that they have different values
		if(A[0] == B[0] or A[1] == B[1]):
			if(a==b):
				return False
		for group in self.groups:
			if(A in group and B in group):
				# A and B in the same group
				result = 0
				# check if group operation is valid
				if(group[-2] == '+'):
					result = a + b
					counter = 0
					for var in group:
						if(var in assignment and var != A and var != B):
							result += assignment[var]
							counter += 1
					if result < group[-1] and counter < len(group)-4:
						return True
					elif result == group[-1] and counter == len(group)-4:
						return True
					return False
				elif(group[-2] == '-'):
					if(a > b):
						return a-b == group[-1]
					else:
						return b-a == group[-1]
				elif(group[-2] == '*'):
					result = a * b
					counter = 0
					for var in group:
						if(var in assignment and var != A and var != B):
							result *= assignment[var]
							counter += 1
					if result <= group[-1] and counter < len(group)-4:
						return True
					elif result == group[-1] and counter == len(group)-4:
						return True
					return False
				elif(group[-2] == '/'):
					if(a > b):
						return a/b == group[-1]
					else:
						return b/a == group[-1]
		# A and B are not in the same group
		return True
			
# inputs
easy =	'''3x3
0.0 null 1
1.0 1.1 + 5
2.0 2.1 / 3
0.1 0.2 - 1
1.2 2.2 - 1'''

medium = '''5x5
0.0 1.0 + 3
0.1 0.2 0.3 + 8
0.4 1.4 + 7
1.1 2.0 2.1 + 9
1.2 2.2 + 9
1.3 2.3 2.4 + 9
3.0 4.0 3.1 + 9
3.2 3.3 + 6
4.1 4.2 + 7
4.3 null 3
3.4 4.4 + 5'''

hard1 =	'''6x6
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

hard2 =	'''6x6
0.0 0.1 0.2 1.0 + 18
1.1 1.2 - 2
0.3 1.3 1.4 * 30
0.4 0.5 - 1
1.5 2.5 / 3
2.0 3.0 4.0 + 6
2.1 3.1 - 1
2.2 2.3 2.4 * 60
3.2 4.2 - 2
3.3 3.4 / 2
4.3 4.4 - 2
3.5 4.5 5.5 * 120
5.0 4.1 5.1 + 13
5.2 5.3 - 2
5.4 null 3'''

# select input grid from above
input = easy

# BT
print("____________________")
print("_________BT_________")
mykenken = kenken(input)
start = time.time()
res = backtracking_search(mykenken)
end = time.time()
mykenken.print(res)
print("nassigns =",mykenken.nassigns)
print("Time =",end-start,"seconds")

# TAKES A LOT OF TIME TO FINISH (read pdf document)
# BT+MRV
print("____________________")
print("_______BT+MRV_______")
mykenken = kenken(input)
start = time.time()
res = backtracking_search(mykenken, select_unassigned_variable=mrv)
end = time.time()
mykenken.print(res)
print("nassigns =",mykenken.nassigns)
print("Time =",end-start,"seconds")

# FC
print("____________________")
print("_________FC_________")
mykenken = kenken(input)
start = time.time()
res = backtracking_search(mykenken, inference=forward_checking)
end = time.time()
mykenken.print(res)
print("nassigns =",mykenken.nassigns)
print("Time =",end-start,"seconds")

# FC+MRV
print("____________________")
print("_______FC+MRV_______")
mykenken = kenken(input)
start = time.time()
res = backtracking_search(mykenken, select_unassigned_variable=mrv,inference=forward_checking)
end = time.time()
mykenken.print(res)
print("nassigns =",mykenken.nassigns)
print("Time =",end-start,"seconds")

# MAC
print("____________________")
print("_________MAC________")
mykenken = kenken(input)
start = time.time()
res = backtracking_search(mykenken, inference=mac)
end = time.time()
mykenken.print(res)
print("nassigns =",mykenken.nassigns)
print("Time =",end-start,"seconds")

# MinConflicts
print("____________________")
print("____MinConflicts____")
mykenken = kenken(input)
start = time.time()
res = min_conflicts(mykenken)
end = time.time()
mykenken.print(res)
print("nassigns =",mykenken.nassigns)
print("Time =",end-start,"seconds")