import pygame
import numpy as np
import time
from arena import *
from settings import *
from movable import *
from stationary import *
pygame.init() # initializing pygame
clock = pygame.time.Clock() # setting up clock
t = time.time() # setting up time
"""---------------------------------------------"""

class Game:
    def __init__(self):
        self.setup_elements()
        self.setup_arena()

    def setup_arena(self):
        for i in range(len(Arena[0])):
            for j in range(len(Arena)):
                if Arena[j][i] == 1:
                    self.landing_pad_group.add(landing_pad((i*TILE_SIZE, j*TILE_SIZE)))
                elif Arena[j][i] == 3:
                    self.obstacle_group.add(obstacle((i*TILE_SIZE, j*TILE_SIZE)))
        self.draw_arena_elements()

    def setup_elements(self):
        # stationary object groups
        self.landing_pad_group = pygame.sprite.Group()
        self.obstacle_group = pygame.sprite.Group()
        self.fuel_bar_group = pygame.sprite.Group()
        self.player_1_fuel_bar = fuel_bar((500, 200), 100, red)
        self.player_2_fuel_bar = fuel_bar((100, 200), 100, green)
        self.fuel_bar_group.add(self.player_1_fuel_bar)
        self.fuel_bar_group.add(self.player_2_fuel_bar)

        # movable object groups
        self.player_group = pygame.sprite.Group()
        self.player_1 = player((X_SIZE-2*TILE_SIZE, Y_SIZE-2*TILE_SIZE), (0, 0), PLAYER_1)
        self.player_2 = player((2*TILE_SIZE, Y_SIZE-2*TILE_SIZE), (0, 0), PLAYER_2)
        self.player_group.add(self.player_1)
        self.player_group.add(self.player_2)

        self.bullet_group_1 = pygame.sprite.Group()
        self.bullet_group_2 = pygame.sprite.Group()
        self.score_group = pygame.sprite.Group()
        self.score = score_card((500, 200), self.player_1.score, self.player_2.score)
        self.score_group.add(self.score)

    def draw_arena_elements(self):
        SCREEN.blit(BACKGROUND, (0, 0))
        self.landing_pad_group.draw(SCREEN)
        self.fuel_bar_group.draw(SCREEN)
        self.obstacle_group.draw(SCREEN)
        self.score_group.draw(SCREEN)

    def draw_player_elements(self):
        self.player_group.update()
        self.player_group.draw(SCREEN)
        self.bullet_group_1.update()
        self.bullet_group_1.draw(SCREEN)
        self.bullet_group_2.update()
        self.bullet_group_2.draw(SCREEN)

    def input_player_1(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_1.image, self.player_1.rect = self.player_1.rotate_left(PLAYER_1)
        if keys[pygame.K_RIGHT]:
            self.player_1.image, self.player_1.rect = self.player_1.rotate_right(PLAYER_1)
        if keys[pygame.K_UP]:
            self.player_1.image = pygame.transform.rotate(PLAYER_1_THRUST, self.player_1.angle)
            self.player_1.thrust()
            self.player_1_fuel_bar.update(self.player_1.fuel)
        if keys[pygame.K_RSHIFT] and len(self.bullet_group_1) < 1:
            self.bullet_group_1.add(Bullet(self.player_1.rect.center, self.player_1.speed, self.player_1.angle, BULLET))
        if keys[pygame.K_UP] == False:
            self.player_1.image = pygame.transform.rotate(PLAYER_1, self.player_1.angle)
    
    def input_player_2(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player_2.image, self.player_2.rect = self.player_2.rotate_left(PLAYER_2)
        if keys[pygame.K_d]:
            self.player_2.image, self.player_2.rect = self.player_2.rotate_right(PLAYER_2)
        if keys[pygame.K_w]:
            self.player_2.image = pygame.transform.rotate(PLAYER_2_THRUST, self.player_2.angle)
            self.player_2.thrust()
            self.player_2_fuel_bar.update(self.player_2.fuel)
        if keys[pygame.K_LSHIFT] and len(self.bullet_group_2) < 1:
            self.bullet_group_2.add(Bullet(self.player_2.rect.center, self.player_2.speed, self.player_2.angle, BULLET))
        if keys[pygame.K_w] == False:
            self.player_2.image = pygame.transform.rotate(PLAYER_2, self.player_2.angle)

    def vertical_tile_collision(self):
        for player in self.player_group:
            for pad in self.landing_pad_group:
                if pygame.sprite.spritecollide(player, self.landing_pad_group, False, pygame.sprite.collide_mask):
                    if player.speed.y > 0:
                        player.rect.bottom = pad.rect.top
                        player.speed.y = 0
                    elif player.speed.y < 0:
                        player.speed *= -1

    def horizontal_tile_collision(self):  
        for player in self.player_group:
            for tile in self.landing_pad_group:
                if pygame.sprite.spritecollide(player, self.landing_pad_group, False, pygame.sprite.collide_mask):
                    if player.speed.x > 0:
                        player.rect.right = tile.rect.left
                        player.speed.x = 0
                    elif player.speed.x < 0:
                        player.rect.left = tile.rect.right
                        player.speed.x = 0

    def edge_detection(self):
        for player in self.player_group:
            if player.pos.y < 0:
                player.speed.reflect_ip((0, 1))
                player.speed *= -0.3
            elif player.pos.y > Y_SIZE:
                player.speed.reflect_ip((0, 1))
                player.speed *= -0.3
            elif player.rect.left < 0:
                player.speed.reflect_ip((1, 0))
                player.speed *= -0.3
            elif player.rect.right > X_SIZE:
                player.speed.reflect_ip((1, 0))
                player.speed *= -0.3
    
    def obstacle_collision(self):
        for player in self.player_group:
            if pygame.sprite.spritecollide(player, self.obstacle_group, False, pygame.sprite.collide_mask):
                player.speed *= -1
                player.score -= 1

    def refueling(self):
        for player in self.player_group:
            for landing_pad in self.landing_pad_group:
                if player.rect.colliderect(landing_pad.rect):
                    if player.fuel < 100:
                        player.fuel +=1

    def bullet_collision(self):
        for bullet in self.bullet_group_1:
            if bullet.pos.y < 0 or bullet.pos.y > Y_SIZE or bullet.pos.x < 0 or bullet.pos.x > X_SIZE:
                self.bullet_group_1.remove(bullet)
        for bullet in self.bullet_group_2:
            if bullet.pos.y < 0 or bullet.pos.y > Y_SIZE or bullet.pos.x < 0 or bullet.pos.x > X_SIZE:
                self.bullet_group_2.remove(bullet)

        for bullet in self.bullet_group_1:
            for obstacle in self.safe_objects_group:
                if bullet.rect.colliderect(obstacle.rect):
                    self.bullet_group_1.remove(bullet)
            for obstacle in self.obstacle_group:
                if bullet.rect.colliderect(obstacle.rect):
                    self.bullet_group_1.remove(bullet)
            if bullet.rect.colliderect(self.player_2.rect):
                self.bullet_group_1.remove(bullet)
                self.player_2.score -= 1
                self.player_1.score += 1
                self.score.update(self.player_1.score, self.player_2.score)

        for bullet in self.bullet_group_2:
            for obstacle in self.safe_objects_group:
                if bullet.rect.colliderect(obstacle.rect):
                    self.bullet_group_2.remove(bullet)
            for obstacle in self.obstacle_group:
                if bullet.rect.colliderect(obstacle.rect):
                    self.bullet_group_2.remove(bullet)
            if bullet.rect.colliderect(self.player_1.rect):
                self.bullet_group_2.remove(bullet)
                self.player_1.score -= 1
                self.player_2.score += 1
                self.score.update(self.player_1.score, self.player_2.score)

    def finish_game(self, img1, img2):
        if self.player_1.score >= 3 or self.player_2.score <= -3:
            SCREEN.blit(img1, (0, 0))
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.__init__()
        elif self.player_2.score >= 3 or self.player_1.score <= -3:
            SCREEN.blit(img2, (0, 0))
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.__init__()

    def game_loop(self):
        # drawing the on screen elements
        self.draw_arena_elements()
        self.draw_player_elements()

        # collision detection
        #self.horizontal_tile_collision()
        self.vertical_tile_collision()
        self.edge_detection()

        
        # input from the players
        self.input_player_1()
        self.input_player_2()

        # refueling
        self.refueling()
        self.player_1_fuel_bar.update(self.player_1.fuel)
        self.player_2_fuel_bar.update(self.player_2.fuel)
        self.obstacle_collision()

        # bullet collision
        self.bullet_collision()

        # updating the score
        self.score.update(self.player_1.score, self.player_2.score)

        # finish the game
        self.finish_game(P1_WIN, P2_WIN)

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
    Game().run()