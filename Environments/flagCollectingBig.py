import numpy as np
from abc import ABC
import Environments.environment as environment


class FlagCollectingBig(environment.Environment):
	def __init__(self):
		self.name = "FlagCollectingBig"
		self.initialFlags = [(5*3,15*3), (0*3,0*3), (20*3,0*3)]
		self.size = (21*3,16*3)
		self.reset()
	def terminal(self, state):
		return (state[0], state[1]) in self.goal


	def reset(self):
		self.flagsCollected = 0
		self.state = (4*3,9*3,0,0,0)
		self.prevState = (4*3,9*3,0,0,0)
		self.wallBlocks = [(6,0), (15,0), (6,1), (6,2), (15,2), (6,3), (15,3), (6,4), (7,4), (9,4), (10,4), (11,4), (12,4), (13,4),(14,4), (15,4), (6,5), (10,5), (15,5), (6,6), (10,6), (15,6), (0,7), (2,7), (3,7), (4,7), (5,7), (6,7), (10,7), (15,7), (6,8), (10,8), (15,8),(6,9), (15,9), (10,10),(15,10), (0,11), (1,11), (2,11),(3,11),(5,11), (6,11), (7,11), (8,11), (9,11), (10,11), (15,11), (6,12), (15,12), (6,13), (15,13), (6,14),(15,14), (6,15),(15,15)]
		self.flags = self.initialFlags
		self.walls = []
		for e in self.wallBlocks:
			self.walls.extend([(3*e[0],3*e[1]), (3*e[0]+1,3*e[1]), (3*e[0], 3*e[1]+1), (3*e[0]+1,3*e[1]+1), (3*e[0]+2,3*e[1]), (3*e[0],3*e[1]+2), (3*e[0]+1,3*e[1]+2), (3*e[0]+2, 3*e[1]+1), (3*e[0]+2,3*e[1]+2)]) 
		#self.flags= [(1,6)]
	#	print("WALLS ARE")
	#	print(self.walls)
		self.goal = [(1*3,1*3)]
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
