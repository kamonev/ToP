import pygame
from settings import *
from collections import deque

# Initializing sprites from the folder with img files
class Sprites:
    def __init__(self):
        self.sprite_parametrs = {
            'barrel' : {
                'sprite' : pygame.image.load('sprites/objects/barrelGreenWater/0.png').convert_alpha(),
                'veiwing_angles' : None,
                'shift' : 1.7,
                'scale' : 0.4,
                'animation' : None, # deque(
                    #[pygame.image.load(f'sprites/objects/barrelGreenWater/{i}.png').convert_alpha() for i in range(12)]
                    #)
                'animation_dist':800,
                'animation_speed':10,
                'blocked' : True,
            },
            'amogus' : {
                'sprite' : pygame.image.load('sprites/enemy/amogus/0.png').convert_alpha(),
                'veiwing_angles' : None,
                'shift' : -0.02,
                'scale' : 1.3,
                'animation' : None, # deque(
                    #[pygame.image.load(f'sprites/objects/barrelGreenWater/{i}.png').convert_alpha() for i in range(12)]
                    #)
                'animation_dist':800,
                'animation_speed':10,
                'blocked' : True,
            }
        }
        #self.sprite_types = {
        #    'barrel': pygame.image.load('sprites/objects/barrelGreenWater/0.png').convert_alpha(),
        #    'skull': [pygame.image.load(f'sprites/enemy/skull/skullStay/{i}.png').convert_alpha() for i in range(8)],
        #}
        self.list_of_objects = [
            SpriteObject(self.sprite_parametrs['barrel'], (17.7, 3.5)),
            SpriteObject(self.sprite_parametrs['barrel'], (17.7, 6.5)),
            SpriteObject(self.sprite_parametrs['amogus'], (17.7, 11.5)),
            #SpriteObject(self.sprite_types['skull'], False, (15.1, 8.1), 0.4, 0.6),
        ]


class SpriteObject:
    #Initializing sprites Characteristics
    def __init__(self, parametrs, pos):
        self.object = parametrs['sprite']
        self.veiwing_angles = parametrs['veiwing_angles']
        self.shift = parametrs['shift']
        self.scale = parametrs['scale']
        self.animation = parametrs['animation']
        self.blocked = parametrs['blocked']
        self.side = 30
        self.animation_dist = parametrs['animation_dist']
        self.animation_speed = parametrs['animation_speed']
        self.animation_count = 0
        self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.pos = self.x - self.side //2, self.y - self.side // 2
        

        if self.veiwing_angles:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_pos = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}
    #Sprite placement
    def object_locate(self, player):
        dx, dy = self.x - player.x, self.y - player.y
        sprite_distance = math.sqrt(dx**2 + dy**2)

        theta = math.atan2(dy,dx)
        gamma = theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += double_pi

        delta_rays = int(gamma / delta_angle)
        cur_ray = center_ray + delta_rays
        sprite_distance *= math.cos(half_fov - cur_ray * delta_angle)


        fake_ray = cur_ray + fake_rays
        if 0 <= fake_ray <= fake_rays_range and sprite_distance > 30:
            proj_height = min(int(pr_coeff / sprite_distance * self.scale), double_height)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift


            #Displaying a dynamic sprite
            if self.veiwing_angles:
                if theta < 0:
                    theta += double_pi
                theta = 360 - int(math.degrees(theta))

                for angles in self.sprite_angles:
                    if theta in angles:
                        self.object = self.sprite_pos[angles]
                        break

            #sprite animation
            sprite_object = self.object
            if self.animation and distance_to_sprite < self.animation_dist:
                sprite_object = self.animation[0]
                if self.animation_count < self.animation_speed:
                    self.animation_count+=1
                else:
                    self.animation.rotate()
                    self.animation_count = 0

            #sprite scale and pos
            sprite_pos = (cur_ray * scale - half_proj_height, half_height - half_proj_height + shift)
            sprite = pygame.transform.scale(sprite_object, (proj_height, proj_height))
            return (sprite_distance, sprite, sprite_pos)
        else:
            return(False,)