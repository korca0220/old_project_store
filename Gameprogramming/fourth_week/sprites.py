#sprite classes for ploatform game
import pygame as pg
import random
from settings import *
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):

    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30,40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.pos= vec(10, 580)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):
        self.vel.y = -PLAYER_JUMP

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)#가속값 -> X는 0이고 Y는 중력이 적용
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION #X에만 마찰력이 적용됨 (Y는 중력 적용)

        #equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        #wrap around the sides of the screen
        if self.pos.x > WIDTH :
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Enemy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        #Enemy 객체가 생성되는 x,y 값은 랜덤하게 생성됨
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        #Enemy의 각 객체별로 상이한 속도를 갖고 있음.
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(1, 5)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        #객체가 바닥을 지나거나, 왼쪽 또는 오른쪽 화면을 넘어 갔을시
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(1, 5)

class Bullet(pg.sprite.Sprite):
    def __init__(self, x , y):
        pg.sprite.Sprite.__init__(self)
        player = Player(self)
        self.image = pg.Surface((10, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        #총알 객체는 현재 player객체의 위치를 기준으로 생성 됨,
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
