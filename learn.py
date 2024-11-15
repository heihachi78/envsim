import numpy as np


class Q():

    def __init__(self, size, states, actions):
        self.size = size
        self.states = states
        self.actions = actions
        self.mem_size = 10000
        self.q = np.zeros((states * 2 - 1, states * 2 - 1, actions), dtype=np.int16)

        self.eap_mem = np.zeros((self.mem_size, size))
        self.eap_next_mem = np.zeros((self.mem_size, size))
        self.act_mem = np.zeros((self.mem_size))
        self.rew_mem = np.zeros((self.mem_size))

        self.counter = 0
        self.index = 0


    def store(self, eap, action, reward, eap_next):
        self.index = self.counter%self.mem_size
        self.eap_mem[self.index] = eap.copy()
        self.eap_next_mem [self.index] = eap_next.copy()
        self.act_mem[self.index] = action
        self.rew_mem[self.index] = reward

        next_max_reward = np.max(self.q[eap_next[0]][eap_next[1]])
        new_reward = reward + 0.9 * next_max_reward
        self.q[eap[0]][eap[1]][action] = new_reward
        
    
    def get_action(self, eap):
        return np.argmax(self.q[eap[0]][eap[1]])
