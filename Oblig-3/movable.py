import pygame
import numpy as np
from settings import *

class movable(pygame.sprite.Sprite):
    """Objects that can move"""
    def __init__(self, pos, speed, img):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.speed = pygame.Vector2(speed)
        self.image = img
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))

    def move(self):
        """Moves the object"""
        self.pos += self.speed # updating position
        self.speed += pygame.Vector2(0, g) # updating speed
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y)) 

    def update(self):
        """Updates the object/object group"""
        self.move()

class player(movable):
    def __init__(self, pos, speed, img):
        super().__init__(pos, speed, img)
        self.angle = np.degrees(0)
        self.fuel = 100
        self.score = 0
        self.image = img

    def rotate_right(self, img):
        """Rotates the boid image to match the direction of the boid"""
        self.angle -= np.degrees(0.1)
        rot_image = pygame.transform.rotate(img, self.angle) # rotating the image
        rot_rect = rot_image.get_rect(center=(self.pos.x, self.pos.y)) # rotating the rect
        return rot_image, rot_rect
    
    def rotate_left(self, img):
        """Rotates the boid image to match the direction of the boid"""
        self.angle += np.degrees(0.1)
        rot_image = pygame.transform.rotate(img, self.angle) # rotating the image
        rot_rect = rot_image.get_rect(center=(self.pos.x, self.pos.y)) # rotating the rect
        return rot_image, rot_rect

    def thrust(self):
        """Applies thrust in the direction of the ship"""
        if self.fuel > 0:
            thrust = pygame.Vector2(0, 0.1)
            thrust.rotate_ip(-self.angle+180)
            self.speed += thrust
            self.fuel -= 0.1

    def update(self):
        self.move()
