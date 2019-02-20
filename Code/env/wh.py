from config import * 

import numpy as np 
import matplotlib.pyplot as plt 

class Env(object): 
	def __init__(self): 
		''' 
		self.observation_space = observation_space 
		self.action_space = action_space 
		''' 

	# Reset at the beginning of a new episode 
	def reset(self): 
		n = np.random.randint(C+1) # number of bags (today) 
		d = np.random.randint(1, D+1) # day (today) 
		state = (n, d) 
		return state 

	# Poisson Distribution; Function to return demand for a given day 
	def demand(self, day): 
		#s = np.random.poisson(lam=(m1,m2,m3,m4,m5,m6,m7), size=(N, D)) # dimensions of s = N x D 	
		s = np.random.poisson(lam=(m1,m2,m3,m4,m5,m6,m7)) # dimensions of s = 1 x D 
		return s[day-1] 

	def profit(self, n): 
		return n * P 

	def penalty_1(self, n): # Bags sent back to supplier; Loss incurred when extra bags were ordered 
		return n * P1 

	def penalty_2(self, n): # Customers sent back without wheat; Loss incurred due to insufficient supply of wheat for higher demand 
		return n * P2 

	def penalty_3(self, n): # Cost of holding bags in store 
		return n * P3 

	def penalty_4(self, n): 
		return n * P4 


	def step(self, state, action): 
		day = state[1] 
		n = state[0] # Number of bags already in store 
		sold = self.demand(day) # Number of bags sold # Obtained from Poisson Distribution; demand() function 
		
		# action = Number of bags ordered 
		#action = epsilon_greedy(q, state) 

		if (day!=7): next_state = ( (n - sold + action), (day + 1) )  
		else: next_state = ( (n - sold + action), (1) ) 

		p = 0 
		p1 = 0 
		p2 = 0 
		p3 = 0 
		p4 = 0

		p = self.profit(sold) 

		if (next_state[0] > C): 
			p1 = self.penalty_1(next_state[0] - C) 
			next_state = (C, next_state[1])  
		
		elif ( (n - sold ) < 0): 
			p2 = self.penalty_2(abs(n-sold)) 
			p = self.profit(sold - abs(n-sold)) 
			next_state = (0 + action, next_state[1])  

		#print "P=",p," p_supplier=", p1," p_customer=", p2 

		p3 = self.penalty_3(n - sold) 

		p4 = self.penalty_4(action)  

		''' 
		3 penalty cases: 
			(a) cost of ordering ore than capacity; 
			(b) cost of being short of supply; 
			(c) Cost of holding too many bags; to enable the agent to learn that no need to overfill the storage to meet the demand. 
			(d) Cost incurred in supplying bags (per bag); used to help in ordering only required number of bags and not too many bags 

		''' 
		reward = p - p1 - p2 - p3 - p4  
		# Update q_table 
		#q = update_q_table(q, state, action, next_state, reward) 

		#return state, action, sold, reward, next_state, q 
		return state, reward, sold, next_state 

if __name__ == "__main__": 
	env = Env() 
	state = env.reset() 
	print env.step(state, 20) 