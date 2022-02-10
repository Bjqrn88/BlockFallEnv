import math
import pygame
import random
import BlockFallSettings as bfs

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.allSprits
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface([bfs.BLOCK_SIZE_WIDTH, bfs.BLOCK_SIZE_HEIGHT])
        self.image.fill(bfs.BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def move(self, dx = 0, dy = 0):
        self.x += dx
        self.y += dy

    def reset(self):
        self.x = random.randrange(0, bfs.SCREEN_WIDTH)
        self.y = bfs.START_Y_POS

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def pos(self):
        return [self.x, self.y]

    def outOfbounds(self):
        if self.rect.y > bfs.SCREEN_HEIGHT - bfs.BLOCK_SIZE_HEIGHT or self.rect.x > bfs.SCREEN_WIDTH - bfs.BLOCK_SIZE_WIDTH or self.rect.x < 0:
            self.game.lives -= 1
            return True
        return False
    
    def inGoal(self):
        if self.rect.y > bfs.SCREEN_HEIGHT - bfs.BLOCK_SIZE_HEIGHT - (bfs.GOAL_POST_HEIGHT/2) and self.rect.x > bfs.GOAL_START + bfs.GOAL_POST_WIDTH - 1 and self.rect.x < bfs.GOAL_END - bfs.BLOCK_SIZE_WIDTH + 1:
            return True
        return False
    
    def distFromGoal(self):
        goalCenterX = bfs.SCREEN_WIDTH / 2
        goalCenterY = bfs.SCREEN_HEIGHT
        maxDist = math.sqrt(math.pow(goalCenterX, 2) + math.pow(goalCenterY, 2))
        curDist = abs(math.sqrt(math.pow(goalCenterX - self.x, 2) + math.pow(goalCenterY - self.y, 2)))
        return curDist / maxDist

    def distFromVerticalCenter(self):
        windowCenter = bfs.SCREEN_WIDTH / 2
        return abs(windowCenter - self.x) / windowCenter

class GoalPost(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.allSprits, game.goalPosts
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface([bfs.GOAL_POST_WIDTH, bfs.GOAL_POST_HEIGHT])
        self.image.fill(bfs.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y