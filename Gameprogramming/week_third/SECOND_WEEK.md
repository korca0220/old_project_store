<h1>** GameProgramming **

# 2주차 #
- 진행사항
- 변경 및 수정 된 부분

## 진행사항 ##

** Platform(블록) 개체 구현 **
```python
class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
```

** 중력 구현 **
```python
PLAYER_GRAV = 0.5 #중력 값 = 0.5
self.acc = vec(0, PLAYER_GRAV)
```

** 점프 구현 **
```python
''' 'X'Key를 누르면 JUMP
    최대 2단 점프까지만'''
if event.type == pg.KEYDOWN:
    if event.key == pg.K_x and self.count <2:
        self.count += 1
        self.player.jump()
    elif pg.sprite.spritecollide(self.player, self.platforms, False):
        self.count = 0
  ```
** 충돌 **
```python
hits = pg.sprite.spritecollide(self.player, self.platforms, False)
```

# 변경 및 수정 된 부분

1.  ** PLATFROM_LIST(블록 위치값)상수 값 리스트를 이용하여 코드 축소 **
  ```python
  for plat in PLATFORM_LIST:
      p = Platform(*plat)
      self.all_sprites.add(p)
      self.platforms.add(p)
      ```
2. ** 마찰력을 X축만 받도록 수정 **
  ```python
  # apply friction
  self.acc.x += self.vel.x * PLAYER_FRICTION
  ```
