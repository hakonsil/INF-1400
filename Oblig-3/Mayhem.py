import pygame
import numpy as np
from arena import *
from settings import *
from movable import *
from stationary import *
pygame.init() # initializing pygame
clock = pygame.time.Clock() # setting up clock
"""---------------------------------------------"""

class Game:
    def __init__(self):
        self.setup_elements()
        self.setup_arena()
        self.run()

    def setup_arena(self):
        for i in range(len(Arena[0])):
            for j in range(len(Arena)):
                if Arena[j][i] == 1:
                    self.tile_group.add(tile((i*TILE_SIZE, j*TILE_SIZE)))
                elif Arena[j][i] == 2:
                    self.landing_pad_group.add(landing_pad((i*TILE_SIZE, j*TILE_SIZE)))
                elif Arena[j][i] == 3:
                    self.obstacle_group.add(obstacle((i*TILE_SIZE, j*TILE_SIZE)))
        self.draw_arena_elements()

    def setup_elements(self):
        # stationary object groups
        self.tile_group = pygame.sprite.Group()
        self.landing_pad_group = pygame.sprite.Group()
        self.obstacle_group = pygame.sprite.Group()
        self.fuel_bar_group = pygame.sprite.Group()
        self.player_1_fuel_bar = fuel_bar((500, 200), 100, red)
        self.fuel_bar_group.add(self.player_1_fuel_bar)

        # movable object groups
        self.player_group = pygame.sprite.Group()
        self.player_1 = player((500, 200), (1, 0), RED_SHIP)
        self.player_group.add(self.player_1)

    def draw_arena_elements(self):
        SCREEN.blit(BACKGROUND, (0, 0))
        self.tile_group.draw(SCREEN)
        self.landing_pad_group.draw(SCREEN)
        self.fuel_bar_group.draw(SCREEN)
        self.obstacle_group.draw(SCREEN)

    def draw_player_elements(self):
        self.player_group.update()
        self.player_group.draw(SCREEN)

    def input_player_1(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_1.image, self.player_1.rect = self.player_1.rotate_left(RED_SHIP)
        if keys[pygame.K_RIGHT]:
            self.player_1.image, self.player_1.rect = self.player_1.rotate_right(RED_SHIP)
        if keys[pygame.K_UP]:
            self.player_1.thrust()
            self.player_1_fuel_bar.update(self.player_1.fuel)

    def vertical_collision_detection(self):
        for player in self.player_group:
            player.speed.y += g
            for tile in self.tile_group:
                if player.rect.colliderect(tile.rect) and player.speed.y > 0:
                    player.rect.bottom = tile.rect.top
                    player.speed.y = 0
                elif player.rect.colliderect(tile.rect) and player.speed.y < 0:
                    player.rect.top = tile.rect.bottom
                    player.speed.y = 0

    def horizontal_collision_detection(self):  
        for player in self.player_group:
            for tile in self.tile_group:
                if player.rect.colliderect(tile.rect) and player.speed.x > 0:
                    player.speed.x = 0
                    player.rect.right = tile.rect.left
                elif player.rect.colliderect(tile.rect) and player.speed.x < 0:
                    player.speed.x = 0
                    player.rect.left = tile.rect.right

    def game_loop(self):
        # drawing the on screen elements
        self.draw_arena_elements()
        self.draw_player_elements()

        # input from the players
        self.input_player_1()

        # collision detection
        self.vertical_collision_detection()
        self.horizontal_collision_detection()

        # refueling

        # updating the score

        # finish the game



    def run(self):
        while True:
            clock.tick(FPS) # setting the framerate to 60 fps
            event = pygame.event.poll() 
            if event.type == pygame.QUIT:
                break
            self.game_loop()
            pygame.display.update() #update the display
        print("Thanks for playing!")

if __name__ == "__main__":
    Game()