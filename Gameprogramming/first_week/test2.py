#coding=utf-8
import os
import random
import pygame
pygame.init()

Fight = os.path.join('Music', 'Fight.mp3')
Summer_Break = os.path.join('Music', 'Summer_Break')
Flaming = os.path.join('Music', 'Flaming')
Counting_Star = os.path.join('Music', 'Counting_Star')
Catching_the_beat = os.path.join('Music', 'Catching_the_beat')
horror_image = os.path.join('Image', 'horror_image.jpg')
random_list_music = ['Fight','Summer_Break','Flaming','Counting_Star','Catching_the_beat']

myImg = pygame.image.load(horror_image)

pygame.mixer.music.load(random.choice(random_list_music))
pygame.mixer.music.play(0) #0은 한번, -1은 무한
display_width = 300
display_height = 300

DISPLAYSURF = pygame.display.set_mode((display_width,display_height))

def myimg(x,y):
    DISPLAYSURF.blit(myImg, (x, y)) #blit 그려주는 것

# x = (display_width * 0.5)
# y = (display_height * 0.5)
x=1
y=1

finished=False
while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True


    DISPLAYSURF.fill((255,255,255)) #배경색
    myimg(x,y)
    pygame.display.update() # ==flip()

pygame.quit()
quit()
