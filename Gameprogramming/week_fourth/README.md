<h1>GameProgramming

# 4주차 #
- 진행사항
- 추가사항

## 진행사항 ##

**적 객체 구현**
* 적이 등장하는 부분은 랜덤(지정된 값 사이)
* 각 적 객체마다 다른 속도를 갖고 있음
```python
class Enemy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(1, 5)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            .... 생략
```


**총알 객체 구현**
* 총알이 WIDTH == 값이 되면 객체 삭제
```python
class Bullet(pg.sprite.Sprite):
    def __init__(self, x , y):
        pg.sprite.Sprite.__init__(self)
        player = Player(self)
        self.image = pg.Surface((10, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
```

**적 객체 생성**

```python
for i in range(6): #한번에 총 N개의 적이 생성
        enemy = Enemy() #객체 생성
        self.all_sprites.add(enemy) #객체를 all_sprites 그룹에 추가
        self.enemys.add(enemy) # 적 sprite 그룹에 추가
```

**충돌 조건 추가(적과 총알, 플레이어와 적)**

```python
#bullet(총알)과 enemy(적) 충돌 체크
if pg.sprite.groupcollide(self.bullets, self.enemys, True, True):
    self.score += 10 #점수를 10점 증가시킴

#player와 enemy 충돌(game over 조건)
hits = pg.sprite.spritecollide(self.player, self.enemys, False)
if hits:
    self.playing = False
```

**총 발사 이벤트 추가**
* 해당 키를 누르면 총알 객체를 생성함.

```python
#총 발사
if event.type == pg.KEYDOWN:
    if event.key == pg.K_z:
      bullet = Bullet(self.player.rect.centerx, self.player.rect.top)
      self.player.rect.top)
      self.all_sprites.add(bullet)
      self.bullets.add(bullet)
```

## 추가 및 변동 사항 ##

**Sprite group 생성 추가**

```python
    self.enemys = pg.sprite.Group() #적 sprite 그룹 생성
    self.bullets = pg.sprite.Group() # 총알 sprite 그룹 생성
```

**화면 이동에 따른 적 객체 이동**
```python
for ene in self.enemys: #적 객체 또한 plat객체 처럼 '+'시킴
    ene.rect.y += abs(self.player.vel.y)
  ```
