import math
import random
import pygame as pg
import gym
import sys
import numpy as np
from gym import spaces

#-----Constants-----
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
START_Y_POS = 20
GOAL_WIDTH = 120
GOAL_START = (SCREEN_WIDTH / 2) - (GOAL_WIDTH / 2)
GOAL_END = (SCREEN_WIDTH / 2) + (GOAL_WIDTH / 2)
GOAL_POST_HEIGHT = 15
GOAL_POST_WIDTH = 4

BLOCK_SIZE_WIDTH = 10
BLOCK_SIZE_HEIGHT = 10

MAX_STEP_SIZE = 10

LIVES = 3

FPS = 30
#-------------------

#--------ENV--------
class BlockFallEnv(gym.Env):
    def __init__(self, hideDisplay=False):
        pg.init()
        pg.display.init()
        if (hideDisplay):
            self.screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], flags=pg.HIDDEN)
        else:
            self.screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(low=0.0, high=float(SCREEN_WIDTH), shape=(3,), dtype=np.float32)
        self.reset()

    def reset(self):
        self.done = False
        self.allSprits = pg.sprite.Group()
        self.goalPosts = pg.sprite.Group()
        self.lives = LIVES

        GoalPost(self, GOAL_START, SCREEN_HEIGHT - GOAL_POST_HEIGHT)
        GoalPost(self, GOAL_END, SCREEN_HEIGHT - GOAL_POST_HEIGHT)
        self.block = Block(self, random.randrange(0, SCREEN_WIDTH), START_Y_POS)
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
        self.screen.fill(WHITE)
        self.allSprits.draw(self.screen)

    def _getObs(self):
        state = [self.block.x, self.block.y, self.block.distFromGoal()]
        state = np.array(state)
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
#-------------------

#------Sprites------
class Block(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.allSprits
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface([BLOCK_SIZE_WIDTH, BLOCK_SIZE_HEIGHT])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def move(self, dx = 0, dy = 0):
        self.x += dx
        self.y += dy

    def reset(self):
        self.x = random.randrange(0, SCREEN_WIDTH)
        self.y = START_Y_POS

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def pos(self):
        return [self.x, self.y]

    def outOfbounds(self):
        if self.rect.y > SCREEN_HEIGHT - BLOCK_SIZE_HEIGHT or self.rect.x > SCREEN_WIDTH - BLOCK_SIZE_WIDTH or self.rect.x < 0:
            self.game.lives -= 1
            return True
        return False
    
    def inGoal(self):
        if self.rect.y > SCREEN_HEIGHT - BLOCK_SIZE_HEIGHT - (GOAL_POST_HEIGHT/2) and self.rect.x > GOAL_START + GOAL_POST_WIDTH - 1 and self.rect.x < GOAL_END - BLOCK_SIZE_WIDTH + 1:
            return True
        return False
    
    def distFromGoal(self):
        goalCenterX = SCREEN_WIDTH / 2
        goalCenterY = SCREEN_HEIGHT
        maxDist = math.sqrt(math.pow(goalCenterX, 2) + math.pow(goalCenterY, 2))
        curDist = abs(math.sqrt(math.pow(goalCenterX - self.x, 2) + math.pow(goalCenterY - self.y, 2)))
        return curDist / maxDist

    def distFromVerticalCenter(self):
        windowCenter = SCREEN_WIDTH / 2
        return abs(windowCenter - self.x) / windowCenter

class GoalPost(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.allSprits, game.goalPosts
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface([GOAL_POST_WIDTH, GOAL_POST_HEIGHT])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
#-------------------