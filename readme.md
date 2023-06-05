 # GalactorRepublic
    #### Description: 

2D space shooter. The objective of the game is to avoid all of the incoming asteroids using the arrowkeys. Press space to start the game as instructed. Once the game is started space can be pressed again to pause the game although there is limited functionality with this. 

Install pygame, random, and math (assuming these libraries are not already installed). Install the GalactorRepublic folder and run the program by executing py project.py.

All images were created by me. This project is an ongoing project and I plan to constantly be updating it.

The game starts in the project.py file where the user is instructed to press space to start the game. Once the space bar is hit, or the start button is pressed, the run method is called and the infinite run loop is started for the game. It keeps track of the user input and adjusts the x and y coordinates of the spaceship accordingly. Asteroids are also generated in the update and render methods of game.py. Collision is detected using colliderect by making the spaceship and asteroid images rectanges and checking if their path intersect. If this happens the game is over and will stay in another infinite loop until the player presses space to restart the game. There is no score feature, no buttons and not way to efefctively pause and resume the game.

The next plan is to conitnue polishing the game, add more characters to choose from that can be accessed with currency, add a scoring method for personal high score as well as score amongst other users, and to add some form of database SQL or SQLite to store user data and keep track of in-game progress.

    TODO: Use the arrow keys to manipulate the character, space bar to shoot lasers (3 second interval between laser shots), once the player score reaches 50 the laser shot interval decreases to 0.75 seconds.
