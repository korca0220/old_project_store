import pygame

WHITE= (255,255,255)
WIDTH = 1024
HEIGHT = 512
BACKGROUND_WIDTH = 1024


def block(block, x, y):
    global gamepad
    
def back(background, x,y):
    global gamepad
    gamepad.blit(background, (x,y))

def runGame():
    global gamepad, clock, background1, background2


    background_x1 = 0
    background_x2 = BACKGROUND_WIDTH

    finished = False
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
        gamepad.fill(WHITE)

        #배경을 2픽셀씩 왼쪽으로 이동
        background_x1 -= 2
        background_x2 -= 2

        #배경1이 사라지면 다시 오른쪽에 위치시키고
        #배경2또한 위와 같은 동작을 수행
        if background_x1 == -BACKGROUND_WIDTH:
            background_x1 = BACKGROUND_WIDTH
        if background_x2 == - BACKGROUND_WIDTH:
            background_x2 = BACKGROUND_WIDTH

        back(background1, background_x1,0)
        back(background2, background_x2,0)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()

def initGame():
    global gamepad, clock, background1, background2

    pygame.init()
    gamepad = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Pygame')
    background1 = pygame.image.load('D:\Storage\Study\Python\pygame\Image\city_image.jpg')
    background2 = pygame.image.load('D:\Storage\Study\Python\pygame\Image\city_image2.jpg')

    clock = pygame.time.Clock()
    runGame()

if __name__=='__main__':
    initGame()
