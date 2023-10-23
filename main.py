import pygame
from settings import *
from player import Player
from sprite_objects import *
from ray_casting import rayCasting
import math
from drawing import Drawing


pygame.init()

sc = pygame.display.set_mode((width, height))
sc_map = pygame.Surface((width // map_scale, height // map_scale))

sprites = Sprites()
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
    walls = rayCasting(player, drawing.textures)
    drawing.world(walls + [obj.object_locate(player, walls) for obj in sprites.list_of_objects])
    drawing.fps(frames)

    drawing.mini_map(player)

    pygame.display.flip()
    frames.tick(fps)
