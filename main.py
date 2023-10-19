import pygame
from settings import *



pygame.init()
sc = pygame.display.set_mode((width, height))
frames = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    sc.fill(black)

    pygame.draw.circle(sc, purple, p_pos, 12)

    pygame.display.flip()
    frames.tick()