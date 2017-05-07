import random
import pygame as pg
from settings import *
from sprites import *
myImg = pg.image.load('D:\Storage\Study\Junewoo\Gameprogramming\week_second\Image\city_image.jpg')

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.count = 0


    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group() #platforms(블록) sprites 그룹 생성
        self.player = Player(self) #self.player, Player객체 생성
        self.all_sprites.add(self.player)
        #PLATFORM_LIST에서 각 value값을 받아와 객체 생성
        for plat in PLATFORM_LIST:
            p = Platform(*plat) #python에서 *은 point가 아닌 리스트 언패킹
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()


    def run(self):
        #game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        #game loop - update
        self.all_sprites.update()
        if self.player.vel.y > 0:
            #hits -> spritecollide 메서드를 이용(x,y, default boolean)충돌 체크
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top + 1  #충돌시 player의 Y축 위치값이 충돌한 블록의 TOP값으로
                                                            #즉, 블록위에 있는 것처럼 보이게함
                self.player.vel.y = 0

            elif self.player.rect.midtop == self.platforms:
                self.player.pos.y = hits[0].rect.bottom - 1
                self.player.vel.y = 10


    def events(self):
        #game loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            #점프 구현
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_x and self.count <2: #count값을 두어 최대 2단 점프
                    self.count += 1
                    self.player.jump()
                #2번 점프하고 바닥과의 충돌이 발생하면 count값을 다시 0으로 둠
                elif pg.sprite.spritecollide(self.player, self.platforms, False):
                    self.count = 0


    def draw(self):
        #game loop - draw
        self.screen.fill(BLACK)
        self.screen.blit(myImg, (1,1))
        self.all_sprites.draw(self.screen)
        pg.display.update()

    def show_start_screen(self):
        #game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
