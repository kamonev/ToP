import pygame
from settings import *
from player import Player



pygame.init()
sc = pygame.display.set_mode((width, height))
frames = pygame.time.Clock()
player = Player()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    player.movement()

    sc.fill(black)

    pygame.draw.circle(sc, purple, player.pos, 12)

    pygame.display.flip()
    frames.tick(fps)