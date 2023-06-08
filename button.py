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
    
    def draw_menu(self):
        black = (0, 0, 0)
        self.screen.fill(black)
        while True: 
            pygame.display.set_caption('Instruction Menu')
            font_path = r"C:\Users\bengs\OneDrive\Desktop\GalactorRepublic\rishgular-font\RishgularTry-x30DO.ttf"
            font_size = 36
            font = pygame.font.Font(font_path, font_size)
            instruction_text1 = font.render("Press Escape to return back to the Main Menu", True, (0, 100, 100))
            self.screen.blit(instruction_text1, (20, 20))
            instruction_text2 = font.render("Dodge the asteroids and stay alive for as long as possible", True, (0, 100, 100))
            self.screen.blit(instruction_text2, (20, 50))
            instruction_text3 = font.render("Use the arrow keys to move spacebar to shoot", True, (0, 100, 100))
            self.screen.blit(instruction_text3, (20, 80))
            instruction_text3 = font.render("ESC to pause and M to mute and unmute the music", True, (0, 100, 100))
            self.screen.blit(instruction_text3, (20, 110))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
            pygame.display.update()
