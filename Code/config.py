# Means for Poisson Distribution 
# Start Day -> Monday 
m1 = 9.  
m2 = 6.  
m3 = 12. 
m4 = 7. 
m5 = 10.  
m6 = 13. 
m7 = 15. 

# Number of Samples 
N = 50000 

# Number of Days (Repetition of Pattern) 
D = 7 

# Maximum number of bags in Store/Shop; Capacity 
C = 50 

# Profits and Penalties per bag 
P = 10 # Profit per bag 
P1 = 5 # Penalty per bag sent back to supplier 
P2 = 7 # Penalty per bag not available for customer 

# Epsilon for Epsilon-Greedy Approach 
EPSILON = 0.6 

# Discount Factor Gamma 
GAMMA = 0.8 

# Number of Episodes; considering end of day as an end of episode 
NUM_EPISODES = 10000000 