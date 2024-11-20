import numpy as np


class Q():

    def __init__(self, states, actions):
        self.states = states
        self.actions = actions
        self.q2 = dict()

    def store(self, current_state, action, reward, next_state):
        keysList = list(self.q2.keys())
        new_reward = 0
        if next_state not in keysList:
            new_reward = reward
        else:
            keysList2 = list(self.q2[next_state].keys())
            if action not in keysList2:
                new_reward = reward
            else:
                new_reward = reward + 0.9 * self.q2[next_state][action]

        if current_state not in keysList:
            self.q2[current_state] = {action : new_reward}
        else:
            self.q2[current_state][action] = new_reward
    
    def get_action(self, current_state):
        try:
            return max(self.q2[current_state].values())
        except:
            return np.random.randint(self.actions)
