import pygame
from settings import *
from ray_casting import rayCasting


class Drawing:
    def __init__(self, sc):
        self.sc = sc  # The game screen
        self.font = pygame.font.SysFont('Arial', 36, bold=True)  # Initialize a font for displaying text

    # Render the background of the game
    def background(self):
        pygame.draw.rect(self.sc, blue, (0, 0, width, height // 2))
        pygame.draw.rect(self.sc, gray, (0, height // 2, width, height // 2))

    # Render the game world using ray casting
    def world(self, player_pos, player_angle):
        rayCasting(self.sc, player_pos, player_angle)

    # Display the frames per second on the screen
    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, orange)
        self.sc.blit(render, fps_pos)