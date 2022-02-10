from stable_baselines3 import PPO
import BlockFallEnv as BFE
import time

game = BFE.BlockFallEnv()

model = PPO.load('./train/train_basic6/best_model_400000')

for episode in range(100):
    obs = game.reset()
    done = False
    total_reward = 0
    while not done:
        action, _ = model.predict(obs)
        obs, reward, done, info = game.step(action)
        game.render()
        total_reward += reward
        if (done):
            break
    print('Total Reward for episode {} is {}'.format(total_reward, episode))
    time.sleep(2)