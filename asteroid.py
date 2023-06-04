import pygame
import random

class Asteroids:
    def __init__(self, screen):
        self.screen = screen

        scale_factors = [0.22, 0.17, 0.115] 
        
        # Load the asteroid images
        self.asteroid_images = [
            pygame.image.load("large_asteroid.png").convert_alpha(),
            pygame.image.load("medium_asteroid.png").convert_alpha(),
            pygame.image.load("small_asteroid.png").convert_alpha()
        ]

        # Set color key on each asteroid image surface
        for image in self.asteroid_images:
            image.set_colorkey((0, 0, 0))

        # Scale the asteroid images
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
        # Render the asteroids in place
        for asteroid_rect, asteroid_image_index, _, _ in self.asteroid_rects:
            asteroid_image = self.asteroid_images[asteroid_image_index]
            self.screen.blit(asteroid_image, asteroid_rect, special_flags=pygame.BLEND_RGBA_ADD)
    
    def split(self, asteroid_rect):
        # Check which asteroid rect collides with the given asteroid_rect
        for i in range(len(self.asteroid_rects)):
            rect, image_index, _, _ = self.asteroid_rects[i]
            size = self.get_asteroid_size(image_index)
            if size == 'large':
                self.create_asteroids(rect.center, 'medium', 2)
            elif size == 'medium':
                self.create_asteroids(rect.center, 'small', 2)
            elif size == 'small':
                self.remove_asteroid(i)
            break

    def get_asteroid_size(self, image_index):
        if image_index == 0:
            return 'large'
        elif image_index == 1:
            return 'medium'
        elif image_index == 2:
            return 'small'

    def create_asteroids(self, position, size, count):
        # Create new asteroids at the given position and size
        for _ in range(count):
            if size == 'medium':
                image_index = 1
                speed = random.randint(5, 10)
            elif size == 'small':
                image_index = 2
                speed = random.randint(5, 15)

            asteroid_rect = self.asteroid_images[image_index].get_rect()
            asteroid_rect.center = position

            angle = random.uniform(-0.3, 0.3)
            direction = pygame.Vector2(1, angle).normalize()

            self.asteroid_rects.append((asteroid_rect, image_index, speed, direction))
            self.num_of_asteroids += 1

    def remove_asteroid(self, index):
        # Remove the asteroid at the given index from the asteroid_rects list
        self.asteroid_rects.pop(index)
        self.num_of_asteroids -= 1

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
            asteroid_speed = random.randint(5, 15)
        else:
            asteroid_speed = random.randint(5, 10)

        angle = random.uniform(-0.5, 0.5)
        asteroid_direction = pygame.Vector2(1, angle).normalize()

        self.asteroid_rects.append((asteroid_rect, asteroid_image_index, asteroid_speed, asteroid_direction))
        self.num_of_asteroids += 1