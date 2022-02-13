import time
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.utils import get_device
import pygame as pg
import gym

from block_fall.envs import BlockFallEnv
#env = gym.make('block_fall:block_fall-v0')

#print(get_device())


#check_env(env, warn=True)

env = BlockFallEnv()

obs = env.reset()
# print(obs.shape)
# n_obs, reward, done, info = game.step(game.action_space.sample())
# game.render()
# print(n_obs)
# cv2.imshow("hame", obs)

# for _ in range(0, 1024):
#     action = game.action_space.sample()
#     n_obs, reward, done, info = game.step(action)
#     game.render()
#     print(n_obs)
#     if (done):
#         break
#     time.sleep(0.2)


running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    action = env.action_space.sample()
    n_obs, reward, done, info = env.step(action)
    env.render()
    print(n_obs, reward)
    if (done):
        break
    time.sleep(0.1)

pg.quit()