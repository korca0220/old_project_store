<h1>GameProgramming

# 마지막 버전 #
- 진행사항
- 기본 소스 변동사항

#### 추가 된 사항이 많아 Text, Image, Sound 관련해서는 생략 ####
## 진행사항 ##

**Item 4종류 추가**

```python
class Item(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = random.choice(['powerup', 'kill', 'speeddown', 'speedup'])
        self.image = self.game.box.get_image(0, 0, 20, 20)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.plat.rect.topleft
        self.rect.bottom = self.plat.rect.top+1

    def update(self):
        self.rect.bottom = self.plat.rect.top+1
        if not self.game.platforms.has(self.plat): #아이템 중복검사
            self.kill()
```

```python
item_hits = pg.sprite.spritecollide(self.player, self.items, True)
  for item in item_hits: #아이텥 목록
      if item.type == 'kill': # 현재 생성된 객체들에 한해서 적 객체 제거
          for enemy in self.enemys:
              self.score += 10
              self.item_kill.play()
              enemy.kill()
      if item.type == 'speedup': # 현재 생성된 객체들에 한해서 적 객체 속도 증가
          for enemy in self.enemys:
              self.item_speedup.play()
              enemy.speedx = random.randrange(-1, 5)
              enemy.speedy = random.randrange(3, 7)
      if item.type == 'speeddown': # 현재 생성된 객체들에 한해서 적 객체 속도 감소
          for enemy in self.enemys:
              self.item_speeddown.play()
              enemy.speedx = random.randrange(-5, 2)
              enemy.speedy = random.randrange(0, 3)
      if item.type == 'powerup': # 나가는 총알 개수 증가, 총 3개까지 증가
          self.item_powerup.play()
          if self.player.power <= 3:
              self.player.power +=1
```


**적 객체에 대한 애니메이션 추가**

데이터를 로드 후
```python
def load_date(self):
      self.meteo_frames = [self.game.enemy.get_image(0, 0, 30, 40),
                           self.game.enemy.get_image(30, 0, 30, 40),
                           self.game.enemy.get_image(60, 0, 30, 40),
                           self.game.enemy.get_image(90, 0, 30, 40)]
      for frames in self.meteo_frames:
          frames.set_colorkey(BLACK)
```

`animate` 메서드로 애니메이션 적용
적 객체는 4개의 프레임으로 구성
```python
def animate(self):
      now = pg.time.get_ticks() #millisecond 단위로 현재 게임시간을 갖고옴

      if now - self.last_update > 120: #프레임 속도를 위한 값
          self.last_update = now
          #현재 프레임 값은 계속 1씩 증가하면서 이미지의 프레임 길이만큼 나눠짐
          #즉, 프레임 길이에 따라서 current_frame값이 바뀜
          self.current_frame = (self.current_frame + 1) % len(self.meteo_frames)
          self.image = self.meteo_frames[self.current_frame]
```
`Enemy(Meteo)이미지`
![meteo](./Image/meteorite.png)
<br>
**플랫폼(블록) 이미지 추가**
```python
images = [self.game.block1.get_image(0, 0, 100, 20),
           self.game.block2.get_image(0, 0, 80, 20),
           self.game.block3.get_image(0, 0, 50, 20)]
 ```
 ![block1](./Image/block1.png)
 ![block2](./Image/block2.png)
 ![block3](./Image/block3.png)
<br>

**효과음 추가**
Jump, Shoot, Game-Over, Hit, Intro,,, 등

```python
#sound(효과음)
self.snd_dir = os.path.join(self.dir, 'sound')
self.jump_sound = pg.mixer.Sound(os.path.join(self.snd_dir, 'Jump.wav'))
self.shoot_sound = pg.mixer.Sound(os.path.join(self.snd_dir, 'Shoot.wav'))
self.hit_sound = pg.mixer.Sound(os.path.join(self.snd_dir, 'Hit.wav'))
self.game_over_sound = pg.mixer.Sound(os.path.join(self.snd_dir, 'Gameover.wav'))
...
```

