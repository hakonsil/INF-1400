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
BACKGROUND = pygame.Surface((X_SIZE, Y_SIZE))
BACKGROUND.fill((255, 255, 255))
pygame.display.set_caption("Mayhem")

# importing files
RED_SHIP_FILE = r"Oblig-3\files\spaceship_red.png"
YELLOW_SHIP_FILE = r"Oblig-3\files\spaceship_yellow.png"
LANDING_PAD_FILE = r"Oblig-3\files\landing_pad.png"
BULLET_FILE = r"Oblig-3\files\bullet.png"
P1_WIN_FILE = r"Oblig-3\files\p1_wins.png"
P2_WIN_FILE = r"Oblig-3\files\p2_wins.png"
TILE_FILE = r"Oblig-3\files\tile.png"
OBSTACLE_FILE = r"Oblig-3\files\obstacle.png"

# loading images
RED_SHIP = pygame.image.load(RED_SHIP_FILE)
RED_SHIP = pygame.transform.scale(RED_SHIP, (35, 35))
YELLOW_SHIP = pygame.image.load(YELLOW_SHIP_FILE)
YELLOW_SHIP = pygame.transform.scale(YELLOW_SHIP, (35, 35))
LANDING_PAD = pygame.image.load(LANDING_PAD_FILE)
LANDING_PAD = pygame.transform.scale(LANDING_PAD, (TILE_SIZE, TILE_SIZE))
BULLET = pygame.image.load(BULLET_FILE)
BULLET = pygame.transform.scale(BULLET, (10, 10))
P1_WIN = pygame.image.load(P1_WIN_FILE)
P1_WIN = pygame.transform.scale(P1_WIN, (X_SIZE/2, Y_SIZE/2))
P2_WIN = pygame.image.load(P2_WIN_FILE)
P2_WIN = pygame.transform.scale(P2_WIN, (X_SIZE/2, Y_SIZE/2))
TILE = pygame.image.load(TILE_FILE)
TILE = pygame.transform.scale(TILE, (TILE_SIZE, TILE_SIZE))
OBSTACLE = pygame.image.load(OBSTACLE_FILE)
OBSTACLE = pygame.transform.scale(OBSTACLE, (TILE_SIZE, TILE_SIZE))

# variables
FPS = 60 # frames per second
g = 1/FPS # gravity
BULLET_SPEED = 10 # speed of bullets

# colors
red = (255, 0, 0)
green = (0, 255, 0)