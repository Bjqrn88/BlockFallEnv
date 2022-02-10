import random
import pygame as pg
import gym
import sys
import cv2
import numpy as np
from gym import spaces

import BlockFallSettings as bfs
import BlockFallSprites as sprits

class BlockFallEnv(gym.Env):
    def __init__(self, hideDisplay=False):
        pg.init()
        pg.display.init()
        if (hideDisplay):
            self.screen = pg.display.set_mode([bfs.SCREEN_WIDTH, bfs.SCREEN_HEIGHT], flags=pg.HIDDEN)
        else:
            self.screen = pg.display.set_mode([bfs.SCREEN_WIDTH, bfs.SCREEN_HEIGHT])
        self.clock = pg.time.Clock()

        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(low=0, high=255, shape=(100, 150, 1), dtype=np.uint8)
        self.reset()

    def reset(self):
        self.done = False
        self.allSprits = pg.sprite.Group()
        self.goalPosts = pg.sprite.Group()
        self.lives = bfs.LIVES

        sprits.GoalPost(self, bfs.GOAL_START, bfs.SCREEN_HEIGHT - bfs.GOAL_POST_HEIGHT)
        sprits.GoalPost(self, bfs.GOAL_END, bfs.SCREEN_HEIGHT - bfs.GOAL_POST_HEIGHT)
        self.block = sprits.Block(self, random.randrange(0, bfs.SCREEN_WIDTH), bfs.START_Y_POS)
        self.allSprits.update()
        self.draw()
        return self._getObs()

    def step(self, action):
        if action == 0: 
            self.block.move(dx=0, dy=5)
        if action == 1:
            self.block.move(dx=-2, dy=5)
        if action == 2:
            self.block.move(dx=2, dy=5)

        self.allSprits.update()
        self.draw()

        obs = self._getObs()
        reward = self._rewardFunc()
        done = self._checkDone()
        _blockPos = self.block.pos()
        _distToGoal = self.block.distFromVerticalCenter()
        info = {"Block Pos": "x: {}, y: {}, dist: {}, lives: {}, done: {}, reward: {}".format(_blockPos[0], _blockPos[1], _distToGoal, self.lives, done, reward)}
        
        if (self.block.outOfbounds() or self.block.inGoal()):
            self.block.reset()

        return obs, reward, done, info
    
    def render(self):
        pg.display.flip()

    def close(self):
        pg.quit()
        sys.exit()

    def draw(self):
        self.screen.fill(bfs.WHITE)
        self.allSprits.draw(self.screen)
        

    def _getObs(self):
        gray = cv2.cvtColor(pg.surfarray.array3d(self.screen), cv2.COLOR_BGR2GRAY)
        resize = cv2.resize(gray, (150, 100), interpolation=cv2.INTER_BITS)
        state = np.reshape(resize, (100, 150, 1))
        return state

    def _rewardFunc(self):
        if (self.block.outOfbounds()):
            return -100 * self.block.distFromVerticalCenter()
        
        if (self.block.inGoal()):
            return 1000
        
        return -10 * self.block.distFromVerticalCenter()

    def _checkDone(self):
        if self.lives <= 0:
            return True
        return False