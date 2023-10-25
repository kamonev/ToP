import pygame
from settings import *
from player import Player
from sprite_objects import *
from ray_casting import rayCasting
import math
from drawing import Drawing
from interactions import Interaction

pygame.init()

sc = pygame.display.set_mode((width, height))
pygame.mouse.set_visible(False)
sc_map = pygame.Surface(minimap_res)

sprites = Sprites()
frames = pygame.time.Clock()
player = Player(sprites)
drawing = Drawing(sc, sc_map, player)
interaction = Interaction(player, sprites, drawing)

while True:
    
    player.movement()

    

    # sky and floor
    drawing.background(player.angle)
    walls = rayCasting(player, drawing.textures)
    drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])
    drawing.fps(frames)
    drawing.mini_map(player)
    drawing.player_weapon()

    interaction.interaction_objects()
    
    pygame.display.flip()
    frames.tick(fps)
