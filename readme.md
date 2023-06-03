 # Galactor
    #### Video Demo:  https://youtu.be/f91dQpoxJ7I
    #### Description: 

2D space shooter. The objective of the game is to avoid all of the incoming asteroids using the arrowkeys. Press space to start the game as instructed. Once the game is started space can be pressed again to pause the game although there is limited functionality with this. 

install pygame, random, and math (assuming these libraries are not already installed). Install the galactor folder and run the program by executing py project.py.

the spaceship images were created by me, there are three images with differing colors for the flames to make it seem as if the flame is moving and accelerating the ship forward. the background and asteroid images were obtained from a free open source image site meant to be used for games like this. 

game starts in the project.py file where the user is instructed to press space to start the game. Once the space bar is hit the run method is called and the infinite run loop is started for the game. It keeps track of the user input and adjusts the x and y coordinates of the spaceship accordingly. Asteroids are also generated in the update and render methods of game.py. Collision is detected using colliderect by making the spaceship and asteroid images rectanges and checking if their path intersect. If this happens the game is over and will stay in another infinite loop until the player presses space to restart the game. There is no score feature, no buttons and not way to efefctively pause and resume the game.

    TODO: Score tracking, boundaries for the game, pause functionality, fix the asteroid rects to be more representative of the asteroids, implement a button class so that the player can interact with the buttons