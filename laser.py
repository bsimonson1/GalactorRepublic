import pygame

class Laser:
    def __init__(self, screen):
        self.screen = screen

        scale_factor = 0.1

        original_laser_bullet = pygame.image.load("laser_bullet.png").convert_alpha()

        scaled_width = int(original_laser_bullet.get_width() * scale_factor)
        scaled_height = int(original_laser_bullet.get_height() * scale_factor)
        scaled_image = pygame.transform.scale(original_laser_bullet, (scaled_width, scaled_height))
        self.laser_bullet = scaled_image

        self.rect = self.laser_bullet.get_rect()

        self.laser_bullets = []

    def shoot(self, x, y):
        laser_rect = self.laser_bullet.get_rect()
        laser_rect.x = x + 10  # Offset the laser position from the player's position
        laser_rect.y = y + 10
        self.laser_bullets.append(laser_rect)

    def render(self):
        for laser_rect in self.laser_bullets:
            self.screen.blit(self.laser_bullet, (laser_rect.x, laser_rect.y))

    def update(self):
        for laser_rect in self.laser_bullets:
            laser_rect.x += 7

    def laser_x(self):
        return self.laser_bullets[0].x if self.laser_bullets else None

    def laser_y(self):
        return self.laser_bullets[0].y if self.laser_bullets else None

    def colliderect(self, other_rect):
        for laser_rect in self.laser_bullets:
            if laser_rect.colliderect(other_rect):
                return True
        return False
