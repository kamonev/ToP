import pygame
from settings import *
from player import Player
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

    pygame.draw.circle(sc, purple, (int(player.x), int(player.y)), 12)
    pygame.draw.line(sc, purple, player.pos, (player.x + width * math.cos(player.angle), player.y + width * math.sin(player.angle)) )

    pygame.display.flip()
    frames.tick(fps)