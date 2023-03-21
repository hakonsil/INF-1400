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
        self.life = 3
        self.bullet_group = pygame.sprite.Group()

    def rotate_right(self):
        """Rotates the boid image to match the direction of the boid"""
        self.angle -= np.degrees(0.1)
        rot_image = pygame.transform.rotate(self.image, self.angle) # rotating the image
        rot_rect = rot_image.get_rect(center=(self.pos.x, self.pos.y)) # rotating the rect
        return rot_image, rot_rect
    
    def rotate_left(self):
        """Rotates the boid image to match the direction of the boid"""
        self.angle += np.degrees(0.1)
        rot_image = pygame.transform.rotate(self.image, self.angle) # rotating the image
        rot_rect = rot_image.get_rect(center=(self.pos.x, self.pos.y)) # rotating the rect
        return rot_image, rot_rect

    def thrust(self):
        """Applies thrust in the direction of the ship"""
        if self.fuel > 0:
            thrust = pygame.Vector2(0, 0.1)
            thrust.rotate_ip(-self.angle+180)
            self.speed += thrust
            self.fuel -= 1

    def shoot(self, bullet_group):
        """Shooting"""
        bullet = Bullet(self.pos , BULLET, self.angle)
        bullet_group.add(bullet)

    def user_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.image, self.rect = self.rotate_left()
        if keys[pygame.K_RIGHT]:
            self.image, self.rect = self.rotate_right()
        if keys[pygame.K_UP]:
            self.thrust()
        if keys[pygame.K_RSHIFT]:
            self.shoot(self.bullet_group)

    def update(self):
        self.user_input()
        self.move()
        
"""
    def damage(self, bullet_group, img):
        for bullet in bullet_group:
            if pygame.sprite.collide_rect(self, bullet):
                self.life -= 1
                bullet.kill()
                if self.life <= 0:
                    info_card_group.add(info_card((X_SIZE/2, Y_SIZE/2), img))

    def vertical_collision(self):
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))
        self.pos.y += self.speed.y
        self.speed.y += g
        for tile in tile_group:
            if pygame.sprite.collide_rect(self, tile):
                if self.speed.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.speed.y = 0
                if self.speed.y < 0:
                    self.rect.top = tile.rect.bottom
                    self.speed.y = 0
    
    def horizontal_collision(self):
        self.pos.x += self.speed.x
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))
        for tile in tile_group:
            if pygame.sprite.collide_rect(self, tile):
                if self.speed.x > 0:
                    self.rect.right = tile.rect.left
                    self.speed.x = 0
                if self.speed.x < 0:
                    self.rect.left = tile.rect.right
                    self.speed.x = 0
"""

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, img, angle):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.image = img
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))
        self.angle = angle
        self.speed = pygame.Vector2(0, BULLET_SPEED)
        self.speed.rotate_ip(-self.angle+180)

    def move(self):
        self.pos += self.speed
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))

    def update(self):
        self.move()