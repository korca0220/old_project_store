#base properties
BACKGORUND = 'Image\city_image.jpg'
TITLE = "My game"
WIDTH = 512
HEIGHT = 800
FPS = 60
FONT_NAME = 'arial'

#Player properties
PLAYER_ACC = 0.65
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.5
PLAYER_JUMP = 12.5

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20),
                (125, HEIGHT - 350, 100, 20),
                (350, 300, 100, 20),
                (175, 200, 50, 20)] #total 5 List

#define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255 ,255 ,0)
WHITE_A = (255, 255, 255, 180)
