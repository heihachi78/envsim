import numpy as np



class Foo():

    def __init__(self, env_size, life, step_cost, food_life, enemy_damage):
        self.posX = np.random.randint(env_size)
        self.posY = np.random.randint(env_size)
        self.env_size = env_size
        self.life = life
        self.max_life = life
        self.step_cost = step_cost
        self.food_life = food_life
        self.enemy_damage = enemy_damage
        self.action_space = 9
        self.food_collected = 0
        self.score = 0
        self.reward = 0


    def get_pos(self):
        return (self.posX, self.posY)


    def act(self, action):
        if action == 0:
            self.move(0, 0)
        if action == 1:
            self.move(0, 1)
        if action == 2:
            self.move(1, 0)
        if action == 3:
            self.move(0, -1)
        if action == 4:
            self.move(-1, 0)
        if action == 5:
            self.move(1, 1)
        if action == 6:
            self.move(1, -1)
        if action == 7:
            self.move(-1, 1)
        if action == 8:
            self.move(-1, -1)


    def move_random(self, eap, qt):
        if self.life > 0:
            if np.random.rand() < 0.1:
                self.action = np.random.randint(self.action_space)
            else:
                self.action = qt.get_action(eap)
            self.act(self.action)
    

    def move(self, deltaX, deltaY):
        if self.life > 0:
            self.posX = self.posX + deltaX
            self.posY = self.posY + deltaY
            if self.posX < 0:
                self.posX = 0
            if self.posY < 0:
                self.posY = 0
            if self.posX >= self.env_size:
                self.posX = self.env_size - 1
            if self.posY >= self.env_size:
                self.posY = self.env_size - 1
            self.life -= self.step_cost
            self.score -= self.step_cost
            self.reward = -self.step_cost

    
    def eat(self):
        self.life += self.food_life
        self.food_collected += 1
        self.score += self.food_life
        self.reward = self.food_life
        if self.life > self.max_life:
            self.life = self.max_life

    
    def fight(self):
        self.life -= self.enemy_damage
        self.score -= self.enemy_damage
        self.reward = -self.enemy_damage
