import pygame
from config import *
from movable import *
from stationary import *
pygame.init() # initializing pygame
clock = pygame.time.Clock() # setting up clock
"""---------------------------------------------"""

class Game:
    def __init__(self):
        self.setup_elements()
        self.setup_arena()
        self.draw_arena_elements()

    def setup_arena(self):
        # set up landing pads
        for i in range(len(landing_pad_pos)):
            self.landing_pad_group.add(Landing_pad(landing_pad_pos[i]))
        # set up obstacles
        for i in range(len(obstacle_pos)):
            self.obstacle_group.add(Obstacle(obstacle_pos[i]))

    def setup_elements(self):
        # stationary object groups
        self.landing_pad_group = pygame.sprite.Group()
        self.obstacle_group = pygame.sprite.Group()
        self.fuel_bar_group = pygame.sprite.Group()
        self.player_1_fuel_bar = Fuel_bar((X_SIZE-50, Y_SIZE-200), 100, red)
        self.player_2_fuel_bar = Fuel_bar((50, Y_SIZE-200), 100, red)
        self.fuel_bar_group.add(self.player_1_fuel_bar)
        self.fuel_bar_group.add(self.player_2_fuel_bar)

        # movable object groups
        self.player_group = pygame.sprite.Group()
        self.player_1 = Player(player_1_start_pos, player_1_init_vel, PLAYER_1)
        self.player_2 = Player(player_2_start_pos, player_2_init_vel, PLAYER_2)
        self.player_group.add(self.player_1)
        self.player_group.add(self.player_2)

        self.bullet_group_1 = pygame.sprite.Group()
        self.bullet_group_2 = pygame.sprite.Group()
        self.score_group = pygame.sprite.Group()
        self.score = Score_card(SCORE_CARD_POS, self.player_1.score, self.player_2.score)
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

    def player_collision(self):
        for player in self.player_group:
            if pygame.sprite.spritecollide(player, self.landing_pad_group, False, pygame.sprite.collide_mask):
                if player.speed.y > 0:
                    player.speed.y = 0
                    player.speed.x = 0.99*player.speed.x
                elif player.speed.y < 0:
                    player.speed *= -1
            if pygame.sprite.spritecollide(player, self.obstacle_group, False, pygame.sprite.collide_mask):
                player.speed *= -1
                player.score -= CRASH_DEDUCTION
        if self.player_1.rect.colliderect(self.player_2.rect):
            self.player_1.speed *= -1
            self.player_2.speed *= -1
            self.player_1.score -= CRASH_DEDUCTION
            self.player_2.score -= CRASH_DEDUCTION

    def edge_detection(self):
        for player in self.player_group:
            if player.pos.y < -50:
                player.score -= MIN_SCORE*2
            elif player.pos.y > Y_SIZE+50:
                player.score -= MIN_SCORE*2
            elif player.rect.left < -50:
                player.score -= MIN_SCORE*2
            elif player.rect.right > X_SIZE+50:
                player.score -= MIN_SCORE*2

    def refueling(self):
        for player in self.player_group:
            for landing_pad in self.landing_pad_group:
                if player.rect.colliderect(landing_pad.rect):
                    if player.fuel < 100:
                        player.fuel += REFUELING_RATE

    def bullet_collision(self):
        for bullet in self.bullet_group_1:
            if bullet.pos.y < 0 or bullet.pos.y > Y_SIZE or bullet.pos.x < 0 or bullet.pos.x > X_SIZE:
                self.bullet_group_1.remove(bullet)
        for bullet in self.bullet_group_2:
            if bullet.pos.y < 0 or bullet.pos.y > Y_SIZE or bullet.pos.x < 0 or bullet.pos.x > X_SIZE:
                self.bullet_group_2.remove(bullet)

        for bullet in self.bullet_group_1:
            for pad in self.landing_pad_group:
                if bullet.rect.colliderect(pad.rect):
                    self.bullet_group_1.remove(bullet)
            for obstacle in self.obstacle_group:
                if bullet.rect.colliderect(obstacle.rect):
                    self.bullet_group_1.remove(bullet)
            if bullet.rect.colliderect(self.player_2.rect):
                self.bullet_group_1.remove(bullet)
                self.player_2.score -= SHOT_DEDUCTION
                self.player_1.score += SHOT_POINTS
                self.score.update(self.player_1.score, self.player_2.score)

        for bullet in self.bullet_group_2:
            for pad in self.landing_pad_group:
                if bullet.rect.colliderect(pad.rect):
                    self.bullet_group_2.remove(bullet)
            for obstacle in self.obstacle_group:
                if bullet.rect.colliderect(obstacle.rect):
                    self.bullet_group_2.remove(bullet)
            if bullet.rect.colliderect(self.player_1.rect):
                self.bullet_group_2.remove(bullet)
                self.player_1.score -= SHOT_DEDUCTION
                self.player_2.score += SHOT_POINTS
                self.score.update(self.player_1.score, self.player_2.score)

    def finish_game(self, img1, img2):
        if self.player_1.score >= MAX_SCORE or self.player_2.score <= MIN_SCORE:
            SCREEN.blit(img1, (0, 0))
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.__init__()
        elif self.player_2.score >= MAX_SCORE or self.player_1.score <= MIN_SCORE:
            SCREEN.blit(img2, (0, 0))
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.__init__()

    def game_loop(self):
        self.draw_arena_elements() # drawing the stationary elements of the game

        self.player_collision() # checking if the players have collided with anything
        self.edge_detection() # checking if the players have gone off the screen
        self.bullet_collision() # checking if the bullets have collided with anything

        self.input_player_1() # checking for input from player 1 and performing the corresponding actions
        self.input_player_2() # checking for input from player 2 and performing the corresponding actions

        self.refueling() # refueling the players
        self.player_1_fuel_bar.update(self.player_1.fuel) # updating the player 1 fuel bar
        self.player_2_fuel_bar.update(self.player_2.fuel) # updating the player 2 fuel bar

        self.score.update(self.player_2.score, self.player_1.score) # updating the score

        self.draw_player_elements() # drawing the players
        self.finish_game(P1_WIN, P2_WIN) # checking if the game is over

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