import gym 
import numpy as np 

from keras import layers 
from keras.models import Model 
from keras import backend as Backend 
from keras import optimizers 
from keras import utils 

from wh import Env  

class Agent(object): 

	def __init__(self, in_dim, out_dim, hidden_dim=[32, 32]): 
		self.in_dim = in_dim 
		self.out_dim = out_dim 

		self._build_network(in_dim, out_dim, hidden_dim) 
		self._train() 

	def _build_network(self, in_dim, out_dim, hidden_dim=[32, 32]): 
		self.X = layers.Input(shape=(in_dim,)) 
		net = self.X 

		for h in hidden_dim: 
			net = layers.Dense(h)(net) 
			net = layers.Activation("relu")(net) 

		net = layers.Dense(out_dim)(net) 
		net = layers.Activation("softmax")(net) 

		self.model = Model(inputs=self.X, outputs=net) 

	def _train(self): 
		action_prob_placeholder = self.model.output 
		action_onehot_placeholder = Backend.placeholder(shape=(None, self.out_dim), name="action_onehot") 
		discount_reward_placeholder = Backend.placeholder(shape=(None,), name="discount_reward") 

		action_prob = Backend.sum(action_prob_placeholder * action_onehot_placeholder, axis=1) 
		log_action_prob = Backend.log(action_prob) 

		loss = - log_action_prob * discount_reward_placeholder 
		loss = Backend.mean(loss) 

		adam = optimizers.Adam() 

		updates = adam.get_updates(params=self.model.trainable_weights, loss=loss) 

		self.train_function = Backend.function(inputs=[self.model.input, action_onehot_placeholder, discount_reward_placeholder], outputs=[], updates=updates) 

	
	def _action(self, state): 
		state = np.expand_dims(state, axis=0) 
		action_prob = np.squeeze(self.model.predict(state)) 
		return np.random.choice(np.arange(self.out_dim), p=action_prob) 

	def fit(self, S, A, R):	
		action_onehot = utils.to_categorical(A, num_classes=self.out_dim) 
		discount_reward = compute_discountR(R) 

		self.train_function([S, action_onehot, discount_reward]) 

def compute_discountR(R, discount_rate = 0.99): 
	discount_r = np.zeros_like(R, dtype=np.float32) 
	running_add = 0 

	for t in reversed(range(len(R))): 
		running_add = running_add * discount_rate + R[t] 
		discount_r[t] = running_add 

	discount_r -= (discount_r.mean() / discount_r.std()) 

	return discount_r 

def run_episode(env, agent): 
	done = False 
	S = [] 
	A = [] 
	R = [] 

	s = env.reset() 
	#print "State: ", np.expand_dims(s, axis=0)

	total_reward = 0 

	i=0

	while not done: 
		if (i==1):
			done = True 
		a = agent._action(s) 

		#s2, r, done, info = env.step(a) 
		s, r, sold, s2 = env.step(s, a) 
		total_reward = total_reward + r 

		S.append(s) 
		A.append(a) 
		R.append(r) 

		s = s2 

		if done: 
			S = np.array(S) 
			A = np.array(A) 
			R = np.array(R) 

			agent.fit(S, A, R) 
		i = i+1 

	return total_reward 


def exploit(agent): 
	s = env.reset() 
	for i in range(30): 
		a = agent._action(s) 
		s, r, sold, s2 = env.step(s, a) 
		print "State: ", s , "  ",
		print "Action: ", a, "  " ,
		print "Demand: ", sold, "  " ,
		print "NextState: ", s2, "  " 
		s = s2 



#env = gym.make("CartPole-v0") 
env = Env() 
in_dim = env.observation_space 
out_dim = env.action_space 
agent = Agent(in_dim, out_dim, [32, 32]) 

for episode in range(200000): 
	reward = run_episode(env, agent) 
	print (episode, reward) 
exploit(agent) 
#env.close() 