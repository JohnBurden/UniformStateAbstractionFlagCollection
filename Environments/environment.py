import numpy as np
from abc import ABC, abstractmethod
class Environment(ABC):

	def __init__(self):
		pass


	@abstractmethod
	def transition(self, state, action):
		pass

	@abstractmethod
	def reward(self, state, action, state2):
		pass

	@abstractmethod
	def actions(self, state):
		pass

