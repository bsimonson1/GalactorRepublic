import pygame
from game import Game

def test_game_initialization():
    """
    This method is used to ensure that the game is being initalized correctly
    """
    #initialize pygame to allow access to pygame methods
    pygame.init()
    #set the screen to the minimum sized background image I am using
    screen = pygame.display.set_mode((800, 469))
    #create an object game of the class Game and pass in screen as aboive
    game = Game(screen)
    #check if the game is None, if not then we know that the game is running
    assert game is not None

def test_player_movement():
    pygame.init()
    #create a surface for testing the game and player movement
    screen = pygame.Surface((800, 600))  

    # make a game variable an object of the Game class and pass in the above screen surface
    game = Game(screen)
    game.spaceship_x = 100
    game.spaceship_y = 100

    # Simulate user input events to trigger player movement
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))
    # Update the game state
    game.update()  
    #since the movement will change by 5 units we can check whether or not the x value changes from the value i initally set it to
    assert game.spaceship_x == 105  # Verify that the player has moved to the right

    # Simulate another user input event for a different movement direction
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))
    # Update the game state
    game.update()  
    #since the movement will change by 5 units we can check whether or not the y value changes from the value i initally set it to
    assert game.spaceship_y == 95  

    pygame.quit()


if __name__ == "__main__":
    test_game_initialization()
    test_player_movement()
