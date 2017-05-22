<h1>GameProgramming

# 3주차 #
- 진행사항

## 진행사항 ##

**화면 이동 및 객체 삭제구현**
```python
# player 위치가 1/2(스크린) 이상 왔을 떄
    if self.player.rect.top <= HEIGHT / 2:
        self.player.pos.y += abs(self.player.vel.y)
        for plat in self.platforms:
            plat.rect.y += abs(self.player.vel.y)
            if plat.rect.top >= HEIGHT:
                #화면에서 보이지 않는 객체들 삭제
                plat.kill()
                self.score += 10 #점수 10점씩
```

**블록의 재생성**
```python
    #화면상 블록객체가 6개 미만인 경우에 블록 생성
    while len(self.platforms) < 6:
        width = random.randrange(50, 150)
        #블록의 크기를 랜덤하게.
        p = Platform(random.randrange(0, WIDTH-width),
                     random.randrange(-75, -30),
                     width, 20)
        self.platforms.add(p)
        self.all_sprites.add(p)
```

**GAME OVER**
```python
    if self.player.rect.bottom > HEIGHT: #플레이어 낙하시
        #화면상 존재하는 sprite객체들을 전부 위에로 올림
        #떨어지는 시각효과
        for sprite in self.all_sprites:
            sprite.rect.y -= max(self.player.vel.y, 10)
            if sprite.rect.bottom < 0:
                sprite.kill()
    if len(self.platforms) == 0:
        self.playing = False #playing값이 True경우만 run()이 돌아감
```
**음악 컨트롤러**
```python
#음악들의 URL을 담은 DICT
MUSIC_DICT = {'Catching' :'Music\Catching the beat.mp3',
              'CountingStar' :'Music\Counting Star.mp3',
              'Fight':'Music\Fight.mp3',
              'Flaming' : 'Music\Flaming.mp3',
              'Start' : 'Music\Start.mp3',
              'Summer' : 'Music\Summer_Break.mp3'
              }
#음악 재생목록들(제목)
MUSIC_LIST = ['Catching', 'CountingStar', 'Fight', 'Flaming', 'Start', 'Summer']
```
```python
def music(self):
       myMusic = os.path.join(os.path.abspath(MUSIC_DICT[random.choice(MUSIC_LIST)]))#DICT를 이용해 URL을 가지고옴
       pg.mixer.music.load(myMusic)#랜덤으로 재생
       pg.mixer.music.play(0)#0은 한번, 1은 두번
```
**화면 텍스트 처리**
```python
#화면에 텍스트 처리를 위한 메서드
def draw_text(self, text, size, color, x, y):
    font = pg.font.Font(self.font_name, size)#폰트 객체를 생성
    text_surface = font.render(text, True, color)#내용 및 COLOR값을 surface로 받은 후
    text_rect = text_surface.get_rect()#surface를 rect값으로 받아
    text_rect.midtop = (x, y)#중간 맨위에서부터 input값(x,y)를
    self.screen.blit(text_surface, text_rect)#화면에 blit해줌

    #render -> render(text, antialias, color, background=None) => Surface
```

**시작, 게임오버 화면**
```python
def show_start_screen(self):
    #GAME START시에 나타낼 스크린
    self.screen.fill(BLUE) #스크린을 채워줄 색상은 BLUE(파란색)
    self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
    self.draw_text("Arrow to move, X to jump", 22, WHITE, WIDTH/2, HEIGHT/2)
    self.draw_text("Press a key to play", 22, WHITE, WIDTH/2, HEIGHT*3/4)
    pg.display.update()
    self.wait_for_key()

def show_over_screen(self):
    # Game Over시에 나타낼 스크린
    self.screen.blit(gameImg, (1,1)) #blit으로 gameImg(게임배경)으로 배경을 그림
    self.draw_text("GAVE OVER", 48, WHITE, WIDTH/2, HEIGHT/4)
    self.draw_text("Score : "+ str(self.score), 22, WHITE, WIDTH/2, HEIGHT/2)
    self.draw_text("Press a key to play again, QUIT to 'ESC'", 22, WHITE, WIDTH/2, HEIGHT*3/4)
    pg.display.update()
    self.wait_for_key()
    if not self.running:
        return
```
**wait_for_key()**
```python
#show_start_screen이나 show_over_screen시 사용자의 입력을 기다리는 메서드
def wait_for_key(self):
      waiting = True
      while waiting:
          self.clock.tick(FPS)
          for event in pg.event.get():
              if event.type == pg.QUIT: #게임종료시(X표 클릭)
                  waiting = False
                  self.running = False
              elif event.type == pg.KEYDOWN:
                  if event.key == pg.K_ESCAPE: #ESC 눌렀을시
                      self.running = False
              elif event.type == pg.KEYUP: #그 외의 킈 (any key)
                  waiting = False
#waiting값이 False가 되면 wait_for_key메서드는 종료되고
#start화면인 경우 게임시작, over화면인 경우 다시시작 or 게임종료
```
