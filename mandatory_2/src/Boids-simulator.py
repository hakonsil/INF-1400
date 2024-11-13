import pygame
import random as rnd
import numpy as np
from variables import *
pygame.init() # initializing pygame
clock = pygame.time.Clock() # setting up clock

"""Setting up the screen and loading images"""
# defining SCREEN size
X_SIZE = 1250
Y_SIZE = 600

# setting up screen
SCREEN = pygame.display.set_mode((X_SIZE, Y_SIZE), 0)
BACKGROUND = pygame.Surface((X_SIZE, Y_SIZE))
BACKGROUND.fill((5, 15, 30))
pygame.display.set_caption("Boids")

# importing files
BOID_FILE = r"src\images\boid.png"
HOIK_FILE = r"src\images\hoik.png"
OBSTACLE_FILE = r"src\images\obstacle.png"
BAIT_FILE = r"src\images\bait.png"

# loading images
BOID = pygame.image.load(BOID_FILE)
BOID = pygame.transform.scale(BOID, (boid_x, boid_y))
HOIK = pygame.image.load(HOIK_FILE)
HOIK = pygame.transform.scale(HOIK, (hoik_x, hoik_y))
OBSTACLE = pygame.image.load(OBSTACLE_FILE)
OBSTACLE = pygame.transform.scale(OBSTACLE, (obstacle_x, obstacle_y))
BAIT = pygame.image.load(BAIT_FILE)
BAIT = pygame.transform.scale(BAIT, (bait_x, bait_y))

"""Defining classes"""
class Movable(pygame.sprite.Sprite):
    """Objects that can move"""
    def __init__(self, pos, speed, img):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.speed = pygame.Vector2(speed)
        self.image = img
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))

    def wrap(self):
        """Wraps elements around the screen,
        so that elements that leave the screen return on the other side"""
        if self.pos.x < b[0]:
            self.pos.x = X_SIZE
        if self.pos.y < 0:
            self.pos.y = Y_SIZE
        if self.pos.x > X_SIZE:
            self.pos.x = b[0]
        if self.pos.y > Y_SIZE:
            self.pos.y = 0

    def move(self):
        """Moves the object"""
        self.pos += self.speed # updating position
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y)) 
        self.wrap() # wrapping around the SCREEN
        
    def update(self):
        """Updates the object/object group"""
        self.move()

class Boid(Movable):
    """Boids, inherits from Movable"""
    def __init__(self, pos, speed):
        super().__init__(pos, speed, BOID)
    
    def separation(self):
        """calculates the separation vector, (basically says that if two boids are
        too close they will move apart)"""
        d = pygame.Vector2(0, 0)
        for neighbour in Boid_group:
            if neighbour != self:
                if (neighbour.pos - self.pos).length() < min_distance:
                    d = d - (neighbour.pos - self.pos)
        return d 

    def alignment(self):
        """calculates the alignment vector, (basically points all local boids in the same direction)"""
        n = 0
        v = pygame.Vector2(0, 0)
        for neighbour in Boid_group:
            if neighbour != self:
                distance = self.pos.distance_to(neighbour.pos)
                if distance < neighbourhood:
                    n += 1
                    v += neighbour.speed
        if n == 0:
            return pygame.Vector2(0, 0)
        else:
            return (v/n) / 10

    def cohesion(self):
        """points all local boids towards the center of mass"""
        n = 0
        v = pygame.Vector2(0, 0)
        for neighbour in Boid_group:
            if neighbour != self:
                distance = self.pos.distance_to(neighbour.pos)
                if distance < neighbourhood:
                    n += 1
                    v += neighbour.pos
        if n == 0:
            return pygame.Vector2(0, 0)
        else:
            return ((v/n) - self.pos) / 100

    def flee(self):
        """Makes the boids flee from the hoiks"""
        n=0
        v = pygame.Vector2(0, 0)
        for hoik in Hoik_group:
            distance = self.pos.distance_to(hoik.pos)
            if distance < neighbourhood:
                n += 1
                v += hoik.pos
        if n == 0:
            return pygame.Vector2(0, 0)
        else:
            return -((v/n) - self.pos) / 100

    def avoid(self):
        """Makes the boids avoid the obstacles"""
        n=0
        v = pygame.Vector2(0, 0)
        for obstacle in Obstacle_group:
            distance = self.pos.distance_to(obstacle.pos)
            if distance < neighbourhood:
                n += 1
                v += obstacle.pos
        if n == 0:
            return pygame.Vector2(0, 0)
        else:
            return -((v/n) - self.pos) / 100
        
    def eat(self):
        """Makes all boids move towards bait"""
        n=0
        v = pygame.Vector2(0, 0)
        for bait in Bait_group:
            n += 1
            v += bait.pos
        if n == 0:
            return pygame.Vector2(0, 0)
        else:
            return ((v/n) - self.pos) / 100

    def rotate(self):
        """Rotates the boid image to match the direction of the boid"""
        self.angle = np.degrees(np.arctan2(self.speed.x, self.speed.y)) + 180 # calculating the angle
        rot_image = pygame.transform.rotate(BOID, self.angle) # rotating the image
        rot_rect = rot_image.get_rect(center=(self.pos.x, self.pos.y)) # rotating the rect
        return rot_image, rot_rect

    def update(self):
        """sum up all velocity vectors and scale them to the boids speed,
        also rotates the image to match the direction of the boid and 'eats' the bait"""

        # adding up all the vectors and scale them to the boids speed
        self.speed += self.cohesion() * cohesion_weight
        self.speed += self.alignment() * alignment_weight
        self.speed += self.separation() * separation_weight
        self.speed += self.flee() * flee_weight
        self.speed += self.avoid() * avoid_weight
        self.speed += self.eat() * eat_weight
        if self.speed != pygame.Vector2(0, 0):
            self.speed.scale_to_length(boid_velocity)
        self.pos += self.speed

        # rotating the image
        self.rotate()
        self.image, self.rect = self.rotate()
        self.wrap()
        
        # eating the bait
        pygame.sprite.spritecollide(self, Bait_group, True)

