import pygame
from settings import *
from player import Player
from map import world_map
from ray_casting import rayCasting
import math


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

    # sky and floor
    pygame.draw.rect(sc, blue, (0, 0, width, height // 2))
    pygame.draw.rect(sc, gray, (0, height // 2, width, height // 2))

    rayCasting(sc, player.pos, player.angle)

    pygame.display.flip()
    frames.tick(fps)