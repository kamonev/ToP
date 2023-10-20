import pygame
from settings import *
from player import Player
from map import world_map
from ray_casting import rayCasting
import math
from drawing import Drawing


pygame.init()
sc = pygame.display.set_mode((width, height))
frames = pygame.time.Clock()
player = Player()
drawing = Drawing(sc)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    player.movement()

    sc.fill(black)

    # sky and floor
    drawing.background()
    drawing.world(player.pos, player.angle)

    pygame.display.flip()
    frames.tick(fps)
