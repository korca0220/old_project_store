# **GameManager**

## *모듈*
---
- firstmenu.cpp
- firstmenu.h

#### 사용자생성, 로또게임 시작, 러시안룰렛 시작, 가위바위보 시작을 위한 처음 화면
#### 사용자생성 - 사용자는 100명까지 생성가능하며, 각각의 기본자금을 갖고 개개인별로 관리 됨
##### < 개발담당 : 박준우 >
---
- gawi.cpp
- gawi.h

#### 간단한 가위바위보 게임으로 연승시 보상금액이 배수로 증가함.
#### 가장 많은 연승을 한 플레이어는 최고 연승 플레이어로 저장됨(bestrecord.txt)
##### < 개발담당 : 박준우 >
---
- lotto.cpp
- lotto.h

#### 게임 진행방식은 현실의 로또와 같으며, 자리수(선택)별로 얻는 보상 금액이 달라진다.
##### < 개발담당 : 이범희 >
---
- russian.cpp
- russian.h

#### 러시안 룰렛의 방식과 같으며, 연승개념이 있다. 연승별 보상금액이 달라진다.
##### < 개발담당 : 유호중 >
---
- main.cpp

#### 게임을 시작하는 main부분이다. main에서 firstmenu실행 -> 다른 메뉴선택 -> 선택지...
#### 방식으로 진행되어지는 부분이다.
##### < 개발담당 : 공동 >
---
- money.h

#### 각 플레이어별로 개인 자금을 갖고, 게임별로 각 고유의 플레이어가 갖고있는 자본을 사용하기 위함.
#### 각각의 모듈에서 gamemoney 라는 클래스를 객체화 하여 사용하고 있다.
##### < 개발담당 : 공동 >
