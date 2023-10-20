import math

# settings
width = 1280
height = 720
half_height = height // 2
fps = 60
TILE = 50
fps_pos = width - 65, 5

# ray casting
fov = math.pi / 3
half_fov = fov // 2
num_rays = 300
max_depth = 800
delta_angle = fov / num_rays
distance = num_rays / (2 * math.tan(fov / 2))
pr_coeff = distance * TILE
scale = width // num_rays

# player settings
p_pos = (width // 2, height // 2)
p_angle = 0
p_speed = 2

# colors
black = (0, 0, 0)
white = (255, 255, 255)
purple = (176, 38, 255)
blue = (0, 180, 255)
gray = (50, 50, 50)
green = (0, 222, 0)
orange = (255, 165, 0)
