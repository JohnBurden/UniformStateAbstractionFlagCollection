import numpy as np
from random import *
import QLambdaAbstractGen.Abstraction
import copy

class QLearningAbstractionGenAgent:

	def __init__(self, stateSize, actionSize):
		self.q = np.random.rand(stateSize[0], stateSize[1], 2, 2, 2, actionSize)
		self.epsilon = 0
		self.stateSize = stateSize
		self.e = []
		self.roomObservations = np.zeros((stateSize[0], stateSize[1])).tolist()
		for i in range(0, len(self.roomObservations)):
			for j in range(0, len(self.roomObservations[0])):
				self.roomObservations[i][j] = np.array([-1,-1,-1,-1,-1])



	def resetEligibility(self):
		self.e = []



	def doTiling(self, template, size):
		templateX = len(template[0])
		templateY = len(template)
		newTiling = copy.deepcopy(template)

		currentLabel = (1,1)
		currentX = 0
		currentY= 0
		for y in range(0, templateY):
			currentLabel = (1, currentLabel[1])
			currentX=0
			for x in range(0, templateX):
				if not template[y][x] == "w":
					newTiling[y][x] = str(currentLabel)
				else:
					newTiling[y][x] = str(currentLabel)

				if currentX < size[0]:
						currentX +=1
				else:
					currentLabel = (currentLabel[0]+1, currentLabel[1])
					currentX = 0
			if currentY<size[1]:
				currentY+=1
			else:
				currentLabel = (currentLabel[0],currentLabel[1]+1)
				currentY=0

		return newTiling


	def abstraction(self):
		## This is a horrible hack to make writing the room layout easier. In hindsight I should have used numbers
		A = "a"
		B = "b"
		C = "c"
		D = "d"
		E = "e"
		F = "f"
		G = "g"
		H = "h"
		I = "i"
		J = "j"
		K= "k"
		L="l"
		M="m"
		N="n"
		O="o"
		P="p"
		Q="q"
		R="r"
		S="s"
		T="t"
		U="u"
		V="v"
		X="x"
		Y="y"
		Z="z"
		AA="aa"
		BB="bb"
		CC="cc"
		DD="dd"
		EE="ee"
		FF="ff"
		GG="gg"
		SS="ss"
		W = "w"
		rooms = [] 

		### "True" layout determined by doorways. 
		roomLayout =   [[C,C,C,C,C,C,W,D,D,D,D,D,D,D,D,W,F,F,F,F,F],
						[C,C,C,C,C,C,W,D,D,D,D,D,D,D,D,W,F,F,F,F,F],
						[C,C,C,C,C,C,W,D,D,D,D,D,D,D,D,W,F,F,F,F,F],
						[C,C,C,C,C,C,W,D,D,D,D,D,D,D,D,W,F,F,F,F,F],
						[W,W,W,W,C,W,W,W,W,W,W,D,D,D,D,W,F,F,F,F,F],
						[B,B,B,B,B,B,B,E,E,E,W,D,D,D,D,W,F,F,F,F,F],
						[B,B,B,B,B,B,W,E,E,E,E,D,D,D,D,W,F,F,F,F,F],
						[B,B,B,B,B,B,W,E,E,E,W,D,D,D,D,W,F,F,F,F,F],
						[W,A,W,W,W,W,W,E,E,E,W,D,D,D,D,W,F,F,F,F,F],
						[A,A,A,A,A,A,W,E,E,E,W,D,D,D,D,W,F,F,F,F,F],
						[A,A,A,A,A,A,W,E,E,E,W,D,D,D,D,W,F,F,F,F,F],
						[A,A,A,A,A,A,W,W,E,W,W,W,W,W,W,W,F,F,F,F,F],
						[A,A,A,A,A,A,W,G,G,G,G,G,G,G,G,W,F,F,F,F,F],
						[A,A,A,A,A,A,W,G,G,G,G,G,G,G,G,W,F,F,F,F,F],
						[A,A,A,A,A,A,W,G,G,G,G,G,G,G,G,F,F,F,F,F,F],
						[A,A,A,A,A,A,W,G,G,G,G,G,G,G,G,W,F,F,F,F,F]]
		
		## Uncomment the below block for big flag collection env
		#newLayout = []
		#for l in roomLayout:
		#	nextLine = []
		#	for x in l:
		#		nextLine.extend([x,x,x])
		#	newLayout.append(nextLine)
		#	newLayout.append(nextLine)
		#	newLayout.append(nextLine)
		#roomLayout = newLayout

	#	roomLayout =  	   [[A,A,W,B,B,W,C,C,W,D,D,D,W,E,E,W,F,F,W,G], ## Strips
	#						[A,A,W,B,B,B,C,C,W,D,D,D,W,E,E,W,F,F,W,G],
	#						[A,A,W,B,B,B,C,C,W,D,D,D,W,E,E,W,F,F,W,G],
	#						[A,A,W,B,B,W,C,C,W,D,D,D,W,E,E,W,F,F,F,G],
	#						[A,A,W,B,B,W,C,C,C,D,D,D,W,E,E,W,F,F,W,G],
	#						[A,A,W,B,B,W,C,C,C,D,D,D,W,E,E,W,F,F,W,G],
	#						[A,A,W,B,B,W,C,C,W,D,D,D,W,E,E,W,F,F,W,G],
	#						[A,A,W,B,B,W,C,C,W,D,D,D,W,E,E,W,F,F,W,G],
	#						[A,A,W,B,B,W,C,C,W,D,D,D,W,E,E,W,F,F,W,G],
	#						[A,A,A,B,B,W,C,C,W,D,D,D,W,E,E,W,F,F,W,G],
	#						[A,A,W,B,B,W,C,C,W,D,D,D,W,E,E,E,F,F,W,G],
	#						[A,A,W,B,B,W,C,C,W,D,D,D,W,E,E,E,F,F,W,G],
	#						[A,A,W,B,B,W,C,C,W,D,D,D,W,E,E,W,F,F,W,G],
	#						[A,A,W,B,B,W,C,C,W,D,D,D,W,E,E,W,F,F,W,G],
	#						[A,A,W,B,B,W,C,C,W,D,D,D,W,E,E,W,F,F,W,G],
	#						[A,A,W,B,B,W,C,C,W,D,D,D,W,E,E,W,F,F,W,G],
	#						[A,A,W,B,B,W,C,C,W,D,D,D,W,E,E,W,F,F,W,G],
	#						[A,A,W,B,B,W,C,C,W,D,D,D,D,E,E,W,F,F,W,G],
	#						[A,A,W,B,B,W,C,C,W,D,D,D,W,E,E,W,F,F,W,G],
	#						[A,A,W,B,B,W,C,C,W,D,D,D,W,E,E,W,F,F,W,G]]

	#	roomLayout = 		[[C,C,C,C,C,C,C,C,C,C,C,C,C,C,C,C,C,C,B,B], ## Spiral 
	#						 [C,C,C,C,C,C,C,C,C,C,C,C,C,C,C,C,C,C,B,B],
	#						 [D,D,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,B,B],
	#						 [D,D,W,G,G,G,G,G,G,G,G,G,G,G,G,F,F,W,B,B],
	#						 [D,D,W,G,G,G,G,G,G,G,G,G,G,G,G,F,F,W,B,B],
	#						 [D,D,W,H,H,W,W,W,W,W,W,W,W,W,W,F,F,W,B,B],
	#						 [D,D,W,H,H,W,K,K,K,K,K,K,J,J,W,F,F,W,B,B],
	#						 [D,D,W,H,H,W,K,K,K,K,K,K,J,J,W,F,F,W,B,B],
	#						 [D,D,W,H,H,W,L,L,W,W,W,W,J,J,W,F,F,W,B,B],
	#						 [D,D,W,H,H,W,L,L,M,M,M,W,J,J,W,F,F,W,B,B],
	#						 [D,D,W,H,H,W,L,L,M,M,M,W,J,J,W,F,F,W,B,B],
	#						 [D,D,W,H,H,W,W,W,W,W,W,W,J,J,W,F,F,W,B,B],
	#						 [D,D,W,H,H,I,I,I,I,I,I,I,I,I,W,F,F,W,B,B],
	#						 [D,D,W,H,H,I,I,I,I,I,I,I,I,I,W,F,F,W,B,B],
	#						 [D,D,W,W,W,W,W,W,W,W,W,W,W,W,W,F,F,W,B,B],
	#						 [D,D,E,E,E,E,E,E,E,E,E,E,E,E,E,E,E,W,B,B],
	#						 [D,D,E,E,E,E,E,E,E,E,E,E,E,E,E,E,E,W,B,B],
	#						 [W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,B,B],
	#						 [A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A],
	#						 [A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A]]

	#	roomLayout = 		[[A,A,A,W,0,0,0,0,0,W,E,E,E,W,W,W,W,E,E,E],
	#						 [A,A,A,W,0,0,0,0,0,W,E,E,E,W,W,W,W,E,E,E],
	#						 [A,A,A,W,0,0,0,0,0,W,E,E,E,W,W,W,W,E,E,E],
	#						 [W,B,W,W,0,0,0,0,0,W,E,E,E,W,W,W,W,E,E,E],
	#						 [W,B,W,0,0,0,0,0,0,W,E,E,E,E,E,E,E,E,E,E],
	#						 [W,B,W,0,0,0,0,0,0,W,E,E,E,E,E,E,E,E,E,E],
	#						 [W,B,W,0,0,0,0,0,0,W,W,W,W,D,W,W,W,W,W,W],
	#						 [W,B,W,0,0,0,0,0,0,0,0,0,W,D,W,0,0,0,0,0],
	#						 [W,B,W,0,0,0,0,0,0,0,0,0,W,D,W,0,0,0,0,0],
	#						 [W,B,W,W,W,W,W,W,W,W,W,W,W,D,W,W,W,W,W,W],
	#						 [W,B,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D],
	#						 [W,B,W,W,W,W,W,W,W,W,W,W,W,D,W,W,W,W,W,W],
	#						 [W,B,W,0,0,0,0,0,0,0,0,0,W,D,W,0,0,0,0,0],
	#						 [W,B,W,0,0,0,0,0,0,0,0,0,W,D,W,0,0,0,0,0],
	#						 [W,B,W,0,0,0,0,0,0,W,W,W,W,D,W,W,W,W,W,W],
	#						 [W,B,W,0,0,0,0,0,0,W,F,F,F,F,F,F,F,F,F,F],
	#						 [W,B,W,W,0,0,0,0,0,W,F,F,F,W,W,W,W,F,F,F],
	#						 [C,C,C,W,0,0,0,0,0,W,F,F,F,W,W,W,W,F,F,F],
	#						 [C,C,C,W,0,0,0,0,0,W,F,F,F,W,W,W,W,F,F,F],
	#						 [C,C,C,W,0,0,0,0,0,W,F,F,F,W,W,W,W,F,F,F]]

	#	roomLayout = 		[[C,C,C,C,C,C,C,C,C,C,C,C,C,E,E,E,E,W,W,W], ## Open Space
	#						 [W,W,W,W,W,C,C,C,C,C,C,C,C,E,E,W,E,E,W,W], 
	#						 [W,W,W,W,W,C,C,C,C,W,W,W,D,E,E,E,W,E,E,W],
	#						 [W,W,W,W,W,C,C,D,D,D,D,D,D,E,E,E,W,W,E,E],
	#						 [B,B,B,B,B,B,D,D,D,D,D,D,D,E,E,E,E,W,W,E],
	#						 [B,B,B,B,B,B,D,D,D,D,D,D,D,E,E,E,E,E,E,E],
	#						 [B,B,B,B,B,B,D,D,D,W,D,D,D,E,E,E,E,E,E,E],
	#						 [B,B,B,B,B,B,D,D,W,W,W,D,D,E,E,E,E,E,E,E],
	#						 [B,B,B,B,B,B,D,W,W,W,W,W,F,F,F,F,F,F,W,W],
	#						 [W,W,W,B,B,B,H,H,W,W,W,F,F,F,F,F,F,W,W,W],
	#						 [W,W,W,B,B,B,H,H,H,W,H,F,F,F,F,F,F,F,W,W],
	#						 [A,A,A,B,B,B,H,H,H,H,H,H,W,W,G,G,G,G,G,G],
	#						 [A,A,A,B,B,B,H,H,H,H,H,H,W,W,G,G,G,G,G,G],
	#						 [A,A,A,B,B,B,H,H,H,H,H,G,G,G,G,G,G,G,G,G],
	#						 [A,A,A,B,B,B,H,H,H,H,H,G,G,G,G,G,G,G,G,G],
	#						 [A,A,A,W,W,W,W,H,H,H,W,G,G,G,G,G,G,G,G,G],
	#						 [A,A,A,W,W,W,W,H,H,H,W,G,G,G,G,W,W,G,G,G],
	#						 [A,A,A,W,W,W,W,H,H,H,W,G,G,G,G,W,W,G,G,G],
	#						 [A,A,A,W,W,W,W,H,H,H,W,G,G,G,G,W,W,G,G,G],
	#						 [A,A,A,A,A,A,A,H,H,H,G,G,G,G,G,W,W,G,G,G]]

	#	roomLayout = 		[[A,A,A,W,H,H,H,I,I,I,I,I,I,I,W,J,J,J,J,J], ##High Connectivity
	#						 [A,A,A,W,H,H,H,W,I,I,I,I,I,I,J,J,J,J,J,J],
	#						 [A,A,A,H,H,H,H,W,I,I,I,I,I,I,W,J,J,J,J,J],
	#						 [A,A,A,W,W,W,H,W,W,W,I,W,P,W,W,J,J,J,J,J],
	#						 [A,A,A,W,G,G,G,G,G,W,K,W,P,P,W,J,J,J,J,J],
	#						 [A,A,A,W,G,G,G,G,G,K,K,W,P,P,W,W,W,J,J,J],
	##						 [A,A,A,G,G,G,G,G,G,W,K,W,P,P,P,P,W,P,W,W],
	#						 [A,A,A,W,W,W,W,G,G,W,K,W,P,P,P,P,P,P,P,P],
	#						 [A,A,A,A,A,A,W,F,W,W,W,W,P,P,P,P,P,P,P,P],
	#						 [A,A,A,A,A,A,F,F,F,F,F,W,P,P,P,P,P,P,P,P],
	#						 [A,A,A,A,A,A,W,F,F,F,F,P,P,P,P,P,P,P,P,P],
	#						 [W,W,W,B,W,W,W,F,W,W,W,W,P,W,W,W,W,P,W,W],
	#						 [B,B,B,B,W,E,E,E,E,E,W,O,O,O,O,O,W,N,N,N],
	#						 [B,B,B,B,W,E,E,E,E,E,W,O,O,O,O,O,O,N,N,N],
	#						 [B,B,B,B,E,E,E,E,E,E,W,O,O,O,O,O,W,N,N,N],
	#						 [B,B,B,B,E,W,E,E,E,W,W,O,W,W,O,O,W,N,N,N],
	#						 [W,C,W,W,E,W,W,W,E,W,L,L,L,W,O,W,W,W,N,W],
	#						 [C,C,C,W,W,W,D,D,D,W,L,L,L,W,W,M,M,M,M,M],
	#						 [C,C,C,C,D,D,D,D,D,W,L,L,L,L,M,M,M,M,M,M],
	#						 [C,C,C,W,W,W,D,D,D,L,L,L,L,L,W,M,M,M,M,M]]
