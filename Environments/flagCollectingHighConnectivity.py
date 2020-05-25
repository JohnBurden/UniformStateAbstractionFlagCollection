import numpy as np
from abc import ABC
import Environments.environment as environment


class FlagCollectingHighConnectivity(environment.Environment):
	def __init__(self):
		self.name = "FlagCollectingHighConnectivity"
		self.initialFlags = [(1,19), (18,17), (6,14)]
		self.size = (20,20)
		self.reset()
	def terminal(self, state):
		return (state[0], state[1]) in self.goal


	def reset(self):
		self.flagsCollected = 0
		self.state = (0,0,0,0,0)
		self.prevState = (0,0,0,0,0)
		self.wallsOutline = [[0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
							 [0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
							 [0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0],
							 [0,0,0,1,1,1,0,1,1,1,0,1,1,1,1,0,0,0,0,0],
							 [0,0,0,1,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0],
							 [0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,1,1,0,0,0],
							 [0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,1,0,1,1],
							 [0,0,0,1,1,1,1,0,0,1,0,1,0,0,0,0,0,0,0,0],
							 [0,0,0,0,0,0,1,0,1,1,1,1,0,0,0,0,0,0,0,0],
							 [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
							 [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
							 [1,1,1,0,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1],
							 [0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
							 [0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
							 [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
							 [0,0,0,0,0,1,0,0,0,1,1,0,1,1,0,0,1,0,0,0],
							 [1,0,1,1,0,1,1,1,0,1,0,0,0,1,0,1,1,1,0,1],
							 [0,0,0,1,1,1,0,0,0,1,0,0,0,1,1,0,0,0,0,0],
							 [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
							 [0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0]]
		self.wallsOutline = self.wallsOutline[::-1]
		self.walls = []
		for y in range(0, len(self.wallsOutline)):
			for x in range(0, len(self.wallsOutline[y])):
				if self.wallsOutline[y][x] == 1:
					self.walls.append((x,y))

		self.flags = self.initialFlags
		#self.flags= [(1,6)]
		self.goal = [(0,4)]
		#self.walls = []

	def isTraversable(self, state):
		##Checks if wall is in th way or out of bounds
		if state[0] < 0 or state[0] >= self.size[0]:
			return False
		elif state[1] < 0 or state[1] >= self.size[1]:
			return False
		elif (state[0], state[1]) in self.walls:
			return False
		else:
			return True



	def actions(self, state):
		## Returns list of actions available to the agent at any given state
		actions = []
		for a in range(0,4):
			if self.isTraversable(self.transition(state, a)):
				actions.append(a)
		return actions




	def transition(self, state, action):
		##Checks where the agent will move to if in a speific state performing
		## a certain action

		newCoord = (0,0)
		if action == 0:
			newCoord = (state[0], state[1] + 1)
		elif action == 1:
			newCoord = (state[0] + 1, state[1])
		elif action == 2:
			newCoord = (state[0], state[1] - 1)
		elif action == 3:
			newCoord =  (state[0]-1, state[1])
		else:
			pass
		if newCoord == self.flags[0]:
			return (newCoord[0], newCoord[1], 1, state[3], state[4])
		elif newCoord == self.flags[1]:
			return (newCoord[0], newCoord[1], state[2], 1, state[4])
		elif newCoord == self.flags[2]:
			return (newCoord[0], newCoord[1], state[2], state[3], 1)
		else:
			return (newCoord[0], newCoord[1], state[2], state[3], state[4])

	def reward(self, state, action, state2):
		flagNumber = -1
		## Gives reward to agent and removes flags if necessary
		for index in range(0, len(self.flags)):
			if (state2[0],state2[1]) == self.flags[index]:
				#print("found")
				flagNumber = index
		if flagNumber > -1:
			#print("flagnumber is : "+ str(flagNumber))
			if state[flagNumber+2] == 0:
				self.flagsCollected+=1
				return 100
		if (state2[0],state2[1]) in self.goal:
			#print("goal")
			return (self.flagsCollected)*1000
		return -1
