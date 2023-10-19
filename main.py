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

    rayCasting(sc, player.pos, player.angle)

    pygame.display.flip()
    frames.tick(fps)