import pygame

class Laser:
    def __init__(self, screen):
        self.screen = screen
        #scaling factor for the lasers
        scale_factor = 0.1

        original_laser_bullet = pygame.image.load("laser_bullet.png").convert_alpha()
        #scale the lasers
        scaled_width = int(original_laser_bullet.get_width() * scale_factor)
        scaled_height = int(original_laser_bullet.get_height() * scale_factor)
        scaled_image = pygame.transform.scale(original_laser_bullet, (scaled_width, scaled_height))
        self.laser_bullet = scaled_image
        #get the rect of the lasers to use in this class
        self.rect = self.laser_bullet.get_rect()

        self.laser_bullets = []

    def shoot(self, x, y):
        laser_rect = self.laser_bullet.get_rect()
        #offset from the players position so it appears that the lasers stem from the edge of the players characters
        laser_rect.x = x + 5
        laser_rect.y = y 
        self.laser_bullets.append(laser_rect)

    def render(self):
        #render the list of lasers (dependent on how many are on screen and when the player presses spae)
        for laser_rect in self.laser_bullets:
            self.screen.blit(self.laser_bullet, (laser_rect.x, laser_rect.y))
            pygame.display.update()

    def update(self):
        for laser_rect in self.laser_bullets:
            laser_rect.x += 7
            pygame.display.update()
        self.laser_bullets = [laser_rect for laser_rect in self.laser_bullets if laser_rect.x < self.screen.get_width()]
        pygame.display.update()
    #getter methods for the laser x and y positions (y will never be updated but will be needed to calc position)
    def laser_x(self):
        return self.laser_bullets[0].x if self.laser_bullets else None

    def laser_y(self):
        return self.laser_bullets[0].y if self.laser_bullets else None

    def colliderect(self, other_rect):
        for laser_rect in self.laser_bullets:
            if laser_rect.colliderect(other_rect):
                return True
        return False
