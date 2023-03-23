import pygame
from arena import *

"""Setting up the screen and loading images"""
# defining SCREEN size
TILE_SIZE = 32
Arena = Arenas[0]
X_SIZE = TILE_SIZE*len(Arena[0])
Y_SIZE = TILE_SIZE*len(Arena)

# setting up screen
SCREEN = pygame.display.set_mode((X_SIZE, Y_SIZE), 0)
pygame.display.set_caption("Mayhem")

# importing files
BACKGROUND_FILE = r"Oblig-3\files\background.png"
PLAYER_1_FILE = r"Oblig-3\files\purple.png"
PLAYER_1_THRUST_FILE = r"Oblig-3\files\purple_thrust.png"
PLAYER_2_FILE = r"Oblig-3\files\yellow.png"
PLAYER_2_THRUST_FILE = r"Oblig-3\files\yellow_thrust.png"
LANDING_PAD_FILE = r"Oblig-3\files\landing_pad.png"
BULLET_FILE = r"Oblig-3\files\bullet.png"
P1_WIN_FILE = r"Oblig-3\files\p1_wins.png"
P2_WIN_FILE = r"Oblig-3\files\p2_wins.png"
OBSTACLE_FILE = r"Oblig-3\files\obstacle.png"

# loading images
BACKGROUND = pygame.image.load(BACKGROUND_FILE)
BACKGROUND = pygame.transform.scale(BACKGROUND, (X_SIZE, Y_SIZE))
PLAYER_1 = pygame.image.load(PLAYER_1_FILE)
PLAYER_1 = pygame.transform.scale(PLAYER_1, (60, 60))
PLAYER_1_THRUST = pygame.image.load(PLAYER_1_THRUST_FILE)
PLAYER_1_THRUST = pygame.transform.scale(PLAYER_1_THRUST, (60,60))
PLAYER_2 = pygame.image.load(PLAYER_2_FILE)
PLAYER_2 = pygame.transform.scale(PLAYER_2, (60, 60))
PLAYER_2_THRUST = pygame.image.load(PLAYER_2_THRUST_FILE)
PLAYER_2_THRUST = pygame.transform.scale(PLAYER_2_THRUST, (60, 60))
LANDING_PAD = pygame.image.load(LANDING_PAD_FILE)
LANDING_PAD = pygame.transform.scale(LANDING_PAD, (TILE_SIZE*6, TILE_SIZE*4))
BULLET = pygame.image.load(BULLET_FILE)
BULLET = pygame.transform.scale(BULLET, (15, 15))
P1_WIN = pygame.image.load(P1_WIN_FILE)
P1_WIN = pygame.transform.scale(P1_WIN, (X_SIZE, Y_SIZE))
P2_WIN = pygame.image.load(P2_WIN_FILE)
P2_WIN = pygame.transform.scale(P2_WIN, (X_SIZE, Y_SIZE))
OBSTACLE = pygame.image.load(OBSTACLE_FILE)
OBSTACLE = pygame.transform.scale(OBSTACLE, (TILE_SIZE, TILE_SIZE))

# variables
FPS = 60 # frames per second
g = 1/FPS # gravity
BULLET_SPEED = 10 # speed of bullets

# colors
red = (255, 0, 0)
green = (0, 255, 0)