class Hoik(Movable):
    """Hoiks that hunt the boids, inherits from Movable"""
    def __init__(self, pos, speed, x, y):
        super().__init__(pos, speed, HOIK)
        self.x = x
        self.y = y
    
    def hunt(self):
        """points the hoik towards the center of mass of local boids"""
        n = 0
        v = pygame.Vector2(0, 0)
        for boid in Boid_group:
            distance = self.pos.distance_to(boid.pos)
            if distance < hunting_radius:
                n += 1
                v += boid.pos
        if n == 0:
            return pygame.Vector2(0, 0)
        else:
            return ((v/n) - self.pos) / 100
    
    def separation(self):
        """makes sure the hoiks dont get to close to each other"""
        d = pygame.Vector2(0, 0)
        for neighbour in Hoik_group:
            if neighbour != self:
                if (neighbour.pos - self.pos).length() < min_distance:
                    d = d - (neighbour.pos - self.pos)
        return d*2

    def rotate(self):
        """Rotates the hoik image to match the direction of the hoik"""
        self.angle = np.degrees(np.arctan2(self.speed.x, self.speed.y)) + 180
        rot_image = pygame.transform.rotate(HOIK, self.angle)
        rot_rect = rot_image.get_rect(center=(self.pos.x, self.pos.y))
        return rot_image, rot_rect

    def update(self):
        """updates the velocity and position of the hoik"""
        # adding up the vectors for the behaviour
        self.speed += self.hunt()
        self.speed += self.separation()
        if self.speed != pygame.Vector2(0, 0):
            self.speed.scale_to_length(hoik_velocity)
        self.pos += self.speed

        self.wrap() # wrapping the hoik around the screen
        self.image, self.rect = self.rotate() # rotating the hoik
        
        # eating the boids
        pygame.sprite.spritecollide(self, Boid_group, True)

class Obstacle(pygame.sprite.Sprite):
    """Obstacles that the boids and hoiks avoid"""
    def __init__(self, pos):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.image = OBSTACLE
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))
    
    def update(self):
        """Kills the boids and hoiks that collide with the obstacle"""
        pygame.sprite.spritecollide(self, Boid_group, True)
        pygame.sprite.spritecollide(self, Hoik_group, True)

class Bait(pygame.sprite.Sprite):
    """Bait that the boids LOVE"""
    def __init__(self, pos):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.image = BAIT
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))

