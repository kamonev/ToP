import pygame
from settings import *
from map import mini_map
from collections import deque


class Drawing:
    def __init__(self, sc, sc_map, player):
        self.sc = sc  # The game screen
        self.sc_map = sc_map  #mini map
        self.player = player
        self.font = pygame.font.SysFont('Arial', 36, bold=True)  # Initialize a font for displaying text

        # assign keys to the pictures
        self.textures = {1: pygame.image.load('img/fence.png').convert(),
                         2: pygame.image.load('img/fence.png').convert(),
                         's': pygame.image.load('img/4.png').convert()}

        # weapon parameters
        self.weapon_base_sprite = pygame.image.load('sprites/Gun/1.png').convert_alpha()
        self.weapon_shot_animation = deque([pygame.image.load(f'sprites/Gun/{i}.png').convert_alpha() for i in range(1,16)])
        self.weapon_rect = self.weapon_base_sprite.get_rect()
        self.weapon_pos = (half_width - self.weapon_rect.width // 2, height - self.weapon_rect.height)
        self.shot_length = len(self.weapon_shot_animation)
        self.shot_length_count = 0
        self.shot_animation_speed = 1
        self.shot_animation_count = 0
        self.shot_animation_trigger = True

    # Render the background of the game
    def background(self,angle):
        sky_offset = -5 * math.degrees(angle) % width
        self.sc.blit(self.textures['s'], (sky_offset, 0))
        self.sc.blit(self.textures['s'], (sky_offset - width, 0))
        self.sc.blit(self.textures['s'], (sky_offset + width, 0))

        pygame.draw.rect(self.sc, gray, (0, half_height, width, half_height))

    # Render the game world using ray casting
    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse = True):
            if obj[0]:
                _, object, object_pos = obj
                self.sc.blit(object, object_pos)

    # Display the frames per second on the screen
    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, orange)
        self.sc.blit(render, fps_pos)

    def mini_map(self, player):
        self.sc_map.fill(black)
        map_x, map_y = player.x // map_scale, player.y // map_scale
        pygame.draw.line(self.sc_map, purple, (map_x, map_y), (map_x + 12 * math.cos(player.angle),
                                                               map_y + 12 * math.sin(player.angle)), 2)
        pygame.draw.circle(self.sc_map, red, (int(map_x), int(map_y)), 5)
        for x, y in mini_map:
            pygame.draw.rect(self.sc_map, sandy, (x, y, map_tile, map_tile))
        self.sc.blit(self.sc_map, map_pos)

    def player_weapon(self):
        if self.player.shot:
            shot_sprite = self.weapon_shot_animation[0]
            self.sc.blit(shot_sprite, self.weapon_pos)
            self.shot_animation_count +=1
            if self.shot_animation_count == self.shot_animation_speed:
                self.weapon_shot_animation.rotate(-1)
                self.shot_animation_count = 0
                self.shot_length_count +=1
                self.shot_animation_trigger = False
            if self.shot_length_count == self.shot_length:
                self.player.shot = False
                self.shot_length_count = 0
                self.shot_animation_trigger = True
        else:
            self.sc.blit(self.weapon_base_sprite,self.weapon_pos)