from wh import Env 

env = Env() 
state = env.reset() 
print env.step(state, 20) 