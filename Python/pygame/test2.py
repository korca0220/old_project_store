#coding=utf-8
import random
import pygame
pygame.init()

random_list_music = ['Fight','Summer_Break','Flaming','Counting_Star','Catching_the_beat']
choice_music = {'Fight':'D:\Storage\Study\Python\pygame\Music\Fight.mp3',
                'Summer_Break':'D:\Storage\Study\Python\pygame\Music\Summer_Break.mp3',
                'Flaming':'D:\Storage\Study\Python\pygame\Music\Flaming.mp3',
                'Counting_Star':'D:\Storage\Study\Python\pygame\Music\Counting Star.mp3',
                'Catching_the_beat':'D:\Storage\Study\Python\pygame\Music\Catching the beat.mp3'}
myImg = pygame.image.load('D:\Storage\Study\Python\pygame\Image\horror_image.jpg')

pygame.mixer.music.load(choice_music[random.choice(random_list_music)])
pygame.mixer.music.play(0) #0은 한번, -1은 무한
display_width = 800
display_height = 600

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
