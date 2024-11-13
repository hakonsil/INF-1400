"""Simulation variables"""
# starting number of boids
number_of_boids = 20 

# sizes
boid_x, boid_y = 8, 16
hoik_x, hoik_y = 20, 30
obstacle_x, obstacle_y = 50, 50
bait_x, bait_y = 30, 30

# weights for boid behaviour
cohesion_weight = 1
alignment_weight = 1
separation_weight = 1
flee_weight = 1
avoid_weight = 1
eat_weight = 2

neighbourhood = 100
min_distance = 5
boid_velocity = 5

# weights for hoik behaviour
hunting_weight = 1
hoik_velocity = 5
hunting_radius = 150

# Button variables
clicked = False
counter = 0
button_size = (110, 50)
b = (220, 50)