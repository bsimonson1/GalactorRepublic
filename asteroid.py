import pygame
import random

class Asteroids:
    def __init__(self, screen):
        self.screen = screen

        scale_factors = [0.22, 0.17, 0.115] 
        
        #load the asteroid images
        self.asteroid_images = [
            pygame.image.load("large_asteroid.png").convert_alpha(),
            pygame.image.load("medium_asteroid.png").convert_alpha(),
            pygame.image.load("small_asteroid.png").convert_alpha()
        ]

        #cet color key on each asteroid image surface
        for image in self.asteroid_images:
            image.set_colorkey((0, 0, 0))

        #ccale the asteroid images
        for i in range(len(self.asteroid_images)):
            original_image = self.asteroid_images[i]
            scale_factor = scale_factors[i]
            scaled_width = int(original_image.get_width() * scale_factor)
            scaled_height = int(original_image.get_height() * scale_factor)
            scaled_image = pygame.transform.scale(original_image, (scaled_width, scaled_height))
            self.asteroid_images[i] = scaled_image

        self.asteroid_rects = []
        self.num_of_asteroids = 0

    def update(self, player_score, lasers):
        # Update game state and position of asteroids
        if player_score >= 50:
            for asteroid_rect, asteroid_image_index, asteroid_speed, asteroid_direction in self.asteroid_rects:
                asteroid_rect.x -= asteroid_speed * asteroid_direction.x
                asteroid_rect.y -= asteroid_speed * asteroid_direction.y
        else:
            for asteroid_rect, asteroid_image_index, asteroid_speed, asteroid_direction in self.asteroid_rects:
                asteroid_rect.x -= asteroid_speed * asteroid_direction.x
                asteroid_rect.y -= asteroid_speed * asteroid_direction.y
    
    def render(self):
        #render the asteroids in place
        for asteroid_rect, asteroid_image_index, _, _ in self.asteroid_rects:
            asteroid_image = self.asteroid_images[asteroid_image_index]
            self.screen.blit(asteroid_image, asteroid_rect, special_flags=pygame.BLEND_RGBA_ADD)
    
    def split(self, asteroid_rect):
        #get the asteroid position to pass into the create_asteroid method
        asteroid_position = asteroid_rect.center

        large_ast = pygame.image.load("large_asteroid.png").convert_alpha()
        medium_ast = pygame.image.load("medium_asteroid.png").convert_alpha()
        small_ast = pygame.image.load("small_asteroid.png").convert_alpha()
        #0.22, 0.17, 0.115]
        large_scale_factor = 0.22
        medium_scale_factor = 0.17
        small_scale_factor = 0.115
        #reload images from before, needed to compare the passed in asteroid_rect with these to determine the size
        large_width = int(large_ast.get_width() * large_scale_factor)
        large_height = int(large_ast.get_height() * large_scale_factor)
        large_scaled = pygame.transform.scale(large_ast, (large_width, large_height))
        
        medium_width = int(medium_ast.get_width() * medium_scale_factor)
        medium_height = int(medium_ast.get_height() * medium_scale_factor)
        medium_scaled = pygame.transform.scale(medium_ast, (medium_width, medium_height))

        small_width = int(small_ast.get_width() * small_scale_factor)
        small_height = int(small_ast.get_height() * small_scale_factor)
        small_scaled = pygame.transform.scale(small_ast, (small_width, small_height))

        #check which asteroid rect collides with the given asteroid_rect
        if asteroid_rect.width == large_scaled.get_width() and asteroid_rect.height == large_scaled.get_height():
            #generate the 2 medium asteroids at this position
            self.create_asteroids(asteroid_position, 'medium', 2)
        elif asteroid_rect.width == medium_scaled.get_width() and asteroid_rect.height == medium_scaled.get_height():
            #generate 2 small asteroids
            self.create_asteroids(asteroid_position, 'small', 2)
        elif asteroid_rect.width == small_scaled.get_width() and asteroid_rect.height == small_scaled.get_height():
            return

    def create_asteroids(self, position, size, count):
        #create new asteroids at the given position and size
        for _ in range(count):
            #count and size passed in from the split method. 
            if size == 'medium':
                image_index = 1
                speed = random.randint(5, 10)
            elif size == 'small':
                image_index = 2
                speed = random.randint(5, 15)
        #create new asteroids from the position passed in by the splut method
            asteroid_rect = self.asteroid_images[image_index].get_rect()
            asteroid_rect.center = position

            angle = random.uniform(-0.6, 0.6)
            direction = pygame.Vector2(1, angle).normalize()

            self.asteroid_rects.append((asteroid_rect, image_index, speed, direction))
            self.num_of_asteroids += 1

    def get_asteroid_rect(self, asteroid_rect):
        for i in range(len(self.asteroid_rects)):
            if self.asteroid_rects[i][0] == asteroid_rect:
                return i
        return None

    def generate_asteroid(self, player_score):
        asteroid_image_index = random.randint(0, len(self.asteroid_images) - 1)
        asteroid_rect = self.asteroid_images[asteroid_image_index].get_rect()
        asteroid_rect.x = 1000
        asteroid_rect.y = random.randint(1, 800)
        if player_score >= 50:
            asteroid_speed = random.randint(8, 13)
        else:
            asteroid_speed = random.randint(5, 10)

        angle = random.uniform(-0.3, 0.3)
        asteroid_direction = pygame.Vector2(1, angle).normalize()

        self.asteroid_rects.append((asteroid_rect, asteroid_image_index, asteroid_speed, asteroid_direction))
        self.num_of_asteroids += 1