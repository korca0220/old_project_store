import os
import random
import pygame as pg
from settings import *
from sprites import *


myImg = os.path.join(os.path.abspath(BACKGROUND))
myImg2 = os.path.join(os.path.abspath(BACKGROUND2))
gameImg = pg.image.load(myImg)
gameImg2 = pg.image.load(myImg2)


class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True #게임 실행 Boolean 값
        self.count = 0 #점프 카운트 값
        self.font_name = pg.font.match_font(FONT_NAME) #FONT_NMAE과 맞는 폰트를 검색
        self.x=0
        self.x1 = WIDTH
        self.frame_count = 0



    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.enemys = pg.sprite.Group() #적 sprite 그룹 생성
        self.bullets = pg.sprite.Group() # 총알 sprite 그룹 생성
        self.platforms = pg.sprite.Group() #platforms(블록) sprites 그룹 생성
        self.player = Player(self) #self.player, Player객체 생성
        self.all_sprites.add(self.player)
        #PLATFORM_LIST에서 각 value값을 받아와 객체 생성
        for plat in PLATFORM_LIST:
            p = Platform(*plat) #python에서 *은 point가 아닌 리스트 언패킹
            self.all_sprites.add(p)
            self.platforms.add(p)
        for i in range(6): #한번에 총 N개의 적이 생성
            enemy = Enemy() #객체 생성
            self.all_sprites.add(enemy) #객체를 all_sprites 그룹에 추가
            self.enemys.add(enemy) # 적 sprite 그룹에 추가
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
                self.player.pos.y = hits[0].rect.top+1 #충돌시 player의 Y축 위치값이 충돌한 블록의 TOP값으로
                                                     #즉, 블록위에 있는 것처럼 보이게함
                self.player.vel.y = 0

        # player 위치가 1/2(스크린) 이상 왔을 떄
        if self.player.rect.top <= HEIGHT / 1.5:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10
            for ene in self.enemys: #적 객체 또한 plat객체 처럼 '+'시킴
                ene.rect.y += abs(self.player.vel.y)

        #블록 재생성
        while len(self.platforms) < 6:
            width = random.randrange(50, 200)
            p = Platform(random.randrange(0, WIDTH-width),
                         random.randrange(20, 60),
                         width, 20)
            self.platforms.add(p)
            self.all_sprites.add(p)

        #Game over
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        #bullet(총알)과 enemy(적) 충돌 체크
        if pg.sprite.groupcollide(self.bullets, self.enemys, True, True):
            self.score += 10 #점수를 10점 증가시킴

        #player와 enemy 충돌(game over 조건)
        hits = pg.sprite.spritecollide(self.player, self.enemys, False)
        if hits:
            self.playing = False


    def events(self):
        #game loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            #점프
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_x and self.count <1:
                    self.count += 1
                    self.player.jump()
                elif pg.sprite.spritecollide(self.player, self.platforms, False):
                    self.count = 0
            #총 발사
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    bullet = Bullet(self.player.rect.centerx, self.player.rect.top) #player 객체의 위치정보를 받아 bullet 객체 생성
                    self.all_sprites.add(bullet)
                    self.bullets.add(bullet)


    #음악 재생 컨트롤러
    def music(self):
        myMusic = os.path.join(os.path.abspath(MUSIC_DICT[random.choice(MUSIC_LIST)]))
        pg.mixer.music.load(myMusic)
        pg.mixer.music.play(0)


    def draw(self):
        #game loop - draw
        self.x1 -= 2
        self.x -= 2
        self.screen.blit(gameImg2, (self.x, 0))
        self.screen.blit(gameImg, (self.x1, 0))
        if self.x == -WIDTH:
            self.x = WIDTH
        if self.x1 == -WIDTH:
            self.x1 = WIDTH
        self.all_sprites.draw(self.screen)
        self.draw_text('Score :' +str(self.score), 22, WHITE, WIDTH-50, 15)
        pg.display.update()

    def show_start_screen(self):
        #GAME START시에 나타낼 스크린
        self.screen.fill(BLUE)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Arrow to move, X to jump", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH/2, HEIGHT*3/4)
        pg.display.update()
        self.wait_for_key()

    def show_over_screen(self):
        # Game Over시에 나타낼 스크린
        self.screen.blit(gameImg, (1,1))
        self.draw_text("GAVE OVER", 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Score : "+ str(self.score), 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press a key to play again, QUIT to 'ESC'", 22, WHITE, WIDTH/2, HEIGHT*3/4)
        pg.display.update()
        self.wait_for_key()
        if not self.running:
            return

    #START와 OVER스크린에서 화면대기 및 진행을 위한 메서드
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                elif event.type == pg.KEYUP:
                    waiting = False

    #화면에 텍스트 처리를 위한 메서드
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
        #render(text, antialias, color, background=None) -> Surface


g = Game()
g. show_start_screen()
while g.running:
    g.music()
    g.new()
    g.show_over_screen()

pg.quit()
