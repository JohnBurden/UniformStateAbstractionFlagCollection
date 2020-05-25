import Environments.flagCollectingStrips
import Environments.flagCollecting
import Environments.flagCollectingSpiral
import Environments.flagCollectingOpenSpace
import Environments.flagCollectingBig
import Environments.FlagCollectingLowConnectivity
import Environments.flagCollectingHighConnectivity
import Environments.flagCollectingLongCorridors

import QLambdaAbstractGen.QLearningAbstractionGenAgent
import copy

import random
import pickle

import matplotlib.pyplot as plt
from tkinter import font
import tkinter as tk
import pandas as pd
import numpy as np
from PIL import Image
import time



#env = Environments.flagCollectingBig.FlagCollectingBig()
env=Environments.flagCollecting.FlagCollecting()


sizex = env.size[0]
sizey = env.size[1]

numActions = 4		
roomR = []
agent = QLambdaAbstractGen.QLearningAbstractionGenAgent.QLearningAbstractionGenAgent((sizex,sizey),numActions)
#env = Environments.flagCollectingStrips.FlagCollectingStrips()

numOfExperiments = 8
alpha=0.1
lambd=0.9
gamma=0.99
omega=20
lastRand=0
epsilon = 0.5
agent.epsilon=epsilon
greedyState= 0
numEpisodes= 500
numRepetitions = 2

abstractionTimingsR = []
simulationTimingsR = []
allRewardsR = []
allFlagsR = []




for r in range(0,numRepetitions):

	print("Iteration is:")
	print(r)

	abstractionTimings = []
	simulationTimings = []
	allRewards = []
	allFlags = []

	moveCount=0
	totalMoveCount=0
	maxflag =0
	maxIndex = 0
	flagCount=0
	rewardScore=[]
	moveCounts=[]
	flagList=[]

	env.reset()

	for e in range(0,numOfExperiments):
		start2 = time.time()
		moveCount=0
		totalMoveCount=0
		maxflag =0
		maxIndex = 0
		flagCount=0
		rewardScore=[]
		moveCounts=[]
		flagList=[]
		collectingReachability=True

		agent = QLambdaAbstractGen.QLearningAbstractionGenAgent.QLearningAbstractionGenAgent((sizex,sizey),numActions) ## resets the agent
		agent.epsilon = 0.5
		env.reset()
		abstraction = QLambdaAbstractGen.Abstraction.Abstraction(agent.abstraction()[e], env.flags, env.goal, env.state) ## gives the right state abstraction
		print(agent.abstraction()[e])
		start1 = time.time()
		abstraction.solveAbstraction()
		end1 = time.time()
		abstractionTimings.append(end1-start1)

		#agent.reachabilityBins = [[abstraction.abstractState(env.state), [env.state]]]

		print("Begin Training:")
		for ep in range(0,numEpisodes):


			episodeReward = 0
			if ep%100==0:
				print(ep)

			env.reset();
			if ep > numEpisodes/10:
				agent.epsilon-= (0.5)/numEpisodes
				##reduce exploration over time.

			agent.resetEligibility()
			moveCount = 0
			a = agent.policy(env.state, env.actions(env.state))
			path=[]

			while not env.terminal(env.state):
				moveCount+=1
				##Select action using policy
				abstractState = abstraction.abstractState(env.state)
				newState = env.transition(env.state, a)
				newAbstractState = abstraction.abstractState(newState)
#				print(newState, newAbstractState) 



				path.append(newState)


				aPrime = agent.policy(newState, env.actions(newState)) ##Greedy next-action selected
				aStar=agent.policyNoRand(newState, env.actions(newState)) ## Optimal next action ---- comparison of the two required for Watkins Q-lambda


				rew = env.reward(env.state,a,newState) ## ground level reward

				shaping = gamma*(abstraction.value(abstraction.abstractState(newState)))*omega - (abstraction.value(abstraction.abstractState(env.state)))*omega
				## potential based reward shaping value

				episodeReward+=rew 
				if e >= numOfExperiments-1: ### We avoid shaping on the last experiment which we set aside for vanilla Q-Learning
					shaping=0
				
				agent.learn(env.state, a, aPrime, rew+shaping, alpha, gamma, lambd, newState, aStar)
				## updates the Q-table for eligible states according to Q-lambda algorithm

				env.state = newState
				a = aPrime
				#next steps actions and states set.


			############# Keep Track of Stuff ################
			flagCount+=env.flagsCollected
			totalMoveCount+=moveCount
			rewardScore.append(episodeReward)
			moveCounts.append(moveCount)
			flagList.append(env.flagsCollected)

		allRewards.append(rewardScore)
		allFlags.append(flagList)

		end2 = time.time()
		simulationTimings.append(end2-start2)

	abstractionTimingsR.append(abstractionTimings)
	simulationTimingsR.append(simulationTimings)
	allFlagsR.append(allFlags)
	allRewardsR.append(allRewards)

