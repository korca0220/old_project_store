<h1>GameProgramming

# 5주차 #
- 진행사항
- 추가사항

## 진행사항 ##

**Game클래스에 이미지 로드 함수 구현**

여러개의 이미지를 불러오기 위해 헬퍼 함수 작성.
```python
  def load_date(self):
      self.dir = os.path.dirname(__file__)
      img_dir = os.path.join(self.dir, 'Image')
      self.stand = Spritesheet(os.path.join(img_dir, STAND))
      self.jump = Spritesheet(os.path.join(img_dir, JUMP))
      ....
```

**이미지 로드 클래스 구현**

- 이미지시트(sheet)의 각 좌표로 부터 이미지를 불러오기 위함
- .convert()를 이용해 `self.spritesheet`가 갖고 있는 값을 보다 빠르게 load

```python
class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        return image
```

**Player클래스에 이미지 로드 함수 구현**

- 각 이미지 프레임별로 List에 넣기 위함
- `set_colorkey`를 이용해 이미지 뒷 배경을 제거

```python
def load_images(self):
      self.standing_frames = [self.game.stand.get_image(2, 0, 28, 40),
                              self.game.stand.get_image(32, 0, 29, 40),
                              self.game.stand.get_image(62, 0, 28, 40)]
      for frame in self.standing_frames:
          frame.set_colorkey(WHITE)
      self.walk_frame_l = [self.game.move.get_image(0, 0, 30, 40),
                          self.game.move.get_image(30, 0, 30, 40)]
      self.walk_frame_r = []
      for frame in self.walk_frame_l:
          frame.set_colorkey(WHITE)

      for frame in self.walk_frame_l:
          self.walk_frame_r.append(pg.transform.flip(frame, True, False))
      self.jump_frame = self.game.jump.get_image(0, 0, 30, 40)
```

**Jump Cut 구현**

- Keyup 이벤트 발생시 점프값을 감소 시킴
- 보다 Detail한 점프 가능

```python
def jump_cut(self):
    if self.jumping:
        if self.vel.y < -2:
            self.vel.y = -3
```

**동작 애니메이션 구현**

- 각 애니메이션이 필요한 부분 동작별 구현
- 게임 진행 시간(tick)을 이용하여 프레임 계산

```python
def animate(self):
    now = pg.time.get_ticks() #millisecond 단위로 현재 게임시간을 갖고옴

    #움직임 값(Bollean)에 대한 명세
    if self.vel.x != 0:
        self.walking = True
    else:
        self.walking = False

    #player가 움직이고 있을 떄(True) 애니메이션
    if self.walking:
        print(self.current_frame)
        if now - self.last_update > 120: #프레임 속도를 위한 값
            self.last_update = now
            #현재 프레임 값은 계속 1씩 증가하면서 이미지의 프레임 길이만큼 나눠짐
            #즉, 프레임 길이에 따라서 current_frame값이 바뀜
            self.current_frame = (self.current_frame + 1) % len(self.walk_frame_l)
            if self.vel.x > 0: #바뀌는 current_frame 값이 이미지의 프레임을 순회.
                self.image = self.walk_frame_r[self.current_frame]
            else:
                self.image = self.walk_frame_l[self.current_frame]

    if self.vel.y != 0:
        self.jumping = True

    #제자리 점프에 대한 애니메이션
    if self.jumping and not self.walking:
        if now - self.last_update > 150:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % 1
            self.image = self.jump_frame
            self.image.set_colorkey(GREEN)

    #가만히 있을때 애니메이션
    if not self.jumping and not self.walking:
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            self.image = self.standing_frames[self.current_frame]

```

## 수정 사항 ##

**적 객체 생성**

- update()안에 넣어 계속적으로 적이 생성되도록 변경
- new()에서 -> update()로 변경
```python
while len(self.enemys) < 8:
    enemy = Enemy(self) #객체 생성
    self.all_sprites.add(enemy) #객체를 all_sprites 그룹에 추가
    self.enemys.add(enemy) # 적 sprite 그룹에 추가
```

**각 클래스별 매개변수 추가**

- Game 객체를 매개변수로 받기 위함
- Game 객체에서 생성된 이미지를 불러오기 위함.
```python
self.game = game
```
