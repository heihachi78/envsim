import numpy as np
import cv2
from PIL import Image
from environment import Env
from foo import Foo
from learn import Q


VISUALS_SPEED = 10
ENV_SIZE = 32
N_FOOD = 100
N_ENEMY = 32
MAX_LIFE = 100
FOO_STEP_COST = 1
FOO_FOOD_LIFE = 74
FOO_ENEMY_DAMAGE = 90

eps = 1.0
g = 0.999

env = Env(size=ENV_SIZE)
env.add_enemy(N_ENEMY)
env.add_food(N_FOOD)
foo = Foo(env_size=ENV_SIZE, life=MAX_LIFE, step_cost=FOO_STEP_COST, food_life=FOO_FOOD_LIFE, enemy_damage=FOO_ENEMY_DAMAGE)
env.add_foo(foo=foo)
qt = Q(states=env.return_states_high_value, actions=foo.action_space)

for e in range(100000):
    sum_reward = 0
    state_old = env.get_env_at_pos(x=foo.posX, y=foo.posY)

    while foo.life > 0 and len(env.env[env.env == env.FOOD]) > 0:
        foo.move_random(state_old, qt, eps)
        state_next = env.get_env_at_pos(x=foo.posX, y=foo.posY)
        qt.store(state_old, foo.action, foo.reward, state_next)
        if not e % 100:
            env.visualize(VISUALS_SPEED)
        state_old = state_next
        sum_reward += foo.reward
    eps *= g
    print(e, 'data:', len(qt.q2), 'collected:', foo.food_collected, 'sum reward:', sum_reward, 'eps:', eps)

    env = Env(size=ENV_SIZE)
    env.add_enemy(N_ENEMY)
    env.add_food(N_FOOD)
    foo = Foo(env_size=ENV_SIZE, life=MAX_LIFE, step_cost=FOO_STEP_COST, food_life=FOO_FOOD_LIFE, enemy_damage=FOO_ENEMY_DAMAGE)
    env.add_foo(foo=foo)

cv2.waitKey(0)
