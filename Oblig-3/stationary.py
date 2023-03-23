import pygame
from settings import *

class stationary(pygame.sprite.Sprite):
    """All stationary objects"""
    pass

class fuel_bar(pygame.sprite.Sprite):
    def __init__(self, pos, fuel_amount, color):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.fuel_amount = fuel_amount
        self.color = color
        self.image = pygame.Surface((10, self.fuel_amount))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(midbottom=(self.pos.x, self.pos.y))

    def update(self, fuel_amount):
        self.image.fill(self.color)
        self.image = pygame.Surface((10, fuel_amount))
        self.rect = self.image.get_rect(midbottom=(self.pos.x, self.pos.y))
        self.image.fill(self.color)

class landing_pad(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.image = LANDING_PAD
        self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))

class obstacle(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.image = OBSTACLE
        self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))
        self.mask = pygame.mask.from_surface(self.image)

class score_card(pygame.sprite.Sprite):
    def __init__(self, pos, score1, score2):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.score1 = score1
        self.score2 = score2
        self.font = pygame.font.SysFont('Arial', 20)    
        self.image = self.font.render(f'Player 1 Score: {self.score1} | Player 2 Score: {self.score2} ', True, (0, 0, 0))
        self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))

    def update(self, score1, score2):
        self.score1 = score1
        self.score2 = score2
        self.image = self.font.render(f'Player 1 Score: {self.score1} | Player 2 Score: {self.score2} ', True, (0, 0, 0))
        self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))
        SCREEN.blit(self.image, self.rect)