#base properties
BACKGROUND = 'Image\city_image.jpg'
BACKGROUND2 = 'Image\city_image2.jpg'
TITLE = "My game"
WIDTH = 512
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'

#Player properties
PLAYER_ACC = 0.65
PLAYER_FRICTION = -0.15
PLAYER_GRAV = 0.5
PLAYER_JUMP = 14

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20),
                (125, HEIGHT - 350, 80, 20),
                (350, 400, 100, 20),
                (175, 300, 50, 20)] #total 5 List

#define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255 ,255 ,0)
WHITE_A = (255, 255, 255, 180)

#Music
MUSIC_DICT = {'Catching' :'Music\Catching the beat.mp3',
              'CountingStar' :'Music\Counting Star.mp3',
              'Fight':'Music\Fight.mp3',
              'Flaming' : 'Music\Flaming.mp3',
              'Start' : 'Music\Start.mp3',
              'Summer' : 'Music\Summer_Break.mp3'
              }
MUSIC_LIST = ['Catching', 'CountingStar', 'Fight', 'Flaming', 'Start', 'Summer']

#Image
STAND = "stand.png"
JUMP = "jump.png"
MOVE = "move.png"
BULLET = "bullet.png"
ENEMY = "meteorite.png"
JUMP = "jump.png"
JUMP_RIGHT = "jump_right.png"
