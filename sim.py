import numpy as np
import cv2
from PIL import Image
from environment import Env
from foo import Foo
from learn import Q


VISUALS_SPEED = 100
ENV_SIZE = 10
N_FOOD = 10
N_ENEMY = 3
MAX_LIFE = 100
FOO_STEP_COST = 1
FOO_FOOD_LIFE = 25
FOO_ENEMY_DAMAGE = 100


qt = Q(states=6, size=12, actions=9)

for e in range(100000):
    env = Env(size=ENV_SIZE)
    env.add_enemy(N_ENEMY)
    env.add_food(N_FOOD)
    foo = Foo(env_size=ENV_SIZE, life=MAX_LIFE, step_cost=FOO_STEP_COST, food_life=FOO_FOOD_LIFE, enemy_damage=FOO_ENEMY_DAMAGE)
    env.add_foo(foo=foo)
    eap_old = env.get_env_at_pos(x=foo.posX, y=foo.posY)

    while foo.life > 0 and len(env.env[env.env == env.FOOD]) > 0:
        foo.move_random(eap_old, qt)
        eap_next = env.get_env_at_pos(x=foo.posX, y=foo.posY)
        qt.store(eap_old, foo.action, foo.reward, eap_next)
        if not e % 250:
            env.visualize(VISUALS_SPEED)
        eap_old = eap_next
    print(e, np.round(np.sum(qt.q), 2), foo.food_collected, foo.score)


cv2.waitKey(0)
