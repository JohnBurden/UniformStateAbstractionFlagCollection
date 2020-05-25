import numpy as np

class Abstraction:
	def __init__(self, states,flags, goal, start):


		##### This is an ugly hack to create the AMDPs.
		##### Each concrete state has an associated string, designating the abstract state, or whether the space is a wall.
		##### Unfortunately adding more than three flags required adding extra for loops for each flag. I couldn't think of a more elegant solution sorry.


		## Initializes abstract states and adjacencies
		self.concreteStates = states
		self.abstractStates = []
		self.adjacencies = []
		self.listOfAbstractStates = []
		## Create mapping from concrete-state to abstract-state
		for j in range(0, len(self.concreteStates)):
			for i in range(0, len(self.concreteStates[0])):
				for k in range(0,2):
					for l in range(0,2):
						for m in range(0,2):
							if self.abstractState((i,j,k,l,m)) not in self.listOfAbstractStates:
								if not self.abstractState((i,j,k,l,m))[0] =="w":
									self.listOfAbstractStates.append(self.abstractState((i,j,k,l,m)))

		## Construct list of adjacencies
		## For each concrete-state check the adjacent concrete-states and check if they belong to separate abstract states. 
		for k in range(0,2):
			for l in range(0,2):
				for m in range(0,2):
					for j in range(0, len(self.concreteStates)-1):
						for i in range(0, len(self.concreteStates[0])-1):
							current = self.abstractState((i,j,k,l,m))
							up = self.abstractState((i,j+1,k,l,m))
							right = self.abstractState((i+1,j,k,l,m))
							if not current == up and not current == "w" and not up == "w":
								if (current,up) not in self.adjacencies:
									self.adjacencies.append((current,up))
									self.adjacencies.append((up,current))
							if not current == right and not current =="w" and not right =="w":
								if (current, right) not in self.adjacencies:
									self.adjacencies.append((current,right))
									self.adjacencies.append((right,current))

						i = len(self.concreteStates[0])-1
						current = self.abstractState((i,j,k,l,m))
						up = self.abstractState((i,j+1,k,l,m))
						if not current == up and not current == "w" and not up == "w":
							if (current,up) not in self.adjacencies:
								self.adjacencies.append((current,up))
								self.adjacencies.append((up,current))



		self.compAdjacencies=[]
		for a in self.listOfAbstractStates:
			nextAdj = [a]
			for b in self.listOfAbstractStates:
				if (a,b) in self.adjacencies:
					nextAdj.append(b)
			self.compAdjacencies.append(nextAdj)
		self.compAdjacencies.append([("bin"), ("bin")])
		## Turn this adjacency pairs into a adjacency list


		## Get the rooms these features are in
		self.listOfAbstractStates.append(('bin'))
		self.flagRooms = [self.abstractState((i,j,0,0,0))[0] for (i,j) in flags]
		self.goalRoom = [self.abstractState((i,j,0,0,0))[0] for (i,j) in goal]
		self.startState = self.abstractState((start[0], start[1], 0,0,0))

		## Initialise empty action, State, State' transitions
		self.rewards = np.zeros((len(self.listOfAbstractStates) + 4, len(self.listOfAbstractStates), len(self.listOfAbstractStates)))
		self.transitions = np.zeros((len(self.listOfAbstractStates) + 4, len(self.listOfAbstractStates), len(self.listOfAbstractStates)))
		self.nonZeroTransitions = []

		for i in range(0, len(self.listOfAbstractStates)):
			for j in range(0,len(self.listOfAbstractStates)):

				## Set transitions for normal moves.
				if self.listOfAbstractStates[j] in self.abstractActions(self.listOfAbstractStates[i]):
					self.transitions[j,i,j]=1
					self.nonZeroTransitions.append((j,i,j))



				## Set Transitions for flag collecting actions
				for fr in range(0,len(self.flagRooms)):
					action = "F" + self.flagRooms[fr]

					if action in self.abstractActions(self.listOfAbstractStates[i]):
						sPrime = self.listOfAbstractStates[i]
						if not sPrime == "bin":
							sPrimeTmp = list(sPrime)
							if sPrimeTmp[1+fr] == 0:
								sPrimeTmp[1+fr] = 1
								sPrime = tuple(sPrimeTmp)
								if self.listOfAbstractStates[j] == sPrime:
									self.transitions[len(self.listOfAbstractStates)+fr,i,j]=1
									self.nonZeroTransitions.append((len(self.listOfAbstractStates)+fr,i,j))

				## Set Transitions for Goal navigation action.
				for gr in range(0,len(self.goalRoom)):
					action = "G"+ self.goalRoom[gr]
					if action in self.abstractActions(self.listOfAbstractStates[i]):
							self.transitions[-1, i, -1]=1
							self.nonZeroTransitions.append((-1,i,-1))

		## Set rewards matrix
		for i in range(0, len(self.listOfAbstractStates)):
			for gr in range(0,len(self.goalRoom)):
				action = "G"+ self.goalRoom[gr]
				if action in self.abstractActions(self.listOfAbstractStates[i]):
					if not self.listOfAbstractStates[i]=="bin": 
						self.rewards[-1, i, -1]= sum(self.listOfAbstractStates[i][1:])*1000




	def solveAbstraction(self):
		### Implementation of Value Iteration on our AMDP
		self.V = np.zeros(len(self.listOfAbstractStates))
		## Value Iteration
		delta = 0.2
		theta = 0.1
		print("Value Iteration delta value:")
		while delta > theta:
			delta = 0
			for i in range(0, len(self.V)):
				v = self.V[i]
				listOfValues = []
				for a in range(0,len(self.listOfAbstractStates)+4):
					value = 0
					for j in range(0,len(self.V)):
						value+= self.transitions[a,i,j]*(self.rewards[a,i,j] + 0.99 * self.V[j])
					listOfValues.append(value)
				self.V[i] = max(listOfValues)
				delta = max(delta, abs(v - self.V[i]))
			print(delta)

		self.V -= min(self.V[0:-1])
		print()


	## Maps from states to abstract states
	def abstractState(self, state):
		x, y = state[0], state[1]
		n = len(state)
		stateBuild = [self.concreteStates[y][x]]
		for i in range(2,n):
			stateBuild.append(state[i])
		return tuple(stateBuild)

	## Provides list of Abstract actions available.
	def abstractActions(self,abstractState):
		newList = []
		for state in self.compAdjacencies:
			if state[0] == abstractState:	
				newList = state[1:]
				if state[0][0] in self.flagRooms and not state[0] == "bin":
					newList.append("F" + state[0][0])
				if state[0][0] in self.goalRoom and not state[0] == "bin":
					newList.append("G" + state[0][0])
				return newList

	## value lookup for abstract states
	def value(self, abstractState):
			return self.V[self.listOfAbstractStates.index(abstractState)]

