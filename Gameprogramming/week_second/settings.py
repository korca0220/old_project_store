#base properties
TITLE = "My game"
WIDTH = 1024
HEIGHT = 512
FPS = 60

#Player properties
PLAYER_ACC = 0.35
PLAYER_FRICTION = -0.08
PLAYER_GRAV = 0.5

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20),
                (125, HEIGHT - 350, 100, 20),
                (350, 200, 100, 20),
                (175, 100, 50, 20)] #total 5 List

#define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255 ,255 ,0)
