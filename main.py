import pygame
from settings import *
from player import Player
from map import world_map
from ray_casting import rayCasting
import math
from drawing import Drawing


pygame.init()

sc = pygame.display.set_mode((width, height))
sc_map = pygame.Surface((width // map_scale, height // map_scale))

frames = pygame.time.Clock()
player = Player()
drawing = Drawing(sc, sc_map)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    player.movement()

    sc.fill(black)

    # sky and floor
    drawing.background(player.angle)
    drawing.world(player.pos, player.angle)

    drawing.fps(frames)

    drawing.mini_map(player)

    pygame.display.flip()
    frames.tick(fps)
