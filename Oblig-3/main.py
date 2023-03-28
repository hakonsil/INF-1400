"""
Main game file
---
Author: Håkon Silseth (hsi039)

This file contains the main game loop, and the class for the game.
Here is where the game mechanics are defined and the game is initialized and run.
"""
import pygame
from config import *
from movable import *
from stationary import *
pygame.init() # initializing pygame
clock = pygame.time.Clock() # setting up clock
pygame.mixer.init() # initializing mixer (for sound)

class Game:
    """Game 
    ---
    Contains all the mechanics of the game.
    
    Methods:
        - __init__(): Initializes the game.
        - setup_arena(): Sets up the arena.
        - setup_elements(): Sets up the elements of the game.
        - draw_arena_elements(): Draws the stationary elements of the game.
        - draw_player_elements(): Draws the movable elements of the game.
        - input_player_1(): Takes input from player 1.
        - input_player_2(): Takes input from player 2.
        - player_collision(): Checks if the players collide with another object.
        - bullet_collision(): Checks if the bullets collide with another object.
        - edge_detection(): Checks if the players are out of bounds.
        - refueling(): Checks if the players are in contact with a landing pad, and if so, refuels them.
        - finish_game(): Checks if a player has won, and if so, shows the winner.
        - game_loop(): The main game loop.
        - run(): Runs the game.
        """
    def __init__(self):
        self.setup_elements()
        self.setup_arena()
        self.draw_arena_elements()

    def setup_arena(self):
        """
        Sets up the arena
        ---
        Sets up the landing pads and obstacles in the game
        """
        for i in range(len(landing_pad_pos)):
            self.landing_pad_group.add(Stationary(landing_pad_pos[i], LANDING_PAD)) # set up landing pads

        for i in range(len(obstacle_pos)):
            self.obstacle_group.add(Stationary(obstacle_pos[i], OBSTACLE)) # set up obstacles

    def setup_elements(self):
        """
        Initializes all the visible elements of the game.
        ---
        """

        self.landing_pad_group = pygame.sprite.Group() # initialize landing pad group
        self.obstacle_group = pygame.sprite.Group() # initialize obstacle group

        self.fuel_bar_group = pygame.sprite.Group() # initialize fuel bar group
        self.player_1_fuel_bar = Fuel_bar((X_SIZE-50, Y_SIZE-200), 100, red) # fuel bar for player 1
        self.player_2_fuel_bar = Fuel_bar((50, Y_SIZE-200), 100, red) # fuel bar for player 2
        self.fuel_bar_group.add(self.player_1_fuel_bar) # add fuel bar to group
        self.fuel_bar_group.add(self.player_2_fuel_bar) # add fuel bar to group

        self.player_group = pygame.sprite.Group() # initialize player group
        self.player_1 = Player(player_1_start_pos, player_1_init_vel, PLAYER_1) # initialize player 1
        self.player_2 = Player(player_2_start_pos, player_2_init_vel, PLAYER_2) # initialize player 2
        self.player_group.add(self.player_1) # add player 1 to group
        self.player_group.add(self.player_2) # add player 2 to group

        self.bullet_group_1 = pygame.sprite.Group() # initialize bullet group for player 1
        self.bullet_group_2 = pygame.sprite.Group() # initialize bullet group for player 2
        self.score_group = pygame.sprite.Group() # initialize a group for the score card
        self.score = Score_card(SCORE_CARD_POS, self.player_1.score, self.player_2.score) # instantiate the score card
        self.score_group.add(self.score) # add the score card to the group

    def draw_arena_elements(self):
        """
        Draws all the stationary objects that are visible in the game.
        ---
        """
        SCREEN.blit(BACKGROUND, (0, 0))
        self.landing_pad_group.draw(SCREEN)
        self.fuel_bar_group.draw(SCREEN)
        self.obstacle_group.draw(SCREEN)
        self.score_group.draw(SCREEN)

    def draw_player_elements(self):
        """
        Draws all the moving objects in the game.
        ---
        """
        self.player_group.update()
        self.player_group.draw(SCREEN)
        self.bullet_group_1.update()
        self.bullet_group_1.draw(SCREEN)
        self.bullet_group_2.update()
        self.bullet_group_2.draw(SCREEN)

    def input_player_1(self):
        """
        Checks for input from player 1 and performs the corresponding action.
        ---
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: # check if the left arrow key is pressed
            self.player_1.image, self.player_1.rect = self.player_1.rotate_left(PLAYER_1) # rotate the player left

        if keys[pygame.K_RIGHT]: # check if the right arrow key is pressed
            self.player_1.image, self.player_1.rect = self.player_1.rotate_right(PLAYER_1) # rotate the player right
        
        if keys[pygame.K_UP]: # check if the up arrow key is pressed
            self.player_1.image = pygame.transform.rotate(PLAYER_1_THRUST, self.player_1.angle) # change player image to thrust image
            self.player_1.thrust() # apply thrust to the player
            self.player_1_fuel_bar.update(self.player_1.fuel) # update the fuel bar

        if keys[pygame.K_RSHIFT] and len(self.bullet_group_1) < 1: # check if the right shift key is pressed and if the player has any active bullets
            self.play_music(PEW_SOUND_FILE)
            self.bullet_group_1.add(Bullet(self.player_1.rect.center, self.player_1.speed, self.player_1.angle, BULLET)) # shoot a bullet
        
        if keys[pygame.K_UP] == False: # check if the up arrow key is not pressed
            self.player_1.image = pygame.transform.rotate(PLAYER_1, self.player_1.angle) # keep the original player image
    
    def input_player_2(self):
        """
        Checks for input from player 2 and performs the corresponding action.
        ---
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: # check if the a key is pressed
            self.player_2.image, self.player_2.rect = self.player_2.rotate_left(PLAYER_2) # rotate the player left
        if keys[pygame.K_d]: # check if the d key is pressed
            self.player_2.image, self.player_2.rect = self.player_2.rotate_right(PLAYER_2) # rotate the player right
        if keys[pygame.K_w]: # check if the w key is pressed
            self.player_2.image = pygame.transform.rotate(PLAYER_2_THRUST, self.player_2.angle) # change player image to thrust image
            self.player_2.thrust() # apply thrust to the player
            self.player_2_fuel_bar.update(self.player_2.fuel) # update the fuel bar

        if keys[pygame.K_LSHIFT] and len(self.bullet_group_2) < 1: # check if the left shift key is pressed and if the player has any active bullets
            self.play_music(PEW_SOUND_FILE)
            self.bullet_group_2.add(Bullet(self.player_2.rect.center, self.player_2.speed, self.player_2.angle, BULLET)) # shoot a bullet

        if keys[pygame.K_w] == False: # check if the w key is not pressed
            self.player_2.image = pygame.transform.rotate(PLAYER_2, self.player_2.angle) # keep the original player image

    def player_collision(self):
        """
        Check if a player is colliding with the other player, a landing pad or an obstacle.
        ---
        """
        for player in self.player_group:
            if pygame.sprite.spritecollide(player, self.landing_pad_group, False, pygame.sprite.collide_mask): # check if the player is colliding with a landing pad
                if player.speed.y > 0: # check if the player is moving downwards
                    player.speed.y = 0 # stop the players vertical motion
                    player.speed.x = 0.99*player.speed.x # slow the players horizontal motion
                elif player.speed.y < 0: # check if the player is moving upwards
                    player.speed *= -1 # reverse the players vertical motion (bounce off the landing pad)
            if pygame.sprite.spritecollide(player, self.obstacle_group, False, pygame.sprite.collide_mask): # check if the player is colliding with an obstacle
                player.speed *= -1 # reverse the players motion (bounce off the obstacle)
                player.score -= CRASH_DEDUCTION # deduct points for crashing into an obstacle
                self.play_music(CRASH_SOUND_FILE) # play the crash sound
        if self.player_1.rect.colliderect(self.player_2.rect): # check if the players are colliding
            self.play_music(CRASH_SOUND_FILE) # play the crash sound
            self.player_1.speed *= -1 # reverse the players motion (bounce off each other)
            self.player_2.speed *= -1 # reverse the players motion (bounce off each other)
            self.player_1.score -= CRASH_DEDUCTION # deduct points for crashing into the other player
            self.player_2.score -= CRASH_DEDUCTION # deduct points for crashing into the other player

    def edge_detection(self):
        """
        Check if a player has gone off the edge of the screen.
        ---
        """
        # checks if a player if off the edge of the screen, and if so kill the player
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
        """
        Check if a player is in contact with a landing pad and refuels the player.
        ---
        """
        for player in self.player_group:
            if pygame.sprite.spritecollide(player, self.landing_pad_group, False, pygame.sprite.collide_mask): # check if the player is colliding with a landing pad
                    if player.fuel < 100: # check if the player has a full tank of fuel
                        player.fuel += REFUELING_RATE # refuel the player

    def bullet_collision(self):
        """
        Check if a bullet is off screen, or has collided with stationary object or a player.
        ---
        """
        # removing bullets if they go off screen
        for bullet in self.bullet_group_1:
            if bullet.pos.y < 0 or bullet.pos.y > Y_SIZE or bullet.pos.x < 0 or bullet.pos.x > X_SIZE:
                self.bullet_group_1.remove(bullet)
        for bullet in self.bullet_group_2:
            if bullet.pos.y < 0 or bullet.pos.y > Y_SIZE or bullet.pos.x < 0 or bullet.pos.x > X_SIZE:
                self.bullet_group_2.remove(bullet)

        # removing bullets if they collide with stationary objects
        for bullet in self.bullet_group_1:
            for pad in self.landing_pad_group:
                if bullet.rect.colliderect(pad.rect):
                    self.bullet_group_1.remove(bullet)
            for obstacle in self.obstacle_group:
                if bullet.rect.colliderect(obstacle.rect):
                    self.bullet_group_1.remove(bullet)

            # removing bullets if they collide with players, and reward/deduct points from the players
            if bullet.rect.colliderect(self.player_2.rect):
                self.bullet_group_1.remove(bullet)
                self.player_2.score -= SHOT_DEDUCTION
                self.player_1.score += SHOT_POINTS
                self.score.update(self.player_1.score, self.player_2.score)

        # removing bullets if they collide with stationary objects
        for bullet in self.bullet_group_2:
            for pad in self.landing_pad_group:
                if bullet.rect.colliderect(pad.rect):
                    self.bullet_group_2.remove(bullet)
            for obstacle in self.obstacle_group:
                if bullet.rect.colliderect(obstacle.rect):
                    self.bullet_group_2.remove(bullet)
            
            # removing bullets if they collide with players, and reward/deduct points from the players
            if bullet.rect.colliderect(self.player_1.rect):
                self.bullet_group_2.remove(bullet)
                self.player_1.score -= SHOT_DEDUCTION
                self.player_2.score += SHOT_POINTS
                self.score.update(self.player_1.score, self.player_2.score)

    def finish_game(self, img1, img2):
        """
        Checks if a player has enough points to win/lose the game and displays the appropriate image.
        ---
        """

        # checking if player 1 has won
        if self.player_1.score >= MAX_SCORE or self.player_2.score <= MIN_SCORE:
            SCREEN.blit(img1, (0, 0)) # displaying the win screen
            pygame.mixer.music.stop() # stopping the music
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.__init__() # restarting the game
        
        # checking if player 2 has won
        elif self.player_2.score >= MAX_SCORE or self.player_1.score <= MIN_SCORE:
            SCREEN.blit(img2, (0, 0)) # displaying the win screen
            pygame.mixer.music.stop() # stopping the music
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.__init__() # restarting the game

    def play_music(self, music, volume=1):
        """
        Plays the music.
        ---
        """
        pygame.mixer.music.load(music)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play()

    def game_loop(self):
        """
        The main game loop.
        ---
        Calls on all the other methods to run the game.
        """
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
        """
        Runs the game.
        ---
        """
        while True:
            clock.tick(FPS) # setting the framerate to 60 fps
            event = pygame.event.poll() # checking for events
            if event.type == pygame.QUIT: # checking if the user has quit the game
                break # break out of the loop
            self.game_loop() # run the game loop
            pygame.display.update() #update the display
        print("Thanks for playing!") # goodbye message

if __name__ == "__main__":
    """
    ## remove the commenting to run cProfile ##
    import cProfile
    cProfile.run('Game().run()') # profile the game
    """
    Game().run() # run the game