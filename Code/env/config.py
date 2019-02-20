import numpy as np 

# Number of Samples 
N = 50000 

# Number of Days (Repetition of Pattern) 
D = 7 

# Maximum number of bags in Store/Shop; Capacity 
C = 50 

means = np.random.randint(C, size=D) 

# Means for Poisson Distribution 
# Start Day -> Monday 
m1 =  means[0] 
m2 = means[1] 
m3 = means[2] 
m4 = means[3] 
m5 = means[4] 
m6 = means[5] 
m7 = means[6] 

# Profits and Penalties per bag 
P = 10 # Profit per bag 
P1 = 5 # Penalty per bag sent back to supplier 
P2 = 7 # Penalty per bag not available for customer 
P3 = 3 # Cost of standby of bags (per bag) 
P4 = 2 # Cost of supplying bags (per bag) 

# Epsilon for Epsilon-Greedy Approach 
EPSILON = 0.6 

# Discount Factor Gamma 
GAMMA = 0.8 

# Number of Episodes; considering end of day as an end of episode 
NUM_EPISODES = 1000000

path = "outputs/v2/" 

###-----------------------------------------------------------------------------------------------------###

 