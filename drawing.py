import pygame
from settings import *
from ray_casting import rayCasting


class Drawing:
    def __init__(self, sc):
        self.sc = sc  # The game screen

    def background(self):
        pygame.draw.rect(self.sc, blue, (0, 0, width, height // 2))
        pygame.draw.rect(self.sc, gray, (0, height // 2, width, height // 2))

    def world(self, player_pos, player_angle):
        rayCasting(self.sc, player_pos, player_angle)
