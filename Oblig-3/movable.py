import pygame
import numpy as np
from config import *

class Movable(pygame.sprite.Sprite):
    """Objects that can move"""
    def __init__(self, pos, speed, img):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.speed = pygame.Vector2(speed)
        self.image = img
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        """Moves the object"""
        self.pos += self.speed # updating position
        self.speed += pygame.Vector2(0, g) # updating speed
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y)) 

    def update(self):
        """Updates the object/object group"""
        self.move()

class Player(Movable):
    def __init__(self, pos, speed, img):
        super().__init__(pos, speed, img)
        self.angle = np.degrees(0)
        self.fuel = MAX_FUEL
        self.score = 0
        self.image = img

    def rotate_right(self, img):
        """Rotates the boid image to match the direction of the boid"""
        self.angle -= np.degrees(ROTATION_SPEED)
        rot_image = pygame.transform.rotate(img, self.angle) # rotating the image
        rot_rect = rot_image.get_rect(center=(self.pos.x, self.pos.y)) # rotating the rect
        return rot_image, rot_rect
    
    def rotate_left(self, img):
        """Rotates the boid image to match the direction of the boid"""
        self.angle += np.degrees(ROTATION_SPEED)
        rot_image = pygame.transform.rotate(img, self.angle) # rotating the image
        rot_rect = rot_image.get_rect(center=(self.pos.x, self.pos.y)) # rotating the rect
        return rot_image, rot_rect

    def thrust(self):
        """Applies thrust in the direction of the ship"""
        if self.fuel > 0:
            thrust = pygame.Vector2(0, THRUST_POWER)
            thrust.rotate_ip(-self.angle+180)
            self.speed += thrust
            self.fuel -= FUEL_CONSUMPTION

    def update(self):
        self.move()

class Bullet(Movable):
    def __init__(self, pos, speed, angle, img):
        super().__init__(pos, speed, img)
        self.angle = angle
        self.speed = pygame.Vector2(0, BULLET_SPEED)
        self.speed.rotate_ip(-self.angle+180)

    def update(self):
        self.move()