class Count_Button:
    """Note: This entire class is not my own code,
    please check the report for the reference to the original code and author"""
    def __init__(self, action, pos):
        self.pos = pos
        self.action = action

    def draw_button(self):
        global clicked
        action = False
        font = pygame.font.SysFont('Constantia', 30)

        #create pygame Rect object for the button
        button_rect = pygame.Rect(self.pos[0], self.pos[1], button_size[0], button_size[1])

        #check mouseover and clicked conditions
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(SCREEN, (64, 64, 64), button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pygame.draw.rect(SCREEN, (90, 90, 90), button_rect)
        else:
            pygame.draw.rect(SCREEN, (80, 80, 80), button_rect)

        #add text to button
        text_img = font.render(self.action, True, (0, 0, 0))
        text_len = text_img.get_width()
        SCREEN.blit(text_img, (self.pos[0] + 50 - int(text_len / 2), self.pos[1] + 12))
        return action

class Button:
    """Note: This entire class is not my own code,
    please check the report for the reference to the original code and author"""
    def __init__(self, text, value, pos):
        self.text = str(text)
        self.pos = pos
        self.value = value

    def draw_button(self):
        global clicked
        action = False
        font = pygame.font.SysFont('Constantia', 30)

        #create pygame Rect object for the button
        button_rect = pygame.Rect(self.pos[0], self.pos[1], b[0], b[1])

        #add text to button
        pygame.draw.rect(SCREEN, (128, 128, 128), button_rect)
        text_img = font.render(self.text + str(self.value), True, (0, 0, 0))
        SCREEN.blit(text_img, (self.pos[0] + 25, self.pos[1] + 12))
        return action

"""Setting up the elements"""
# setting up the boids
Boid_group = pygame.sprite.Group()
for _ in range(number_of_boids):
    Boid_group.add(Boid((rnd.randint(0, X_SIZE), rnd.randint(0, Y_SIZE)), (rnd.randint(-5, 5), rnd.randint(-5, 5))))

# setting up the hoiks, bait and obstacles
Hoik_group = pygame.sprite.Group()
Obstacle_group = pygame.sprite.Group()
Bait_group = pygame.sprite.Group()

while True:
    """Game loop"""
    clock.tick(60) # setting the framerate to 60 fps

    #defining the user input (keys to add elements)
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            Bait_group.add(Bait(pygame.mouse.get_pos()))
        if event.key == pygame.K_b:
            Boid_group.add(Boid(pygame.mouse.get_pos(), (rnd.randint(-5, 5), rnd.randint(-5, 5))))
        if event.key == pygame.K_h:
            Hoik_group.add(Hoik(pygame.mouse.get_pos(), (rnd.randint(-5, 5), rnd.randint(-5, 5)), hoik_x, hoik_y))
        elif event.key == pygame.K_o:
            Obstacle_group.add(Obstacle(pygame.mouse.get_pos()))
        elif event.key == pygame.K_e:
            Hoik_group.empty()
            Boid_group.empty()
            Obstacle_group.empty()
            Bait_group.empty()

    SCREEN.blit(BACKGROUND, (0,0)) # drawing the background

    # drawing and updating all sprites on the screen
    Boid_group.draw(SCREEN)
    Boid_group.update()
    Hoik_group.draw(SCREEN)
    Hoik_group.update()
    Obstacle_group.draw(SCREEN)
    Obstacle_group.update()
    Bait_group.draw(SCREEN)

    """drawing the buttons"""
    # cohesion
    cohesion_add = Count_Button("+", (button_size[0], 0+button_size[1]))
    cohesion_subtract = Count_Button("-", (0, 0 + button_size[1]))
    cohesion_button = Button("Cohesion: ", cohesion_weight, (0, 0))
    if cohesion_add.draw_button():
        cohesion_weight += 1
    if cohesion_subtract.draw_button():
        cohesion_weight -= 1
    cohesion_button.draw_button()

    # separation
    separation_add = Count_Button("+", (button_size[0], button_size[1]*3))
    separation_subtract = Count_Button("-", (0, 0 + button_size[1]*3))
    separation_button = Button("Separation: ", separation_weight, (0,button_size[1]*2 ))
    if separation_add.draw_button():
        separation_weight += 1
    if separation_subtract.draw_button():
        separation_weight -= 1
    separation_button.draw_button()

    # alignment
    alignment_add = Count_Button("+", (button_size[0], button_size[1]*5))
    alignment_subtract = Count_Button("-", (0, 0 + button_size[1]*5))
    alignment_button = Button("Alignment: ", alignment_weight, (0, button_size[1]*4))
    if alignment_add.draw_button():
        alignment_weight += 1
    if alignment_subtract.draw_button():
        alignment_weight -= 1
    alignment_button.draw_button()

    # number of boids
    number_of_boids = len(Boid_group)
    boid_button = Button("Boids: ", number_of_boids, (0, b[1]*6))
    boid_button.draw_button()

    # adding the 'instructions'
    button_1 = Button("Add boid: ", "'b'", (0, b[1]*7))
    button_1.draw_button()
    button_2 = Button("Add hoik: ", "'h'", (0, b[1]*8))
    button_2.draw_button()
    button_3 = Button("Add obst: ", "'o'", (0, b[1]*9))
    button_3.draw_button()
    button_4 = Button("Add bait: ", "'a'", (0, b[1]*10))
    button_4.draw_button()
    button_5 = Button("Empty:", "'e'", (0, b[1]*11))
    button_5.draw_button()

    # drawing some lines to make it look nice
    for i in range(8):
        pygame.draw.line(SCREEN, (0,0,0), (0, b[1]*i), (b[0], b[1]*i), 2)
    pygame.draw.line(SCREEN, (0,0,0), (button_size[0], button_size[1]*1), (button_size[0], button_size[1]*2) , 2)
    pygame.draw.line(SCREEN, (0,0,0), (button_size[0], button_size[1]*3), (button_size[0], button_size[1]*4) , 2)
    pygame.draw.line(SCREEN, (0,0,0), (button_size[0], button_size[1]*5), (button_size[0], button_size[1]*6) , 2)
    
    #update the display
    pygame.display.update() 
print("byebye!")