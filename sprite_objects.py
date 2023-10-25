import pygame
from settings import *
from collections import deque
from numba.core import types
from numba.typed import Dict
from numba import int32


# Initializing sprites from the folder with img files
class Sprites:
    def __init__(self):
        self.sprite_parameters = {
            'barrel' : {
                'sprite' : pygame.image.load('sprites/objects/barrelGreenWater/0.png').convert_alpha(),
                'viewing_angles' : None,
                'shift' : 1.7,
                'scale' : (0.4, 0.4),
                'side' : 30,
                'animation' : deque(
                    [pygame.image.load(f'sprites/objects/barrelGreenWater/{i}.png').convert_alpha() for i in range(1)]
                    ),
                'death_animation' : deque(
                    [pygame.image.load(f'sprites/objects/barrelGreenWater/{i}.png').convert_alpha() for i in range(1)]
                    ),
                'is_dead' : None,
                'dead_shift' : 2.6,
                'animation_dist':800,
                'animation_speed':10,
                'blocked' : True,
                'flag' : 'object',
                'obj_action' : []
            },
            'skull' : {
                'sprite' : [pygame.image.load(f'sprites/enemy/skull/skullStay/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles' : True,
                'shift' : 0,
                'scale' : (0.4, 0.4),
                'side' : 30,
                'animation' : [],
                'death_animation' : deque([pygame.image.load(f'sprites/enemy/skull/skullStay/{i}.png').convert_alpha() for i in range(1)]),
                'is_dead' : None,
                'dead_shift' : 2.6,
                'animation_dist':800,
                'animation_speed':10,
                'blocked' : True,
                'flag' : 'object',
                'obj_action' : []
            },
            'amogus' : {
                'sprite' : pygame.image.load('sprites/enemy/amogus/0.png').convert_alpha(),
                'viewing_angles' : None,
                'shift' : -0.02,
                'scale' : (1.3,1.3),
                'side' : 30,
                'animation' : [],
                'death_animation' : deque([pygame.image.load(f'sprites/enemy/amogus/explosive_anim/{i}.png').convert_alpha() for i in range(5)]),
                'is_dead' : None,
                'dead_shift' : 0.6,
                'animation_dist':1000,
                'animation_speed':10,
                'blocked' : True,
                'flag' : 'npc_enemy',
                'obj_action' : deque([pygame.image.load(f'sprites/enemy/amogus/explosive_anim/{i}.png').convert_alpha() for i in range(1)])
            }
        }
        #self.sprite_types = {
        #    'barrel': pygame.image.load('sprites/objects/barrelGreenWater/0.png').convert_alpha(),
        #    'skull': [pygame.image.load(f'sprites/enemy/skull/skullStay/{i}.png').convert_alpha() for i in range(8)],
        #}
        self.list_of_objects = [
            SpriteObject(self.sprite_parameters['barrel'], (17.7, 3.5)),
            SpriteObject(self.sprite_parameters['barrel'], (17.7, 6.5)),
            SpriteObject(self.sprite_parameters['amogus'], (17.7, 11.5)),
            SpriteObject(self.sprite_parameters['amogus'], (17.7, 13.5)),
            SpriteObject(self.sprite_parameters['amogus'], (17.7, 21.5)),
            SpriteObject(self.sprite_parameters['amogus'], (11.7, 21.5)),
            SpriteObject(self.sprite_parameters['amogus'], (27.7, 13.5)),
            SpriteObject(self.sprite_parameters['amogus'], (22.7, 11.5)),
            SpriteObject(self.sprite_parameters['skull'],  (15.7, 11.5)),
        ]


class SpriteObject:
    #Initializing sprites Characteristics
    def __init__(self, parameters, pos):
        self.object = parameters['sprite'].copy()
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation'].copy()
        # ---------------------
        self.death_animation = parameters['death_animation'].copy()
        self.is_dead = parameters['is_dead']
        self.dead_shift = parameters['dead_shift']
        # ---------------------
        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.blocked = parameters['blocked']
        self.flag = parameters['flag']
        self.obj_action = parameters['obj_action'].copy()
        self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.side = parameters['side']
        self.dead_animation_count = 0
        self.animation_count = 0
        self.npc_action_trigger = False
        self.door_open_trigger = False
        self.door_prev_pos = self.y if self.flag == 'door_h' else self.x
        self.delete = False

        

        if self.viewing_angles:
            if len(self.object) == 8:
                self.sprite_angles = [frozenset(range(338, 361)) | frozenset(range(0, 23))] + \
                                     [frozenset(range(i, i + 45)) for i in range(23, 338, 45)]
            else:
                self.sprite_angles = [frozenset(range(348, 361)) | frozenset(range(0, 11))] + \
                                     [frozenset(range(i, i + 23)) for i in range(11, 348, 23)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}

    @property
    def is_on_fire(self):
        if center_ray - self.side // 2 < self.cur_ray < center_ray + self.side // 2 and self.blocked:
            return self.sprite_distance, self.proj_height
        return float('inf'), None

    @property
    def pos(self):
        return self.x - self.side // 2, self.y - self.side // 2

    #Sprite placement
    def object_locate(self, player):
        dx, dy = self.x - player.x, self.y - player.y
        self.sprite_distance = math.sqrt(dx**2 + dy**2)

        self.theta = math.atan2(dy,dx)
        gamma = self.theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += double_pi
        self.theta -= 1.4 * gamma

        delta_rays = int(gamma / delta_angle)
        self.cur_ray = center_ray + delta_rays
        self.sprite_distance *= math.cos(half_fov - self.cur_ray * delta_angle)


        fake_ray = self.cur_ray + fake_rays
        if 0 <= fake_ray <= fake_rays_range and self.sprite_distance > 30:
            self.proj_height = min(int(pr_coeff / self.sprite_distance), double_height)
            sprite_width = int(self.proj_height * self.scale[0])
            sprite_height = int(self.proj_height * self.scale[1])
            half_sprite_width = sprite_width // 2
            half_sprite_height = sprite_height // 2
            shift = half_sprite_height * self.shift


            #Displaying a dynamic sprite
            if self.is_dead and self.is_dead != 'immortal':
                sprite_object = self.dead_animation()
                #shift = half_sprite_height * self.dead_shift
                sprite_height = int(sprite_height / 1)
            elif self.npc_action_trigger:
                sprite_object = self.npc_in_action()
            else:
                self.object = self.visible_sprite()
                sprite_object = self.sprite_animation()

            #sprite animation
            #sprite_object = self.object
            #if self.animation and self.sprite_distance < self.animation_dist:
            #    sprite_object = self.animation[0]
            #    if self.animation_count < self.animation_speed:
            #        self.animation_count+=1
            #    else:
            #        self.animation.rotate()
            #        self.animation_count = 0

            #sprite scale and pos
            sprite_pos = (self.cur_ray * scale - half_sprite_width, half_height - half_sprite_height + shift)
            sprite = pygame.transform.scale(sprite_object, (sprite_width, sprite_height))
            return (self.sprite_distance, sprite, sprite_pos)
        else:
            return(False,)

    def sprite_animation(self):
        if self.animation and self.sprite_distance < self.animation_dist:
            sprite_object = self.animation[0]
            if self.animation_count < self.animation_speed:
                self.animation_count+=1
            else:
                self.animation.rotate()
                self.animation_count = 0
            return sprite_object
        return self.object

    def visible_sprite(self):
        if self.viewing_angles:
            if self.theta < 0:
                self.theta += double_pi
            self.theta = 360 - int(math.degrees(self.theta))

            for angles in self.sprite_angles:
                if self.theta in angles:
                    return self.sprite_positions[angles]
        return self.object

    def dead_animation(self):
        if len(self.death_animation):
            
            if self.dead_animation_count < self.animation_speed:
                self.dead_sprite = self.death_animation[0]
                self.dead_animation_count += 1
            else:
                self.dead_sprite = self.death_animation.popleft()
                self.dead_animation_count = 0
        return self.dead_sprite
    def npc_in_action(self):
        sprite_object = self.obj_action[0]
        if self.animation_count < self.animation_speed:
            self.animation_count += 1
        else:
            self.obj_action.rotate()
            self.animation_count = 0
        return sprite_object
