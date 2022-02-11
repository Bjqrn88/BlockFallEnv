import time
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.utils import get_device
import BlockFallEnvV2 as BFE
import cv2

#print(get_device())
game = BFE.BlockFallEnv(False)

#check_env(game, warn=True)

obs = game.reset()
# print(obs.shape)
# n_obs, reward, done, info = game.step(game.action_space.sample())
# game.render()
# print(n_obs)
# cv2.imshow("hame", obs)

for _ in range(0, 1024):
    action = game.action_space.sample()
    n_obs, reward, done, info = game.step(action)
    game.render()
    print(n_obs)
    if (done):
        break
    time.sleep(0.2)