#

	#	roomLayout = 		[[A,A,A,W,H,H,H,I,I,I,I,I,I,I,W,J,J,J,J,J], ##Low Connectivity
	#						 [A,A,A,W,H,H,H,W,I,I,I,I,I,I,J,J,J,J,J,J],
	#						 [A,A,A,W,H,H,H,W,I,I,I,I,I,I,W,J,J,J,J,J],
	#						 [A,A,A,W,W,W,H,W,W,W,I,W,W,W,W,J,J,J,J,J],
	#						 [A,A,A,W,G,G,G,G,G,W,K,W,P,P,W,J,J,J,J,J],
	#						 [A,A,A,W,G,G,G,G,G,K,K,W,P,P,W,W,W,J,J,J],
	#						 [A,A,A,W,G,G,G,G,G,W,K,W,P,P,P,P,W,W,W,W],
	#						 [A,A,A,W,W,W,W,G,G,W,K,W,P,P,P,P,P,P,P,P],
	#						 [A,A,A,A,A,A,W,F,W,W,W,W,P,P,P,P,P,P,P,P],
	#						 [A,A,A,A,A,A,W,F,F,F,F,W,P,P,P,P,P,P,P,P],
	#						 [A,A,A,A,A,A,W,F,F,F,F,P,P,P,P,P,P,P,P,P],
	#						 [W,W,W,B,W,W,W,W,W,W,W,W,P,W,W,W,W,W,W,W],
	#						 [B,B,B,B,W,E,E,E,E,E,W,O,O,O,O,O,W,N,N,N],
	#						 [B,B,B,B,W,E,E,E,E,E,W,O,O,O,O,O,O,N,N,N],
	#						 [B,B,B,B,E,E,E,E,E,E,W,O,O,O,O,O,W,N,N,N],
	#						 [B,B,B,B,E,W,E,E,E,W,W,W,W,W,O,O,W,N,N,N],
	#						 [W,C,W,W,E,W,W,W,E,W,L,L,L,W,O,W,W,W,N,W],
	#						 [C,C,C,W,W,W,D,D,D,W,L,L,L,W,W,M,M,M,M,M],
	#						 [C,C,C,W,D,D,D,D,D,W,L,L,L,L,M,M,M,M,M,M],
	#						 [C,C,C,W,W,W,D,D,D,L,L,L,L,L,W,M,M,M,M,M]]


		room = copy.deepcopy(roomLayout)
		room.reverse()
		rooms.append(room)


		room = copy.deepcopy(roomLayout)
		room = self.doTiling(room, (2,2))
		#room = self.doTiling(room, (8,8))
		room.reverse()
		rooms.append(room)


		room = copy.deepcopy(roomLayout)
		room = self.doTiling(room, (3,3))
		#room = self.doTiling(room, (11,11))
		room.reverse()
		rooms.append(room)


		room = copy.deepcopy(roomLayout)
		room = self.doTiling(room, (4,4))
		#room = self.doTiling(room, (14,14))
		room.reverse()
		rooms.append(room)

		room = copy.deepcopy(roomLayout)
		room = self.doTiling(room, (6,6))
		#room = self.doTiling(room, (20,20))
		room.reverse()
		rooms.append(room)

		room = copy.deepcopy(roomLayout)
		room = self.doTiling(room, (8,8))
		#room = self.doTiling(room, (26,26))
		room.reverse()
		rooms.append(room)

		room = copy.deepcopy(roomLayout)
		room = self.doTiling(room, (9,9))
		#room = self.doTiling(room, (31,23))
		room.reverse()
		rooms.append(room)


		room = copy.deepcopy(roomLayout)
		room.reverse()
		rooms.append(room)

		return rooms

	def policy(self, state, actions):
		##epsilon greedy policy
		ran = randint(0,99)
		if ran < self.epsilon*100:
			return actions[randint(0,len(actions)-1)]
		return actions[np.argmax([self.q[state[0],state[1], state[2], state[3], state[4],a] for a in actions])]

	def policyNoRand(self,state,actions):
		## Pure greedy policy used for displaying visual policy
		return actions[np.argmax([self.q[state[0], state[1], state[2], state[3], state[4],a] for a in actions])]


	def learn(self, state1, actionPrev, actionPrime, reward, alpha, gamma, lam, state2, actionStar):
		## Update the eligible states according to Watkins Q-lambda


		found = False
		for x in range(0, len(self.e)):
			if self.e[x][0] == state1 and self.e[x][1]==actionPrev:
				self.e[x] = (self.e[x][0], self.e[x][1], 1)
				found = True
		if not found:
			self.e.append((state1, actionPrev, 1))


		maxValue = self.q[state2[0], state2[1], state2[2], state2[3], state2[4], actionStar]

		delta = reward+(gamma*maxValue) - self.q[state1[0],state1[1], state1[2], state1[3], state1[4] ,actionPrev]
	

		newE = [] ## remove eligibility traces that are too low by rebuilding
		for x in range(0, len(self.e)):
			s,a,v = self.e[x][0], self.e[x][1], self.e[x][2]
			self.q[s[0], s[1], s[2], s[3], s[4], a] = self.q[s[0], s[1], s[2], s[3], s[4],a] + alpha*v*delta
			if actionPrime==actionStar:
				self.e[x] = (self.e[x][0], self.e[x][1], self.e[x][2]*lam*gamma)
			else:
				self.e[x] = (self.e[x][0], self.e[x][1], 0)

			s,a,v = self.e[x]
			if v > 0.01:
				newE.append((s,a,v))
		self.e = newE

