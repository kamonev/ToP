from settings import *
from map import world_map
from ray_casting import mapping
import math
import pygame

def ray_casting_npc_player(npc_x, npc_y,  world_map, player_pos):
    ox, oy = player_pos[0], player_pos[1]
    xm, ym = mapping(ox, oy)
    delta_x, delta_y = ox - npc_x, oy - npc_y
    cur_angle = math.atan2(delta_y, delta_x)
    cur_angle += math.pi

    sin_a = math.sin(cur_angle)
    sin_a = sin_a if sin_a else 0.000001
    cos_a = math.cos(cur_angle)
    cos_a = cos_a if cos_a else 0.000001

    # verticals
    x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
    for i in range(0, int(abs(delta_x)) // TILE):
        depth_v = (x - ox) / cos_a
        yv = oy + depth_v * sin_a
        tile_v = mapping(x + dx, yv)
        
        x += dx * TILE

    # horizontals
    y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
    for i in range(0, int(abs(delta_y)) // TILE):
        depth_h = (y - oy) / sin_a
        xh = ox + depth_h * cos_a
        tile_h = mapping(xh, y + dy)
        
        y += dy * TILE
    return True


class Interaction:
    def __init__(self, player, sprites, drawing):
        self.player = player
        self.sprites = sprites
        self.drawing = drawing
        #self.pain_sound = pygame.mixer.Sound('sound/pain.wav')

    def interaction_objects(self):
        if self.player.shot:

            for obj in sorted(self.sprites.list_of_objects, key=lambda obj: obj.sprite_distance):
                #print("wdw")
                if obj.is_on_fire[1]:
                    #print(obj.is_on_fire[1])
                    print("BEBRA")
                    if obj.is_dead != 'immortal' and not obj.is_dead:

                        #print(ray_casting_npc_player(obj.x, obj.y, world_map, self.player.pos))
                        print(self.player.pos[0],self.player.pos[1])
                        if ray_casting_npc_player(obj.x, obj.y, world_map, self.player.pos):
                            obj.is_dead = True
                            obj.blocked = False
                            print(obj.blocked)
                            self.drawing.shot_animation_trigger = False
                    break

    def npc_action(self):
        for obj in self.sprites.list_of_objects:
            if obj.flag == 'npc_enemy' and not obj.is_dead:
                if ray_casting_npc_player(obj.x, obj.y,
                                          
                                          world_map, self.player.pos):
                    obj.npc_action_trigger = True
                    self.npc_move(obj)
                else:
                    obj.npc_action_trigger = False

    def npc_move(self, obj):
        if abs(obj.sprite_distance) > TILE:
            dx = obj.x - self.player.pos[0]
            dy = obj.y - self.player.pos[1]
            obj.x = obj.x + 1 if dx < 0 else obj.x - 1
            obj.y = obj.y + 1 if dy < 0 else obj.y - 1

    

    