**Intro 영상 및 Openning 영상 추가**

`moviepy` 라이브러리 이용
```python
from moviepy.editor import VideoFileClip
```

```python
#Openning
def openning(self):
    clip = VideoFileClip('open.mp4')
    clip.preview()
    sleep(2)
    self.show_start_screen()

#Intro
def intro_movie(self):
    clip = VideoFileClip('intro.mpeg')
    clip.preview()
    self.intro_effect.play()
    self.draw_text("17.8", 40, WHITE, WIDTH/2, HEIGHT-100)
    pg.display.update()
    sleep(2)
```
**Highscore 저장**

```python
with open(os.path.join(self.dir, SCORE), 'r') as f:
        try :
            self.highscore = int(f.read())
        except:
            self.highscore = 0
```


**시작 화면(Menu)에 대한 로직 추가**

```python
  def show_start_screen(self):
      #GAME START시에 나타낼 스크린
      pg.mixer.music.load(os.path.join(self.snd_dir, 'Mysterious.ogg'))
      pg.mixer.music.play(loops=-1)
      self.running = True
      self.start_new()
      pg.mixer.music.fadeout(500)

  def start_run(self):
      #start loop
      self.start_playing = True
      while self.start_playing:
          self.clock.tick(FPS)
          self.start_events()
          self.start_update()
          self.start_draw()

  def start_events(self):
      for event in pg.event.get():
          if event.type == pg.QUIT:
              if self.start_playing:
                  self.start_playing = False
              self.start = False

  def start_new(self):
      self.start_group = pg.sprite.Group()
      self.select = Select(self)
      self.start_group.add(self.select)
      self.start_run()

  def start_update(self):
      self.start_group.update()

  def start_draw(self):
    ....
```


**Play time 체크**

```python
self.second = ((pg.time.get_ticks() - self.start_tick)/1000)
```

**Level 추가**

게임 레벨 증가에 따라서 적(운석)의 속도 증가.
```python
if self.score == 1000:
      self.score += 10
      self.level_up.play()
      self.leveup_text()
      sleep(0.4)
      self.enemy_level += 1
      self.levelup(self.enemy_level)
  elif self.score == 2500:
      self.score += 10
      self.level_up.play()
      self.leveup_text()
      sleep(0.4)
      self.levelup(self.enemy_level)
  elif self.score == 4000:
      self.score += 10
      self.level_up.play()
      self.leveup_text()
      sleep(0.4)
      self.levelup(self.enemy_level)
```


**게임 클리어 화면 추가**

```python
def ending_screen(self):
      self.screen.fill(BLACK)
      pg.mixer.music.load(os.path.join(self.snd_dir, 'Ending.mp3'))
      pg.mixer.music.play(loops=-1)
      self.draw_text("GAME OVER", 48, WHITE, WIDTH/2, HEIGHT - 400)
      self.draw_text("YOUR SCORE : "+ str(self.score), 20, WHITE, WIDTH/2, HEIGHT - 300)
      if self.score > self.highscore:
          self.highscore = self.score
          self.draw_text("NEW HIGH SCORE! : "+ str(self.score), 20, WHITE, WIDTH/2, HEIGHT - 250)
          with open(os.path.join(self.dir, SCORE), 'w') as f:
              f.write(str(self.score))
      else:
          self.draw_text("HIGH SCORE : "+ str(self.highscore), 20, WHITE, WIDTH/2, HEIGHT - 250)
      self.draw_text("ClEAR TIME : "+ str(self.second), 20, WHITE, WIDTH/2, HEIGHT - 200)
      pg.display.update()
      self.wait_for_key2()
  ```

**토끼 머리(클리어 조건) 추가**

15개를 먹어야 클리어
```python
class Rabbithead(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self.groups = game.all_sprites, game.heads
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.image = self.game.head.get_image(0, 0, 30, 30)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top+1

    def update(self):
        self.rect.bottom = self.plat.rect.top+1
        if not self.game.platforms.has(self.plat): #아이템 중복검사
            self.kill()
```

