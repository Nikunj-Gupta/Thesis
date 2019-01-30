from config import * 

import numpy as np 

# Poisson Distribution; Function to return demand for a given day 
def demand(day): 
	#s = np.random.poisson(lam=(m1,m2,m3,m4,m5,m6,m7), size=(N, D)) # dimensions of s = N x D 
	
	s = np.random.poisson(lam=(m1,m2,m3,m4,m5,m6,m7)) # dimensions of s = 1 x D 

	return s[day-1] 


# printing means of each day 
def util1(): 
	a=[] 
	for d in range(D): 
		for i in s: 
			a.append(i[d]) 
		print np.mean(a) 
		a=[]


''' 
state = (Bags_in_store, Day) # tuple of number of bags present in store on day 'Day' and the present day 'Day'
action = bags_to_order # from supplier/manufacturer  
''' 


# Reset at the beginning of a new episode 
def reset(): 
	n = np.random.randint(C+1) # number of bags (today) 
	d = np.random.randint(1, D+1) # day (today) 
	state = (n, d) 
	return state 


def profit(n): 
	return n * P 


def penalty_1(n): # Bags sent back to supplier; Loss incurred when extra bags were ordered 
	return n * P1 


def penalty_2(n): # Customers sent back without wheat; Loss incurred due to insufficient supply of wheat for higher demand 
	return n * P2 


def step(state, q): 
	day = state[1] 
	n = state[0] # Number of bags already in store 
	sold = demand(day) # Number of bags sold # Obtained from Poisson Distribution; demand() function 
	
	# action = Number of bags ordered 
	action = epsilon_greedy(q, state) 

	if (day!=7): next_state = ( (n - sold + action), (day + 1) )  
	else: next_state = ( (n - sold + action), (1) ) 

	p = 0 
	p1 = 0 
	p2 = 0 

	p = profit(sold) 

	if (next_state[0] > C): 
		p1 = penalty_1(next_state[0] - C) 
		next_state = (C, next_state[1])  
	
	elif ( (n - sold ) < 0): 
		p2 = penalty_2(abs(n-sold)) 
		p = profit(sold - abs(n-sold)) 
		next_state = (0 + action, next_state[1])  

	#print "P=",p," p_supplier=", p1," p_customer=", p2 

	reward = p - p1 - p2 # 2 penalty cases: (a) cost of ordering ore than capacity; (b) cost of being short of supply 

	# Update q_table 
	q = update_q_table(q, state, action, next_state, reward) 

	return state, action, sold, reward, next_state, q 





# Initialization of the Q Table as a dictionary: keys = ((Bags, Day), Action); values = 0 initially 
def q_table(): 
	q = {} 
	keys = [] 
	for k in range(C+1): 
		for i in range(C+1): 
			for j in range(1, D+1): 
				keys.append(((i,j), k)) 
	#print len(keys) 
	for i in range(len(keys)): 
		q.update({keys[i]: 0}) 

	return q 

def epsilon_greedy(q, state): 
	action = 0 
	if (np.random.rand(1)[0] < EPSILON): 
		action = np.random.randint(C+1) 
	else: 
		arr = [] 
		for i in range(C+1): 
			arr.append(q[(state, i)]) 
		action = np.argmax(np.array(arr)) 
	return action 


def update_q_table(q, state, action, next_state, reward): 
	arr = [] 
	for i in range(C+1): 
		arr.append(q[(next_state, i)]) 

	q[(state, action)] = reward + GAMMA * max(arr) 
	return q 

def q_learning(): 
	result_array = [] 
	q = q_table() 
	for i in range(1, NUM_EPISODES+1): 
		state = reset() 
		state, action, sold, reward, next_state, q = step(state, q) 
		observation = [state, action, sold, reward, next_state] 
		save_to_file(observation) 
		result_array.append(observation) # storing the observation list as result 
		print "Episode ", i 
		print observation 
		print
	return result_array, q 

def save_to_file(observation): 
	#print type(np.array(observation))
	f = open("output.txt", "a+") 
	for i in observation: 
		f.write(str(i)+', ')
	f.write("\n")  
	f.close() 


def test3(): 
	q_table() 

def test2(): 
	state = (46, 3) 
	action = 14 
	sold = 5 
	print step(state, action) 

def test(): 
	for i in range(5): 
		state = reset() 
		state, action, sold, reward, next_state = step(state, np.random.randint(50)) 
		print "State:\t\t", state 
		print "Action:\t\t", action  
		print "Demand:\t\t", sold  
		print "Reward:\t\t", reward   
		print "Next State:\t", next_state 
		print 

def util2(state, q): 
	arr = [] 
	for i in range(C+1): 
		arr.append(q[(state, i)]) 
	return np.argmax(np.array(arr))  

def test_q(q): 
	state = (0, 1) 
	print "State: ", state, " Action: ", util2(state, q) 

	state = (0, 2) 
	print "State: ", state, " Action: ", util2(state, q) 

	state = (0, 3) 
	print "State: ", state, " Action: ", util2(state, q) 

	state = (0, 4) 
	print "State: ", state, " Action: ", util2(state, q) 

	state = (0, 5) 
	print "State: ", state, " Action: ", util2(state, q) 

	state = (0, 6) 
	print "State: ", state, " Action: ", util2(state, q) 

	state = (0, 7) 
	print "State: ", state, " Action: ", util2(state, q) 

def test_q_2(): 
	q = np.load('outputs/q_10000000.npy').item() 
	state = reset() 
	for i in range(30):
		state, action, sold, reward, next_state, q = step(state, q) 
		print "State: ", state , "  ",
		print "Action: ", action, "  " ,
		print "Demand: ", sold, "  " ,
		print "NextState: ", next_state, "  " 
		state = next_state 
	

if __name__ == '__main__': 
	#s = demand() 
	#print(len(s))
	#util1() 
	#test3() 
	#result, q = q_learning() 
	#np.save("q.npy", q) 
	test_q_2() 
