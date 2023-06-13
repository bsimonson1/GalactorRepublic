import sys
from cx_Freeze import setup, Executable

executables = [Executable('project.py')]

packages = ['game.py', 'asteroid.py', 'laser.py']

include_files = [r'C:\Users\bengs\OneDrive\Desktop\GalactorRepublic\a-hero-of-the-80s-126684.mp3', r'C:\Users\bengs\OneDrive\Desktop\GalactorRepublic\background_image.png', 
                r'C:\Users\bengs\OneDrive\Desktop\GalactorRepublic\controls.png', r'C:\Users\bengs\OneDrive\Desktop\GalactorRepublic\high_score.png', 
                r'C:\Users\bengs\OneDrive\Desktop\GalactorRepublic\score.png', r'C:\Users\bengs\OneDrive\Desktop\GalactorRepublic\large_asteroid.png', 
                r'C:\Users\bengs\OneDrive\Desktop\GalactorRepublic\medium_asteroid.png', r'C:\Users\bengs\OneDrive\Desktop\GalactorRepublic\small_asteroid.png', 
                r'C:\Users\bengs\OneDrive\Desktop\GalactorRepublic\pause.png', r'C:\Users\bengs\OneDrive\Desktop\GalactorRepublic\laser_bullet.png', 
                r'C:\Users\bengs\OneDrive\Desktop\GalactorRepublic\play.png', r'C:\Users\bengs\OneDrive\Desktop\GalactorRepublic\potential_character.png', 
                r'C:\Users\bengs\OneDrive\Desktop\GalactorRepublic\quit.png', r'C:\Users\bengs\OneDrive\Desktop\GalactorRepublic\resume.png', 
                r'C:\Users\bengs\OneDrive\Desktop\GalactorRepublic\retry.png',  r'C:\Users\bengs\OneDrive\Desktop\GalactorRepublic\rishgular-font\RishgularTry-x30DO.ttf']

options = {
    'build_exe': {
        'packages': packages,
        'include_files': include_files
    }
}

setup(
    name='Galactor',
    version='1.0',
    description='2D infinite sspace shooter. Goal is to survive for as long as possible. Use the arrow keys to avoid incoming asteroids and use the spacebar to shoot asteroids. 3-second cool down on the shoot ability so use it wisely! Press the M-key to muse the song. ',
    options=options,
    executables=executables
)