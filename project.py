import pygame
from game import Game
from button import Button

def main():
    """
    The main method contains everyhting need to start and run the game it uses pygame and calls the run method from the 
    Game class in game.py to start the game upon correct user input
    """
    # pygame setup
    pygame.init()
    #set the background to the minimum sized background image
    screen = pygame.display.set_mode((1000, 800))
    #caption of the pygame window is main menu
    pygame.display.set_caption("Main Menu")
    #infinite loop for the game
    #while this is not necessary to run in this iteration of the game (since game.py has the loop) it will help
    #with future scalability when I come back to it in the future

    play_img = pygame.image.load("play.png").convert_alpha()
    quit_img = pygame.image.load("quit.png").convert_alpha()

    running = True
    while running:
        #default screen (black) instruction the user how to start the game
        screen.fill((0, 0, 0))  # Clear the screen with a black color
        #335, 215, self.retry_img, 0.25, self.screen
        play_button = Button(305, 115, play_img, 0.25, screen)
        quit_button = Button(335, 515, quit_img, 0.25, screen)

        if play_button.draw():
            game = Game(screen)  # Create an instance of the Game class
            game.run()  # Start the game when space is pressed
        if quit_button.draw():
            running = False

        #check if the valid key is pressed to start the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Display the main menu as well as instructions to start the game
        # draw_text("Main Menu", font, text_col, 265, 180)
        # draw_text("Press SPACE to start", font, text_col, 160, 225)

        
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
