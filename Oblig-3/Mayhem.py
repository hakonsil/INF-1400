import pygame
import numpy as np
from arena import *
from settings import *
from movable import *
from stationary import *
pygame.init() # initializing pygame
clock = pygame.time.Clock() # setting up clock

class Game:
    def __init__(self):
        self.player_group = pygame.sprite.Group()
        self.tile_group = pygame.sprite.Group()
        Red = player((1100, 500), (0, 0), RED_SHIP)
        Yellow = player((100, 500), (0, 0), YELLOW_SHIP)
        self.player_group.add(Red)
        self.player_group.add(Yellow)
        self.fuel_group = pygame.sprite.Group()
        fuel_bar_red = fuel_bar((100, 200), Red.fuel, red)
        fuel_bar_yellow = fuel_bar((300, 200), Yellow.fuel, green)
        self.fuel_group.add(fuel_bar_red)
        self.fuel_group.add(fuel_bar_yellow)

    def setup_arena(self):
        for i in range(len(Arena[0])):
            for j in range(len(Arena)):
                if Arena[j][i] == 1:
                    self.tile_group.add(tile((i*TILE_SIZE, j*TILE_SIZE), TILE))
        SCREEN.blit(BACKGROUND, (0, 0))
        self.tile_group.update()
        self.tile_group.draw(SCREEN)

    def setup_elements(self):
        self.player_group.update()
        self.player_group.draw(SCREEN)
        self.fuel_group.update()
        self.fuel_group.draw(SCREEN)

    def vertical_movement(self, players, tiles):
        for player in players:
            player.pos.y += player.speed.y
            player.rect = player.image.get_rect(center=(player.pos.x, player.pos.y))
            player.speed.y += g
            for tile in tiles:
                if player.rect.colliderect(tile.rect):
                    player.speed.y = 0
                    player.pos.y = tile.pos.y - player.rect.height/2
                    player.rect = player.image.get_rect(center=(player.pos.x, player.pos.y))
                    break

    def run(self):
        self.setup_arena()
        self.setup_elements()
        self.vertical_movement(self.player_group, self.tile_group)


"""--------------- Game loop -------------------"""
while True:
    clock.tick(FPS) # setting the framerate to 60 fps
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
    Game.run()
    pygame.display.update() #update the display

