from settings import *
import pygame
import math


class Player:
    def __init__(self):
        self.x, self.y = p_pos
        self.angle = p_angle

    @property
    def pos(self):
        return (self.x, self.y)

    def movement(self):
        sinA = math.sin(self.angle)
        cosA = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.x += p_speed * cosA
            self.y += p_speed * sinA
        if keys[pygame.K_s]:
            self.x += -p_speed * cosA
            self.y += -p_speed * sinA
        if keys[pygame.K_a]:
            self.x += p_speed * sinA
            self.y += -p_speed * cosA
        if keys[pygame.K_d]:
            self.x += -p_speed * sinA
            self.y += p_speed * cosA
        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02

        self.angle %= double_pi