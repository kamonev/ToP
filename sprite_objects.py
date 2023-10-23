import pygame
from settings import *

# Initializing sprites from the folder with img files
class Sprites:
    def __init__(self):
        self.sprite_types = {
            'barrel': pygame.image.load('sprites/objects/barrelGreenWater/0.png').convert_alpha(),
            'skull': [pygame.image.load(f'sprites/enemy/skull/skullStay/{i}.png').convert_alpha() for i in range(8)],
        }
        self.list_of_objects = [
            SpriteObject(self.sprite_types['barrel'], True, (17.7, 3.5), 1.7,0.4),
            SpriteObject(self.sprite_types['barrel'], True, (17.7, 6.5), 1.8,0.4),
            SpriteObject(self.sprite_types['skull'], False, (15.1, 8.1), 0.4, 0.6),
        ]


class SpriteObject:
    #Initializing sprites Characteristics
    def __init__(self, object, static, pos, shift, scale):
        self.object = object
        self.static = static
        self.pos = self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.shift = shift
        self.scale = scale

        if not static:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_pos = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}
    #Sprite placement
    def object_locate(self, player, walls):
        dx, dy = self.x - player.x, self.y - player.y
        sprite_distance = math.sqrt(dx**2 + dy**2)

        theta = math.atan2(dy,dx)
        gamma = theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += double_pi

        delta_rays = int(gamma / delta_angle)
        cur_ray = center_ray + delta_rays
        sprite_distance *= math.cos(half_fov - cur_ray * delta_angle)

        if 0 <= cur_ray <= num_rays - 1 and sprite_distance < walls[cur_ray][0]:
            proj_height = int(pr_coeff / sprite_distance * self.scale)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift


            #Displaying a dynamic sprite
            if not self.static:
                if theta < 0:
                    theta += double_pi
                theta = 360 - int(math.degrees(theta))

                for angles in self.sprite_angles:
                    if theta in angles:
                        self.object = self.sprite_pos[angles]
                        break


            sprite_pos = (cur_ray * scale - half_proj_height, half_height - half_proj_height + shift)
            sprite = pygame.transform.scale(self.object, (proj_height, proj_height))
            return (sprite_distance, sprite, sprite_pos)
        else:
            return(False,)