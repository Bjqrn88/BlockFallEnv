import time
import pygame as pg
pg.init()
pg.display.init()
screen = pg.display.set_mode([600, 400])
screen.fill((255,0,0))
pg.display.flip()
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

pg.quit()