```python
get_heads = pg.sprite.spritecollide(self.player, self.heads, True)
    if get_heads:
        self.get_heads.play()
        self.head_count += 1
```

```python
#게임 클리어 조건
if self.head_count == 15:
    self.clear_text()
    self.ending = True
    self.playing = False
    self.head_count = 0
    sleep(1)
```

**Select(선택지) 추가**
초기 메뉴에서 선택에 따른 게임 진행

```python
class Select(pg.sprite.Sprite):

    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((120,40))
        self.image.blit(self.game.menu_select, (0, 0))
        self.image.set_alpha(0)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH - 70, HEIGHT - 340)
        self.select_number = 0

    def update(self):
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.select_number -= 1
            if self.select_number < 0:
                self.select_number = 2
            if self.select_number == 0:
                self.rect.center = (WIDTH - 70, HEIGHT - 340)
                sleep(0.14)
            elif self.select_number == 1:
                self.rect.center = (WIDTH - 70, HEIGHT - 290)
                sleep(0.14)
            elif self.select_number == 2:
                self.rect.center = (WIDTH - 70, HEIGHT - 240)
                sleep(0.14)

        if keys[pg.K_DOWN]:
            self.select_number += 1
            if self.select_number > 2:
                self.select_number = 0
            if self.select_number == 0:
                self.rect.center = (WIDTH - 70, HEIGHT - 340)
                sleep(0.14)
            elif self.select_number == 1:
                self.rect.center = (WIDTH - 70, HEIGHT - 290)
                sleep(0.14)
            elif self.select_number == 2:
                self.rect.center = (WIDTH - 70, HEIGHT - 240)
                sleep(0.14)

        if keys[pg.K_z] and self.select_number == 0:
            self.game.openning() #오프닝 영상 재생

        if keys[pg.K_z] and self.select_number == 1:
            self.game.start_playing = False #게임시작

        if keys[pg.K_z] and self.select_number == 2:
            pg.quit() #게임 종료
            quit()
```

## 기본 소스 변동 사항 ##

**Enemy(적)클래스 속도 변경**

Level 별로 속도를 증가시키기 위함.
```python
self.max_speed_x = self.game.speed_x
    self.max_speed_y = self.game.speed_y
    self.min_speed_x = self.game.speed_x_min
    self.min_speed_y = self.game.speed_y_min
```


**게임 진행 로직 변경**

```python
g = Game()
g.intro_movie()
while g.start:
    g.show_start_screen()
    while g.running:
        g.new()
        if g.ending == True:
            g.ending_screen()
            if g.clear == True:
                g.running = False
                g.start = False
        else:
            g.show_over_screen()
pg.quit()
```

**`music()` 메서드 삭제**

```python
def music(self):
    myMusic = os.path.join(os.path.abspath(MUSIC_DICT[random.choice(MUSIC_LIST)]))
    pg.mixer.music.load(myMusic)
    pg.mixer.music.play(0)
```
여러개의 배경음을 랜덤으로 재생할 생각이었으나,
게임 분위기상 하나의 배경음만을 재생하는 것으로 변경.

```python
def new(self):
  ....
  pg.mixer.music.load(os.path.join(self.snd_dir, 'old city theme.ogg')) #배경음 로드
      self.run()
```

```python
def run(self):
    #game loop
    pg.mixer.music.play(loops=-1) #배경음 플레이 (loops 값 false = 반복, true = 한번)
    ....
```      

**mask 충돌**
`player`객체와 `enemy`객체에 mask를 씌움.
좀 더 정밀한 체크를 통해 충돌 체크를 하기 위함

```python
self.mask = pg.mask.from_surface(self.image) #플레이어 mask

self.mask = pg.mask.from_surface(self.image) #적 mask

#mask 충돌 체크
hits = pg.sprite.spritecollide(self.player, self.enemys, False, pg.sprite.collide_mask)
```
