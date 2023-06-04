import pygame

class Button():
    def __init__(self, x, y, image, scale, screen):
        pygame.init()
        self.screen = screen
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.clicked = False
    def draw(self):
        action = False
        #get mouse position
        position = pygame.mouse.get_pos()

        #check to see if the mouse position is over the button and if the mouse has been clicked
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: #0 is left click
                self.clicked = True
                action = True
                
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw the button on the screen
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

    #create button isntances in the respective classes using button