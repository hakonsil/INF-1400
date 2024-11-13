"""
Stationary objects
---
Author: Håkon Silseth (hsi039)

This file contains the classes for the stationary objects in the game.
The defined classes are:
    - Stationary: A common class for all stationary objects that physically are a part of the game.
    - Fuel_bar: Displays the amount of fuel left for each player.
    - Score_card: Displays the score for each player.
"""
import pygame
from config import *

class Stationary(pygame.sprite.Sprite):
    """
    Stationary
    ---
    Displays the amount of fuel left for each player.

    Arguments:
        - pos (tuple): The position of the object.
        - img (pygame.Surface): The image of the object.

    Attributes:
        - pos (pygame.Vector2): The position of the object.
        - image (pygame.Surface): The image of the object.
        - rect (pygame.Rect): The rect of the object.
        - mask (pygame.Mask): The mask of the object.

    Methods:
        - __init__(pos, img): Initializes the object.
    """
    def __init__(self, pos, img):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.image = img
        self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))
        self.mask = pygame.mask.from_surface(self.image)

class Fuel_bar(pygame.sprite.Sprite):
    """
    Fuel bar
    ---
    Displays the amount of fuel left for each player.

    Arguments:
        - pos (tuple): The position of the object.
        - fuel_amount (int): The amount of fuel left.
        - color (tuple): The color of the fuel bar.

    Attributes:
        - pos (pygame.Vector2): The position of the object.
        - fuel_amount (float): The amount of fuel left.
        - color (tuple): The color of the fuel bar.
        - image (pygame.Surface): The image of the object.
        - rect (pygame.Rect): The rect of the object.

    Methods:
        - update(fuel_amount): Updates size of the fuel bar
    """

    def __init__(self, pos, fuel_amount, color):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.fuel_amount = fuel_amount
        self.color = color
        self.image = pygame.Surface((20, self.fuel_amount*3))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(midbottom=(self.pos.x, self.pos.y))
        SCREEN.blit(FUEL_OUTLINE, (self.pos.x-10, self.pos.y-300))

    def update(self, fuel_amount):
        """
        Updates the size of the fuel bar
        ---

        Arguments:
            - fuel_amount (int): The amount of fuel remaining.
        """

        self.image = pygame.Surface((20, fuel_amount*3)) # updating size of fuel bar
        self.rect = self.image.get_rect(midbottom=(self.pos.x, self.pos.y)) # updating rect
        self.image.fill(self.color) # coloring the fuel bar
        SCREEN.blit(FUEL_OUTLINE, (self.pos.x-10, self.pos.y-300)) # drawing the outline of the fuel bar

class Score_card(pygame.sprite.Sprite):
    """
    Score card
    ---
    Displays the current score

    Arguments:
        - pos (tuple): The position of the object.
        - score1 (int): The score of player 1.
        - score2 (int): The score of player 2.

    Attributes:
        - pos (pygame.Vector2): The position of the object.
        - score1 (int): The score of player 1.
        - score2 (int): The score of player 2.
        - image (pygame.Surface): The image of the object.
        - rect (pygame.Rect): The rect of the object.
        - font (pygame.font.SysFont): The font of the text.
        - text1 (pygame.Surface): The text of player 1's score.
        - text2 (pygame.Surface): The text of player 2's score.

    Methods:
        - update(score1, score2): Updates the score of the players.
    """
    def __init__(self, pos, score1, score2):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.image = PANEL
        self.score1 = score1
        self.score2 = score2   
        self.rect = self.image.get_rect(midtop=(self.pos.x, self.pos.y))

    def update(self, score1, score2):
        """Updates the score of the players"""
        self.score1 = score1
        self.score2 = score2
        self.image = PANEL
        self.rect = self.image.get_rect(midtop=(self.pos.x, self.pos.y))
        self.font = pygame.font.SysFont('twcen', 100) # font of the text
        self.text1 = self.font.render(f"{self.score1}", True, black)
        self.text2 = self.font.render(f"{self.score2}", True, black)
        SCREEN.blit(self.image, self.rect)
        SCREEN.blit(self.text1, (self.pos.x-100, self.pos.y-5))
        SCREEN.blit(self.text2, (self.pos.x+50, self.pos.y-5))