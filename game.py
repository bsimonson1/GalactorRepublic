import pygame
from asteroid import Asteroids
import time
from button import Button
#determine error for laser
from laser import Laser
#high score 384 Alan
class Game:
    def __init__(self, screen):
        self.start_time = time.time()
        self.player_speed = 10
        pygame.mixer.init()
        pygame.mixer.music.load('a-hero-of-the-80s-126684.mp3')
        #setting the volume manually add functionality for user to change it
        pygame.mixer.music.set_volume(0.2)  
        pygame.mixer.music.play(-1)

        #initialize the game objects and variables
        self.screen = screen
        #using my own font for the game score and other text
        font_path = r"C:\Users\bengs\OneDrive\Desktop\GalactorRepublic\rishgular-font\RishgularTry-x30DO.ttf"
        font_size = 36
        self.font = pygame.font.Font(font_path, font_size)
        
        scale_factor = 0.05

        #load the spaceship image
        self.spaceship_image = pygame.image.load("potential_character.png").convert_alpha()
        self.background_image = pygame.image.load("background_image.png").convert()
        #calculate the scaled dimensions
        scaled_width = int(self.spaceship_image.get_width() * scale_factor)
        scaled_height = int(self.spaceship_image.get_height() * scale_factor)

        #scale the image using pygame.transform.scale
        self.spaceship_image = pygame.transform.scale(self.spaceship_image, (scaled_width, scaled_height))
        #set the boundaries for the player to travel and handle in the update method
        self.min_x = 0
        self.max_x = screen.get_width() - self.spaceship_image.get_width()
        self.min_y = 0
        self.max_y = screen.get_height() - self.spaceship_image.get_height()

        #default positions and states for the player
        self.spaceship_x = 0
        self.spaceship_y = 500
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self._paused = False
        #initialize the asteroids object from the Asteroid class
        self.asteroids = Asteroids(self.screen)

        self.player_score = 0

        #call in labels to be used for buttons in this game
        self.play_img = pygame.image.load("play.png").convert_alpha()
        self.quit_img = pygame.image.load("quit.png").convert_alpha()
        self.paused_img = pygame.image.load("pause.png").convert_alpha()
        self.retry_img = pygame.image.load("retry.png").convert_alpha()
        self.resume_img = pygame.image.load("resume.png").convert_alpha()
        self.score_img = pygame.image.load("score.png").convert_alpha()
        self.high_score_img = pygame.image.load("high_score.png").convert_alpha()
        self.controls_img = pygame.image.load("controls.png").convert_alpha()

        #instantiate laser object
        self.laser = Laser(self.screen)
        #default values for the laser
        self.laser_x = 0
        self.laser_y = 0
        self.lasers = []
        #set the varaible equal to 0 for now to allow the player to shoot
        #this var will be used to moderate the players ability to shoot asteroids
        self.last_laser_shot = 0

        self.crashed = False

        self.toggle_mute = False

    def handle_events(self):
        #handle events such as user input
        #if the key ispressed this is entered
        #this achieves either a pressing effect for when the plauer presses a key or a holdinge ffect for when the player hodls a key
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.moving_down = True
                elif event.key == pygame.K_UP:
                    self.moving_up = True
                elif event.key == pygame.K_RIGHT:
                    self.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.moving_left = True
                elif event.key == pygame.K_ESCAPE:
                    self._paused = not self._paused
                    #if the key is not pressed then this is entered and resets the values
                elif event.key == pygame.K_m:
                    self.toggle_mute = not self.toggle_mute
                    if self.toggle_mute:
                        pygame.mixer.music.set_volume(0.0)
                    else:
                        pygame.mixer.music.set_volume(0.2)
                elif event.key == pygame.K_SPACE:
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_laser_shot >= 3000:  # 3000 milliseconds = 3 seconds
                        new_laser = Laser(self.screen)
                        new_laser.shoot(self.spaceship_x + self.spaceship_image.get_width(), self.spaceship_y + self.spaceship_image.get_height() // 2)
                        self.lasers.append(new_laser)
                        self.last_laser_shot = current_time
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.moving_down = False
                elif event.key == pygame.K_UP:
                    self.moving_up = False
                elif event.key == pygame.K_RIGHT:
                    self.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.moving_left = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def update(self):
        #update the game state
        if not self._paused:
            self.handle_events()

        if self.moving_down and self.spaceship_y < self.max_y:
            self.spaceship_y += self.player_speed
        if self.moving_up and self.spaceship_y > self.min_y:
            self.spaceship_y -= self.player_speed
        if self.moving_right and self.spaceship_x < self.max_x:
            self.spaceship_x += self.player_speed
        if self.moving_left and self.spaceship_x > self.min_x:
            self.spaceship_x -= self.player_speed

        self.current_time = time.time()
        self.elapsed_time = self.current_time - self.start_time
        if self.elapsed_time > 0.5:
            self.player_score += 1
            self.start_time = self.current_time

        spaceship_rect = self.spaceship_image.get_rect()
        spaceship_rect.x = self.spaceship_x
        spaceship_rect.y = self.spaceship_y

        #pass the lasers list to the update method of the Asteroids object
        self.asteroids.update(self.player_score, self.lasers)  

        for asteroid_rect, _, _, _ in self.asteroids.asteroid_rects:
            if spaceship_rect.colliderect(asteroid_rect):
                self.game_over()
                self.player_score = 0
                self.asteroid_interval = 2000
                self.player_speed = 10

        laser_rect = self.laser
        for laser in self.lasers:
            laser.update()
            self.laser.render()

        for laser_rect in self.lasers:
            for asteroid_rect, _, _, _ in self.asteroids.asteroid_rects:
                if laser_rect.colliderect(asteroid_rect):
                    self.handle_collision(laser_rect, asteroid_rect)

    def handle_collision(self, laser_rect, asteroid_rect):
        laser_index = self.lasers.index(laser_rect)
        asteroid_index = self.asteroids.get_asteroid_rect(asteroid_rect)
        if laser_rect.colliderect(asteroid_rect):
            del self.lasers[laser_index]
            del self.asteroids.asteroid_rects[asteroid_index]

    """
    the methods below are used in conjunction to handle if the player has lost the game
    Ie. the player has collided with an asteroid
    """
    def reset(self):
        #reset all necessary variables and states to their initial values
        self.player_speed = 10
        self.spaceship_x = 0
        self.spaceship_y = 220
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self._paused = False
        self.asteroids = Asteroids(self.screen)

    def game_over(self):
        self.crashed = True
        #game over logic 
        self.reset()  
        # Reset the game
        self.render()  
        # render the game objects on the screen
        pygame.display.update()  
        # update the display

        #wait for the player to press space or click the start button to start a new game
        while self.crashed:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.crashed = False
                        return  
                    #return to the main file to start a new game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                self.crashed = True
                self.render()
        
    def render(self):
        #draw the background image
        self.screen.blit(self.background_image, (0, 0))
        #render the game objects on the screen
        self.screen.blit(self.spaceship_image, (self.spaceship_x, self.spaceship_y))
        score_text = self.font.render(f'Score: {self.player_score}', True, (0, 100, 100))
        self.screen.blit(score_text, (800, 5))
        #render the aseroids and lasers
        self.asteroids.render() 
        self.laser.render()

        if self._paused:
            self.resume_button = Button(320, 295, self.resume_img, 0.2534, self.screen)
            self.quit_button = Button(335, 525, self.quit_img, 0.2548, self.screen)
            self.paused_button = Button(335, 75, self.paused_img, 0.25, self.screen)
            self.paused_button.draw()
            if self.resume_button.draw():
                self._paused = not self._paused
                return
            if self.quit_button.draw():
                pygame.quit()
                quit()

        if self.crashed:
            self.retry = Button(335, 215, self.retry_img, 0.25, self.screen)
            self.quit_button_crashed = Button(335, 415, self.quit_img, 0.255, self.screen)
            if self.retry.draw():
                self.crashed = False
                return
            if self.quit_button_crashed.draw():
                pygame.quit()
                quit()

    def paused(self):
        #pause functionality incorrect, need to maintain the state of the game and bring up a new screen with button
        #for whether or not the player wants tos tart a new game or quit
        while self._paused: 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._paused = not self._paused
                        return  # Resume the game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            #once unpaused the object must be redraw and the display must be updated to display them
            self.render()  
            pygame.display.update()  

    def run(self):
        pygame.display.set_caption("Play")
        # main game loop
        clock = pygame.time.Clock()  
        # create a clock object for controlling the frame rate

        asteroid_timer = 0
        self.asteroid_interval = 625
            
        while True:
            clock.tick(60)
            #need the x and y values for the laser to be used in this class
            self.laser_x = self.laser.laser_x() 
            self.laser_y = self.laser.laser_y()
            self.laser.render()
            #continuously update the state of the game with new objects and old objects new positions
            self.update()  

            current_time = pygame.time.get_ticks()
            if self.player_score >= 50: 
                self.asteroid_interval = 420
                self.player_speed = 15
            if current_time - asteroid_timer >= self.asteroid_interval:
                self.asteroids.generate_asteroid(self.player_score)
                asteroid_timer = current_time

            self.render()  

            for laser in self.lasers:
                laser.render()

            #render the game objects on the screen
            pygame.display.update()  
            #update the display

            if self._paused:
                self.paused()
