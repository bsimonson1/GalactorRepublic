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
        pygame.mixer.music.set_volume(0.2)  # 80% volume
        pygame.mixer.music.play()
        self.song_end = False
        self.SONG_END = pygame.USEREVENT
        pygame.mixer.music.set_endevent(self.SONG_END)

        # Initialize the game objects and variables
        self.screen = screen

        font_path = r"C:\Users\bengs\OneDrive\Desktop\GalactorRepublic\rishgular-font\RishgularTry-x30DO.ttf"
        font_size = 36
        self.font = pygame.font.Font(font_path, font_size)
        
        scale_factor = 0.05

        # Load the spaceship image
        self.spaceship_image = pygame.image.load("potential_character.png").convert_alpha()
        self.background_image = pygame.image.load("background_image.png").convert()
        # Calculate the scaled dimensions
        scaled_width = int(self.spaceship_image.get_width() * scale_factor)
        scaled_height = int(self.spaceship_image.get_height() * scale_factor)

        # Scale the image using pygame.transform.scale
        self.spaceship_image = pygame.transform.scale(self.spaceship_image, (scaled_width, scaled_height))

        self.min_x = 0
        self.max_x = screen.get_width() - self.spaceship_image.get_width()
        self.min_y = 0
        self.max_y = screen.get_height() - self.spaceship_image.get_height()

        #default positions and states for the player
        self.spaceship_x = 0
        self.spaceship_y = 220
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

        self.crashed = False

    def handle_events(self):
        # Handle events such as user input
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
                elif event.key == pygame.K_SPACE:
                    new_laser = Laser(self.screen)
                    new_laser.shoot(self.spaceship_x + self.spaceship_image.get_width(), self.spaceship_y + self.spaceship_image.get_height() // 2)
                    self.lasers.append(new_laser)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.moving_down = False
                elif event.key == pygame.K_UP:
                    self.moving_up = False
                elif event.key == pygame.K_RIGHT:
                    self.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.moving_left = False
            elif event.type == self.SONG_END:
                    self.song_end = True
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def draw_lasers(self):
        for laser in self.lasers:
            laser.render()

    def update(self):
        # Update the game state
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

        self.asteroids.update(self.player_score, self.lasers)  # Pass the lasers list to the update method of the Asteroids object

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

        self.draw_lasers()  # Add this line to draw the laser bullets on the screen

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
        # Reset all necessary variables and states to their initial values
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
        # Game over logic 
        self.reset()  
        # Reset the game
        self.render()  
        # Render the game objects on the screen
        pygame.display.update()  
        # Update the display

        # Wait for the player to press space to start a new game
        while self.crashed:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.crashed = False
                        return  
                    # Return to the main file to start a new game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                self.crashed = True
                self.render()
        
    def render(self):
        # Draw the background image
        self.screen.blit(self.background_image, (0, 0))
        # Render the game objects on the screen
        self.screen.blit(self.spaceship_image, (self.spaceship_x, self.spaceship_y))
        score_text = self.font.render(f'Score: {self.player_score}', True, (0, 100, 100))
        self.screen.blit(score_text, (800, 5))

        self.asteroids.render()  
        # Add this line to render the asteroids

        self.laser.render()
        #this will render the bullet

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

            self.render()  # Redraw the game objects
            pygame.display.update()  # Update the display

    def run(self):
        pygame.display.set_caption("Play")
        # Main game loop
        clock = pygame.time.Clock()  
        # Create a clock object for controlling the frame rate

        asteroid_timer = 0
        self.asteroid_interval = 750
            
        while True:
            clock.tick(60)

            self.laser_x = self.laser.laser_x() #need the x and y values for the laser to be used in this class
            self.laser_y = self.laser.laser_y()

            self.update()  
            # Update the game state

            current_time = pygame.time.get_ticks()
            if self.player_score >= 50: 
                self.asteroid_interval = 420
                self.player_speed = 15
            if current_time - asteroid_timer >= self.asteroid_interval:
                self.asteroids.generate_asteroid(self.player_score)
                asteroid_timer = current_time

            self.render()  

            if self.song_end:
                pygame.mixer.music.load('a-hero-of-the-80s-126684.mp3')
                pygame.mixer.music.play()
                self.song_end = False

            # Render the game objects on the screen
            pygame.display.update()  
            # Update the display

            if self._paused:
                self.paused()

                #need to make game logic for when the player presses space
