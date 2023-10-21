import pygame
from settings import *
from ray_casting import rayCasting
from map import mini_map


class Drawing:
    def __init__(self, sc, sc_map):
        self.sc = sc  # The game screen
        self.sc_map = sc_map  #mini map
        self.font = pygame.font.SysFont('Arial', 36, bold=True)  # Initialize a font for displaying text

        # assign keys to the pictures
        self.textures = {'1': pygame.image.load('img/1.png').convert(), '2': pygame.image.load('img/2.png').convert()}

    # Render the background of the game
    def background(self):
        pygame.draw.rect(self.sc, blue, (0, 0, width, half_height))
        pygame.draw.rect(self.sc, gray, (0, half_height, width, half_height))

    # Render the game world using ray casting
    def world(self, player_pos, player_angle):
        rayCasting(self.sc, player_pos, player_angle, self.textures)

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
            pygame.draw.rect(self.sc_map, green, (x, y, map_tile, map_tile))
        self.sc.blit(self.sc_map, map_pos)