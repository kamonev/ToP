import math

# settings
width = 1200
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
pr_coeff = 3 * distance * TILE
scale = width // num_rays

# texture settings (1200 * 1200)
texture_width = 1200
texture_height = 1200
texture_scale = texture_width // TILE
# player settings
p_pos = (width // 2, height // 2)
p_angle = 0
p_speed = 2

# minimap settings
map_scale = 5
map_tile = TILE // map_scale
map_pos = (0, height - height // map_scale)

# colors
black = (0, 0, 0)
white = (255, 255, 255)
purple = (176, 38, 255)
blue = (0, 180, 255)
gray = (50, 50, 50)
green = (0, 222, 0)
orange = (255, 165, 0)
red = (220, 0, 0)

sandy = (244,164,96)