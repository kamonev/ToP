import pygame
from settings import *
from map import world_map


def rayCasting(sc, p_pos, p_angle):
    cur_angle = p_angle - fov // 2
    x0, y0 = p_pos
    for ray in range(num_rays):
        sinA = math.sin(cur_angle)
        cosA = math.cos(cur_angle)
        for depth in range(max_depth):
            x = x0 + depth * cosA
            y = y0 + depth * sinA
            if (x // TILE * TILE, y // TILE * TILE) in world_map:
                depth *= math.cos(p_angle - cur_angle)
                pr_height = pr_coeff / depth
                depth_c = 255 / (1 + depth * depth * 0.00003)
                depth_color = (depth_c // 2, depth_c, depth_c // 2)
                pygame.draw.rect(sc, depth_color, (ray * scale, height // 2 - pr_height // 2, scale, pr_height))
                break
        cur_angle += delta_angle
