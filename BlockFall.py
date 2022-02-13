import pygame
import random

#-----Constants-----
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
START_Y_POS = 20
GOAL_WIDTH = 30
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

#------Classes------
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface([w,h])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self, offsetX, offsetY):
        self.rect.x += offsetX
        self.rect.y += offsetY

    def reset(self):
        self.rect.x = random.randrange(0,SCREEN_WIDTH)
        self.rect.y = START_Y_POS

class GoalPost(pygame.sprite.Sprite):
    def __init__(self, postWidth, postHeight, x, y):
        super().__init__()
        self.image = pygame.Surface([postWidth,postHeight])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Game(object):
    def __init__(self):
        self.game_over = False
        self.blocks = pygame.sprite.Group()
        self.goalPosts = pygame.sprite.Group()
        self.move_LEFT = False
        self.move_RIGHT = False
        self.stepSize = 0
        self.keydownCount = 0
        self.score = 0
        self.lives = LIVES

        goalPostStart = GoalPost(GOAL_POST_WIDTH, GOAL_POST_HEIGHT, GOAL_START, SCREEN_HEIGHT - GOAL_POST_HEIGHT)
        goalPostEnd = GoalPost(GOAL_POST_WIDTH, GOAL_POST_HEIGHT, GOAL_END, SCREEN_HEIGHT - GOAL_POST_HEIGHT)
        self.goalPosts.add(goalPostStart)
        self.goalPosts.add(goalPostEnd)

        block = Block(random.randrange(0, SCREEN_WIDTH), START_Y_POS, BLOCK_SIZE_WIDTH, BLOCK_SIZE_HEIGHT)
        self.blocks.add(block)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 return True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                if event.key == pygame.K_LEFT:
                    self.move_LEFT = True
                    self.move_RIGHT = False
                if event.key == pygame.K_RIGHT:
                    self.move_LEFT = False
                    self.move_RIGHT = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.move_LEFT = False
                    self.keydownCount = 0
                    self.stepSize = 0
                if event.key == pygame.K_RIGHT:
                    self.move_RIGHT = False
                    self.keydownCount = 0
                    self.stepSize = 0

        return False

    def run_logic(self):
        if not self.game_over:
            if self.move_LEFT or self.move_RIGHT:
                self.keydownCount += 1
            if (self.stepSize < MAX_STEP_SIZE):
                self.stepSize = self.keydownCount / 2
            else:
                self.keydownCount = FPS
                self.stepSize = MAX_STEP_SIZE

            for b in self.blocks:
                self._checkForGoal(b)
                if self._checkOutOfBound(b):
                    self.lives -= 1
                    print('OUT')
                if self.lives <= 0:
                    self.game_over = True
                    print('GAME OVER')
                    break
                b.move(0,5) #Move down
                if self.move_LEFT:
                    b.move(-self.stepSize, 0)
                elif self.move_RIGHT:
                    b.move(self.stepSize, 0)

    def display_frame(self, screen):
        screen.fill(WHITE)
        self.goalPosts.draw(screen)
        self.blocks.draw(screen)
        self._printScore(screen)
        self._printLives(screen)
        pygame.display.update()

    def _checkForGoal(self, block):
        if block.rect.y > SCREEN_HEIGHT - BLOCK_SIZE_HEIGHT - (GOAL_POST_HEIGHT/2) and block.rect.x > GOAL_START + GOAL_POST_WIDTH - 1 and block.rect.x < GOAL_END - BLOCK_SIZE_WIDTH + 1:
            self.score += 1
            block.reset()

    def _checkOutOfBound(self, block):
        if block.rect.y > SCREEN_HEIGHT - BLOCK_SIZE_HEIGHT or block.rect.x > SCREEN_WIDTH - BLOCK_SIZE_WIDTH or block.rect.x < 0:
            block.reset()
            return True
        return False

    def _printScore(self, screen):
        font = pygame.font.SysFont(None, 30)
        if self.game_over:
            textsurface = font.render('Score: GAME OVER' , True, BLACK)
        else:
            textsurface = font.render('Score: '+str(self.score), True, BLACK)
        screen.blit(textsurface, (5, 5))

    def _printLives(self, screen):
        font = pygame.font.SysFont(None, 30)
        if self.lives == 3:
            textsurface = font.render('Live: <3 <3 <3', True, BLACK)
        elif self.lives == 2:
            textsurface = font.render('Live: <3 <3 --', True, BLACK)
        elif self.lives == 1:
            textsurface = font.render('Live: <3 -- --', True, BLACK)
        else:
            textsurface = font.render('Live: -- -- --', True, BLACK)
        screen.blit(textsurface, (SCREEN_WIDTH - textsurface.get_width() - 5, 5))
#-------------------

#-------Main--------
def main():
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Falling block')
    pygame.mouse.set_visible(False)

    done = False
    clock = pygame.time.Clock()

    game = Game()

    while not done:
        done = game.process_events()
        game.run_logic()
        game.display_frame(screen)
        clock.tick(FPS)

    pygame.quit()
#-------------------

if __name__ == "__main__":
    main()
