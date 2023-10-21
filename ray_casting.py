import pygame
from settings import *
from map import world_map


def mapping(a, b):
    return (a // TILE) * TILE, (b // TILE) * TILE


def rayCasting(sc, player_pos, player_angle, texture):
    cur_angle = player_angle - half_fov
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    for ray in range(num_rays):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)
        sin_a = sin_a if sin_a else 0.000001
        cos_a = cos_a if cos_a else 0.000001

        # verticals
        x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, width, TILE):
            depth_v = (x - ox) / cos_a
            yv = oy + depth_v * sin_a
            if mapping(x + dx, yv) in world_map:
                break
            x += dx * TILE

        # horizontals
        y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, height, TILE):
            depth_h = (y - oy) / sin_a
            xh = ox + depth_h * cos_a
            if mapping(xh, y + dy) in world_map:
                break
            y += dy * TILE

        # projection
        depth, offset = (depth_v,yv) if depth_v < depth_h else (depth_h,xh)
        offset = int(offset) % TILE
        depth *= math.cos(player_angle - cur_angle)
        # improved performance when approaching walls
        depth = max(depth,0.00001)
        proj_height = min(int(pr_coeff / depth),2 * height)

        # We select the surface for the texture in the form of a square
        wall_column = texture.subsurface(offset * texture_scale, 0, texture_scale, texture_height)
        wall_column = pygame.transform.scale(wall_column,(scale, proj_height))
        sc.blit(wall_column,(ray * scale, half_height - proj_height // 2))
        cur_angle += delta_angle