import pygame
pygame.init()

DISPLAYSURF = pygame.display.set_mode((400,400))
pygame.display.set_caption('Test pygame')
finish = False
colorBlue = True
x=30
y=30
clock = pygame.time.Clock() #프레임단위를 위한 clock 사용

while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True

    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        colorBlue = not colorBlue

    pressed = pygame.key.get_pressed() #키값을 받음
    if pressed[pygame.K_UP]:
        y = y-3
    if pressed[pygame.K_DOWN]:
        y = y+3
    if pressed[pygame.K_LEFT]:
        x = x-3
    if pressed[pygame.K_RIGHT]:
        x = x+3
    DISPLAYSURF.fill((0,0,0))#원래 그려진 사각형을 지움

    if colorBlue:
        color = (0,128,255)
    else:
        color = (255,255,255)

    pygame.draw.rect(DISPLAYSURF, color, pygame.Rect(x,y,40,40))
    pygame.display.update()
    clock.tick(60) #1초 
