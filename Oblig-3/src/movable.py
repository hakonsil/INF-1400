"""
Movable objects
---
Author: Håkon Silseth (hsi039)

This file contains the classes for the moving objects in the game.
The defined classes are:
    - Movable: The base class for all moving objects.
    - Player: The playable character in the game.
    - Bullet: The bullets that the players can shoot.
"""
import pygame
import numpy as np
from config import *

class Movable(pygame.sprite.Sprite):
    """
    Moving objects
    ---

    Arguments:
        - pos (tuple): The initial position of the object.
        - speed (tuple): The initial speed of the object.
        - img (pygame.Surface): The image of the object.
    
    Attributes:
        - pos (pygame.Vector2): The position of the object.
        - speed (pygame.Vector2): The speed of the object.
        - image (pygame.Surface): The image of the object.
        - rect (pygame.Rect): The rect of the object.
        - mask (pygame.Mask): The mask of the object.

    Methods:
        - move(): Moves the object.
        - update(): Updates the object/object group.
    """
    def __init__(self, pos, speed, img):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.speed = pygame.Vector2(speed)
        self.image = img
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        """Updates the postion and speed of the object"""
        self.pos += self.speed # updating position
        self.speed += pygame.Vector2(0, g) # updating speed
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y)) # updating rect

    def update(self):
        """Updates the object
        --- 
        Calls on move()"""
        self.move()

class Player(Movable):
    """
    Player  (inherits from Movable)
    ---
    The playable character in the game.
    
    Arguments:
        - pos (tuple): The initial position of the object.
        - speed (tuple): The initial speed of the object.
        - img (pygame.Surface): The image of the object.

    Attributes:
        - pos (pygame.Vector2): The position of the object.
        - speed (pygame.Vector2): The speed of the object.
        - image (pygame.Surface): The image of the object.
        - rect (pygame.Rect): The rect of the object.
        - mask (pygame.Mask): The mask of the object.
        - angle (float): The angle of the object.
        - fuel (int): The fuel of the object.
        - score (int): The score of the object.

    Methods:
        - move(): Moves the object.
        - update(): Updates object (calls on move()).
        - rotate_right(img): Rotates the object to the right.
        - rotate_left(img): Rotates the object to the left.
        - thrust(): Accelerates the object in the direction it is facing.
    """
    def __init__(self, pos, speed, img):
        super().__init__(pos, speed, img)
        self.angle = np.degrees(0)
        self.fuel = MAX_FUEL # giving the player a full tank of fuel
        self.score = 0 # initializing score to 0
        self.image = img

    def rotate_right(self, img):
        """
        Rotates the object to the right
        ---
        Arguments:
            - img (pygame.Surface): The image of the object.

        Returns:
            - rot_image (pygame.Surface): The rotated image of the object.
            - rot_rect (pygame.Rect): The rotated rect of the object.
        """
        self.angle -= np.degrees(ROTATION_SPEED)
        rot_image = pygame.transform.rotate(img, self.angle) # rotating the image
        rot_rect = rot_image.get_rect(center=(self.pos.x, self.pos.y)) # rotating the rect
        return rot_image, rot_rect

    def rotate_left(self, img):
        """
        Rotates the object to the left
        ---
        Arguments:
            - img (pygame.Surface): The image of the object.

        Returns:
            - rot_image (pygame.Surface): The rotated image of the object.
            - rot_rect (pygame.Rect): The rotated rect of the object.
        """
        self.angle += np.degrees(ROTATION_SPEED)
        rot_image = pygame.transform.rotate(img, self.angle) # rotating the image
        rot_rect = rot_image.get_rect(center=(self.pos.x, self.pos.y)) # rotating the rect
        return rot_image, rot_rect

    def thrust(self):
        """
        Accelerates the object in the direction it is facing
        ---
        """
        if self.fuel > 0:
            thrust = pygame.Vector2(0, THRUST_POWER) # creating a vector with the thrust power
            thrust.rotate_ip(-self.angle+180) # rotating the vector to the direction the object is facing
            self.speed += thrust # accelerating the object
            self.fuel -= FUEL_CONSUMPTION # consuming fuel

class Bullet(Movable):
    """
    Bullet (inherits from Movable)
    ---

    Arguments:
        - pos (tuple): The initial position of the object.
        - speed (tuple): The initial speed of the object.
        - angle (float): The angle of the object.
        - img (pygame.Surface): The image of the object.

    Attributes:
        - pos (pygame.Vector2): The position of the object.
        - speed (pygame.Vector2): The speed of the object.
        - image (pygame.Surface): The image of the object.
        - rect (pygame.Rect): The rect of the object.
        - mask (pygame.Mask): The mask of the object.
        - angle (float): The angle of the object.

    Methods:
        - move(): Moves the object.
        - update(): Updates object (calls on move()).
    """
    def __init__(self, pos, speed, angle, img):
        super().__init__(pos, speed, img)
        self.angle = angle
        self.speed = pygame.Vector2(0, BULLET_SPEED)
        self.speed.rotate_ip(-self.angle+180)