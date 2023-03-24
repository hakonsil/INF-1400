import pygame
from config import *

class Fuel_bar(pygame.sprite.Sprite):
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
        self.image.fill(self.color)
        self.image = pygame.Surface((20, fuel_amount*3))
        self.rect = self.image.get_rect(midbottom=(self.pos.x, self.pos.y))
        self.image.fill(self.color)
        SCREEN.blit(FUEL_OUTLINE, (self.pos.x-10, self.pos.y-300))

class Landing_pad(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.image = LANDING_PAD
        self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))
        self.mask = pygame.mask.from_surface(self.image)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.image = OBSTACLE
        self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))
        self.mask = pygame.mask.from_surface(self.image)

class Score_card(pygame.sprite.Sprite):
    def __init__(self, pos, score1, score2):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.image = PANEL
        self.score1 = score1
        self.score2 = score2
        self.font = pygame.font.SysFont('twcen', 100)    
        self.rect = self.image.get_rect(midtop=(self.pos.x, self.pos.y))

    def update(self, score1, score2):
        self.score1 = score1
        self.score2 = score2
        self.image = PANEL
        self.rect = self.image.get_rect(midtop=(self.pos.x, self.pos.y))
        self.text1 = self.font.render(f"{self.score1}", True, black)
        self.text2 = self.font.render(f"{self.score2}", True, black)
        SCREEN.blit(self.image, self.rect)
        SCREEN.blit(self.text1, (self.pos.x-100, self.pos.y-5))
        SCREEN.blit(self.text2, (self.pos.x+50, self.pos.y-5))