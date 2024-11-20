import numpy as np
import cv2
from PIL import Image

from foo import Foo



class Env():

    def __init__(self, size):
        self.size = size
        self.n_food = 0
        self.n_enemy = 0
        self.n_foo = 0
        self._make_env()
        self.closest_food_index = 0
        self.closest_enemy_index = 0
        
        self.GROUND = 0
        self.ENEMY = 1
        self.FOOD = 2
        self.FOO = 3
        self.FOO_DEAD = 4
        self.VISITED = 5
        
        self.ENEMY_COLOR = [0, 0, 255]
        self.CLOSEST_FOOD = [51, 255, 255]
        self.FOOD_COLOR = [0, 128, 0]
        self.FOO_COLOR = [255, 0, 0]
        self.FOO_DEAD_COLOR = [64, 64, 64]
        self.VISITED_COLOR = [128, 128, 128]

        self.foo_visited = list()
        self.return_size = 4
        self.return_states_high_value = self.decode(''.join([str(self.size-1) for k in range(self.return_size)]), self.size)


    def add_food(self, amount):
        self.n_food = amount
        self.food = np.random.randint(0, self.size, (2, self.n_food))
        self._make_env()

    
    def add_enemy(self, amount):
        self.n_enemy = amount
        self.enemy = np.random.randint(0, self.size, (2, self.n_enemy))
        self._make_env()


    def add_foo(self, foo : Foo):
        self.n_foo = 1
        self.foo = foo
        regen_pos = True
        while regen_pos:
            regen_pos = False
            foo.posX = np.random.randint(self.size)
            foo.posY = np.random.randint(self.size)
            for f in range(self.n_food):
                if self.food[0][f] == foo.posX and self.food[1][f] == foo.posY:
                  regen_pos = True
            for e in range(self.n_enemy):
                if self.enemy[0][e] == foo.posX and self.enemy[1][e] == foo.posY:
                  regen_pos = True

    def _make_env(self):
        self.env = np.zeros((self.size, self.size), dtype=np.uint8)
        if self.n_enemy:
            self.env[tuple(self.enemy)] = self.ENEMY
        if self.n_food:
            self.env[tuple(self.food)] = self.FOOD
        if self.n_foo:
            for v in self.foo_visited:
                self.env[v] = self.VISITED
            if self.env[self.foo.get_pos()] == self.ENEMY:
                self.foo.fight()
            if self.env[self.foo.get_pos()] == self.FOOD:
                self.foo.eat()
            if self.foo.life > 0:
                self.env[self.foo.get_pos()] = self.FOO
            else:
                self.env[self.foo.get_pos()] = self.FOO_DEAD
            self.foo_visited.append(self.foo.get_pos())

    def encode(self, number, base):
        if not number:
            return ['0']
        digits = []
        while number:
            digits.append(str(number % base))
            number //= base
        return list(reversed(digits))

    def decode(self, number, base):
        try:
            return int(''.join([str(a) for a in number]), base)
        except:
            return 0
    
    def get_env_at_pos(self, x, y):
        self._make_env()
        eap = np.zeros(self.return_size, dtype=np.int16)

        md = 99999999999999999999
        fx, fy = self.foo.get_pos()
        closest_food_index = 0
        for i in range(self.n_food):
            if (self.food[0][i], self.food[1][i]) in self.foo_visited:
                continue
            cdx = fx - self.food[0][i]
            cdx *= cdx
            cdy = fy - self.food[1][i]
            cdy *= cdy
            if md > cdy + cdx:
                md = cdy + cdx
                closest_food_index = i
        eap[0] = (self.food[0][closest_food_index] - fx)
        eap[1] = (self.food[1][closest_food_index] - fy)
        self.closest_food_index = closest_food_index

        md = 99999999999999999999
        fx, fy = self.foo.get_pos()
        closest_enemy_index = 0
        for i in range(self.n_enemy):
            cdx = fx - self.enemy[0][i]
            cdx *= cdx
            cdy = fy - self.enemy[1][i]
            cdy *= cdy
            if md > cdy + cdx:
                md = cdy + cdx
                closest_enemy_index = i
        eap[2] = (self.enemy[0][closest_enemy_index] - fx)
        eap[3] = (self.enemy[1][closest_enemy_index] - fy)
        self.closest_enemy_index = closest_enemy_index

        r = eap + self.size
        r = r - min(r)
        return self.decode(r, self.size)


    def visualize(self, speed):
        self._make_env()
        visuals = np.zeros((self.size, self.size, 3), dtype=np.uint8)
        visuals[self.env == self.ENEMY] = self.ENEMY_COLOR
        visuals[self.env == self.FOOD] = self.FOOD_COLOR
        visuals[self.env == self.FOO] = self.FOO_COLOR
        visuals[self.env == self.FOO_DEAD] = self.FOO_DEAD_COLOR
        visuals[self.env == self.VISITED] = self.VISITED_COLOR
        visuals[self.food[0][self.closest_food_index]][self.food[1][self.closest_food_index]] = self.CLOSEST_FOOD

        img = Image.fromarray(visuals, 'RGB')
        img = img.resize((800, 800), Image.NEAREST)
        cv2.imshow('env', np.array(img))
        cv2.waitKey(speed)
