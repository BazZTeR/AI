from csp import *

#SUBSCRIBE TO PEWDIEPIE

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
			self.domains[i] = domainList

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
			if(len(i) == 3):
				group.append((int(i[0]),int(i[2])))
			elif(i=="null" or i=="+" or i=="-" or i=="*" or i=="/"):
				group.append(i)
			else:
				group.append(i)
				self.groups.append(group)
				group = []

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

# Main function

# inputs
easy = '3x3'\
'0.0 null 1'\
'1.0 1.1 + 5'\
'2.0 2.1 / 3'\
'0.1 0.2 - 1'\
'1.2 2.2 - 1'

easy = 	 '''3x3
			0.0 null 1
			1.0 1.1 + 5
			2.0 2.1 / 3
			0.1 0.2 - 1
			1.2 2.2 - 1'''

input = easy
k = kenken(input)
backtracking_search(k)