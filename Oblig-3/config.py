"""
Configuration constants for the game.
---
Author: Håkon Silseth (hsi039)

This file contains all the constants, variables and files used in the game.
"""
import pygame

# defining screen size and framerate
X_SIZE = 1200 # screen width
Y_SIZE = 600 # screen height
FPS = 60 # framerate

SCREEN = pygame.display.set_mode((X_SIZE, Y_SIZE), 0)  # set up the screen
pygame.display.set_caption("Mayhem") # caption the game window

PLAYER_SIZE = (60, 60) # size of player
LANDING_PAD_SIZE = (200, 80) # size of landing pad
BULLET_SIZE = (15,15) # size of bullet
PANEL_SIZE = (300, 100) # size of score panel
FUEL_SIZE = (20, 300) # size of fuel bar
OBSTACLE_SIZE = (60, 60) # size of obstacles

# defining positions and initial values for in-game objects
landing_pad_pos =  [(0, Y_SIZE-0.75*LANDING_PAD_SIZE[1]),
                    (X_SIZE-LANDING_PAD_SIZE[0], Y_SIZE-0.75*LANDING_PAD_SIZE[1]),
                    (X_SIZE/2, Y_SIZE*(2/3))]

obstacle_pos = [(200, 200), (300, 500), (700, 120), (1000, 150)]

SCORE_CARD_POS = (X_SIZE/2, 0)

player_1_start_pos = (X_SIZE-LANDING_PAD_SIZE[0]/2, Y_SIZE-LANDING_PAD_SIZE[1])
player_2_start_pos = (LANDING_PAD_SIZE[0]/2, Y_SIZE-LANDING_PAD_SIZE[1])

player_1_init_vel = (0, 0)
player_2_init_vel = (0, 0)

# game variables
MAX_SCORE = 3 # max score to win
MIN_SCORE = -3 # min score to lose

CRASH_DEDUCTION = 1 # score deduction for crashing
SHOT_DEDUCTION = 1 # score deduction for getting shot
SHOT_POINTS = 1 # score points for shooting

REFUELING_RATE = 1 # rate of refueling
FUEL_CONSUMPTION = 0.3 # rate of fuel consumption
MAX_FUEL = 100 # max fuel

THRUST_POWER = 0.1 # acceleration from thrust
ROTATION_SPEED = 0.1 # speed at which player rotates
BULLET_SPEED = 20 # speed of bullets
g = 1/FPS # gravity

"""----------Loading images---------"""
BACKGROUND_FILE = r"Oblig-3\files\background.png"
BACKGROUND = pygame.image.load(BACKGROUND_FILE)
BACKGROUND = pygame.transform.scale(BACKGROUND, (X_SIZE, Y_SIZE))

PLAYER_1_FILE = r"Oblig-3\files\purple.png"
PLAYER_1_THRUST_FILE = r"Oblig-3\files\purple_thrust.png"
PLAYER_2_FILE = r"Oblig-3\files\yellow.png"
PLAYER_2_THRUST_FILE = r"Oblig-3\files\yellow_thrust.png"
PLAYER_1 = pygame.image.load(PLAYER_1_FILE)
PLAYER_1 = pygame.transform.scale(PLAYER_1, PLAYER_SIZE)
PLAYER_1_THRUST = pygame.image.load(PLAYER_1_THRUST_FILE)
PLAYER_1_THRUST = pygame.transform.scale(PLAYER_1_THRUST, PLAYER_SIZE)
PLAYER_2 = pygame.image.load(PLAYER_2_FILE)
PLAYER_2 = pygame.transform.scale(PLAYER_2, PLAYER_SIZE)
PLAYER_2_THRUST = pygame.image.load(PLAYER_2_THRUST_FILE)
PLAYER_2_THRUST = pygame.transform.scale(PLAYER_2_THRUST, PLAYER_SIZE)

LANDING_PAD_FILE = r"Oblig-3\files\landing_pad.png"
LANDING_PAD = pygame.image.load(LANDING_PAD_FILE)
LANDING_PAD = pygame.transform.scale(LANDING_PAD, LANDING_PAD_SIZE)

BULLET_FILE = r"Oblig-3\files\bullet.png"
BULLET = pygame.image.load(BULLET_FILE)
BULLET = pygame.transform.scale(BULLET, BULLET_SIZE)

P1_WIN_FILE = r"Oblig-3\files\p1_wins.png"
P2_WIN_FILE = r"Oblig-3\files\p2_wins.png"
P1_WIN = pygame.image.load(P1_WIN_FILE)
P1_WIN = pygame.transform.scale(P1_WIN, (X_SIZE, Y_SIZE))
P2_WIN = pygame.image.load(P2_WIN_FILE)
P2_WIN = pygame.transform.scale(P2_WIN, (X_SIZE, Y_SIZE))

OBSTACLE_FILE = r"Oblig-3\files\obstacle.png"
OBSTACLE = pygame.image.load(OBSTACLE_FILE)
OBSTACLE = pygame.transform.scale(OBSTACLE, OBSTACLE_SIZE)

PANEL_FILE = r"Oblig-3\files\panel.png"
PANEL = pygame.image.load(PANEL_FILE)
PANEL = pygame.transform.scale(PANEL, PANEL_SIZE)

FUEL_OUTLINE_FILE = r"Oblig-3\files\fuel_outline.png"
FUEL_OUTLINE = pygame.image.load(FUEL_OUTLINE_FILE)
FUEL_OUTLINE = pygame.transform.scale(FUEL_OUTLINE, FUEL_SIZE)

PEW_SOUND_FILE = r"Oblig-3\files\pew.mp3"
CRASH_SOUND_FILE = r"Oblig-3\files\boink.mp3"

# colors
red = (255, 0, 0)
black = (0, 0, 0)