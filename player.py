from settings import *
import pygame
import math
from map import collision_walls

class Player:
    def __init__(self, sprites):
        self.x, self.y = p_pos
        self.sprites = sprites
        self.angle = p_angle
        self.sensivity = 0.0015
        # collision parametrs
        self.side = 20 
        self.rect = pygame.Rect(*p_pos, self.side, self.side)


        #weapon
        self.shot = False

    @property
    def pos(self): 

        return [self.x, self.y]

    @property
    def collision_list(self):
        return collision_walls + [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in 
                                  self.sprites.list_of_objects if obj.blocked]

    def detect_collision(self, dx, dy):
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(self.collision_list)

        if len(hit_indexes):
            delta_x, delta_y = 0, 0
            for hit_index in hit_indexes:
                hit_rect = self.collision_list[hit_index]
                if dx > 0:
                    delta_x += next_rect.right - hit_rect.left
                else:
                    delta_x += hit_rect.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                else:
                    delta_y += hit_rect.bottom - next_rect.top

            if abs(delta_x - delta_y) < 10:
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0
        self.x += dx
        self.y += dy
  

    def movement(self):
        self.keys_control()
        self.mouse_control()
        self.rect.center = self.x, self.y
        self.angle %= double_pi



    def keys_control(self):
        sinA = math.sin(self.angle)
        cosA = math.cos(self.angle)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            exit()
        if keys[pygame.K_w]:
            dx = p_speed * cosA
            dy = p_speed * sinA
            self.detect_collision(dx, dy)
        if keys[pygame.K_s]:
            dx = -p_speed * cosA
            dy = -p_speed * sinA
            self.detect_collision(dx, dy)
        if keys[pygame.K_a]:
            dx = p_speed * sinA
            dy = -p_speed * cosA
            self.detect_collision(dx, dy)
        if keys[pygame.K_d]:
            dx = -p_speed * sinA
            dy = p_speed * cosA
            self.detect_collision(dx, dy)
        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.shot:
                    
                    self.shot = True
                    

    def mouse_control(self):
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - half_width
            pygame.mouse.set_pos((half_width, half_height))
            self.angle += difference * self.sensivity

        