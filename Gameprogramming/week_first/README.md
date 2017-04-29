<h1> GameProgramming 

# 1주차 #
- 개발환경
- 진행사항 및 특이점

## 개발환경
- Version ->Python 3.6.0
- Library -> pygame 1.9.3
- Editor, IDE -> Atom, Pycharm2017

## 진행사항
- 초기 UML
- 모듈은 크게 3가지로 구분 **_main.py, setting.py, sprites.py_**
        
        main.py -> 게임을 실행시키는 전체적인 코드가 들어감(init, run, new, draw...)
        setting.py -> 상수값 설정 및 DEFINE 설정
        sprites.py -> Class 들에 대한 설정 및 정의(Player, Platform...)


## Importing ##
```python
import random
import pygame as pg  
from settings import *
from sprites import *
```

## Main 메서드 ##
```python
class Game:
    def __init__(self): #변수, 게임 기본설정 초기화
    def new(self): #게임을 시작
    def run(self): #Loop
    def update(self): #게임을 갱신 시키는 부분
    def events(self): #Event 처리에 대한
    def draw(self): #화면에 그려주는 함수
    def show_start_screen(self): #START 화면
    def show_go_screen(self): #GAMEOVER/CONTINUE 화면
```
## Sprites 메서드 ##
```python
class Player(pg.sprite.Sprite):
    def __init__(self):
    def update(self):
```

- 사용 할 배경에 대한 이미지 자료 수집
- 사용 할 배경음에 대한 음악 자료 수집(Gutiar 컨셉), 효과음은 아직X
- test1, test2 파일을 통한 테스트 코드 진행