######################################################
################## Make Directory ####################

def mkdir_p(mypath):
    '''Creates a directory. equivalent to using mkdir -p on the command line'''

    from errno import EEXIST
    from os import makedirs,path

    try:
        makedirs(mypath)
    except OSError as exc: # Python >2.5
        if exc.errno == EEXIST and path.isdir(mypath):
            pass
        else: raise


######################################################
################## Draw Graph ########################


labs = ["True", "3x3 Tiling","4x4 Tiling", "5x5 Tiling", "7x7 Tiling", "9x9 Tiling", "10x10 Tiling", "No Shaping"]
labs = ["True", "9x9 Tiling", "12x12 Tiling", "15x15 Tiling", "21x21 Tiling", "27x27 Tiling", "32x24 Tiling", "No Shaping"]


labs2 = ["True", "3x3","4x4", "5x5", "7x7", "9x9", "10x10", "None"]
labs2 = ["True", "9x9", "12x12", "15x15", "21x21", "27x27", "32x24", "None"]

output_dir = "FExperiments/"+env.name+"qLambdaAlpha"+str(alpha)+"Gamma"+str(gamma)+"Lambda"+str(lambd)+"Epsilon"+str(agent.epsilon)+"Episodes"+str(numEpisodes)
if env.walls==[]:
	output_dir=output_dir+"NoWalls"
else:
	output_dir=output_dir+"Walls"
mkdir_p(output_dir)

## Reward
whenConverged = []
toPickle = []
plt.figure(1)
plotRewards = np.mean(allFlagsR, axis=0)
plotSDs = np.std(allFlagsR, axis=0)
plotErrors = plotSDs / np.sqrt(10)
plt.rcParams['agg.path.chunksize'] = 10000
for i in range(0, len(plotRewards)):
	d = pd.Series(plotRewards[i])
	s = pd.Series(plotErrors[i])
	movAv=pd.Series.rolling(d,window=int(numEpisodes/10), center=False).mean()

	toPickle.append(movAv)	
	l, caps, c = plt.errorbar(np.arange(len(movAv)),movAv, label=labs[i], yerr=plotErrors[i], capsize=5, errorevery=numEpisodes/10)
	for cap in caps:
		cap.set_marker("_")
plt.ylabel("No. Of Flags Collected")
plt.xlabel("Episode No.")
plt.legend(loc=4)
plt.axis([0,numEpisodes, 0,3])
print(whenConverged)

with open("{}/resultsListPickle".format(output_dir), 'wb') as p:
    pickle.dump(toPickle, p)

##plt.title("Number of Episodes: " + str(numEpisodes) + " Alpha: " + str(alpha) + " Gamma: " + str(gamma) + " Lambda: " +str(lambd) + " Epsilon: "+str(agent.epsilon))


plt.savefig("{}/rewardGraph.png".format(output_dir), dpi=1200, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None)




## Flags Collected
plt.figure(3)
plotFlags = np.mean(allFlagsR, axis=0)
plt.rcParams['agg.path.chunksize'] = 10000
for i in range(0,len(plotFlags)):
	d = pd.Series(plotFlags[i])
	movAv=pd.Series.rolling(d,window=1000, center=False).mean()
	plt.plot(movAv,label=labs[i])
plt.ylabel("Number of Flags")
plt.xlabel("Episde No.")
plt.legend(loc=4)

plt.figure(4)	
plotAbsTimings = np.mean(abstractionTimingsR, axis = 0)
for i, v in enumerate(plotAbsTimings):
    plt.text(i-0.25, v+3, str(round(v,1)), color='blue', fontweight='bold')
plt.bar(np.arange(len(plotAbsTimings)), plotAbsTimings)
plt.xticks(np.arange(len(plotAbsTimings)), labs)
plt.xlabel("Abstraction Used")
plt.ylabel("Time Taken")
plt.title("Time Taken to Solve Each Abstraction")
plt.savefig("{}/AbstractionTime.png".format(output_dir), dpi=1200, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None)


plt.figure(5)
plotSimTimings = np.mean(simulationTimingsR, axis=0)
for i, v in enumerate(plotSimTimings):
    plt.text(i-0.30, v+3, str(round(v,1)), color='blue', fontweight='bold')
plt.bar(np.arange(len(plotSimTimings)), plotSimTimings)
plt.xticks(np.arange(len(plotSimTimings)), labs2)
plt.xlabel("Abstraction Used")
plt.ylabel("Time Taken In Seconds")
#plt.title("Time Taken To Simulate 100 Games With Each Abstraction")
plt.savefig("{}/SimulationTime.png".format(output_dir), dpi=1200, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None)







#plt.show()


