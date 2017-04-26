## POS 프로젝트

1.상품등록
: (상품, 가격)CD  (최민영,김한얼)

2.계산(판매)
: 상품선택 판매 갯수 , U (손주호,박정은)

3.정산
: 하루단위로 얼마판매했는지 상품명,상품갯수 (박준우,박범우)



# 코딩컨벤션

##1. 클래스명: UpperCamelCase

**Not Good**
```python
class printmenu():

  def __init__:
    pass

#or

class print_menu:

  def __init__:
    pass
```

**Good**
```python
class PrintMenu:

  def __init__:
    pass

내부적으로 쓰이면 밑줄을 앞에 붙입니다.
# 내부 클래스

class _PrintMenu():

  def __init__:
    pass
```

## 2. 메소드,변수 (모두 소문자)

서브 클래스(sub-class)의 이름충돌을 막기 위해서는 밑줄 2개를 앞에 붙입니다.
메소드명은 함수명과 같으나 비공개(non-public) 메소드, 혹은 변수면 밑줄을 앞에 붙입니다.

`single_trailing_underscore_`: 파이썬 키워드와의 충돌을 방지하기
  위해 쓰인다.  예)

    Tkinter.Toplevel(master, class_='ClassName')

`_single_leading_underscore`: "내부에서 사용한다"는 것을 의미.
 예를 들면, `from M import *`은 언더스코어로 시작하는 객체를 임포
 트하지 않는다.

ex) `public: method(self):` `non-public: _methon(self):`

**Not Good**
```python
class PrintMenu:

  MenuName = None

  def __init__(self,MenuName):
    self.MenuName = MenuName

```

**Good**

```python

함수명은 소문자로 구성하되 필요하면 밑줄로 나눕니다.
가독성을 위해 언더바(_)를 추가해도 좋다
클래스 내의 메소드 정의는 1줄씩 띄어 씁니다.

class PrintMenu:

  menu_name = None  

  def __init__(self,menu_name):
    self.menu_name = menu_name

  def some(self):
    pass


  #or

  class PrintMenu:

    menuname = None

    def __init__(self.menuname):
      self.menuname = menuname

```



## 3. 한 라인 79자가 넘을경우 ,단위로 개행적용

**Not Good**

```python
class PrintMenu:

  def __init__(self):
    pass


  def printSome(one,two,three,four,five,something,something1,module1):
    pass
```

**Good**

```python
class PrintMenu:

  def __init__(self):
    pass

    def printSome(self,
                one,
                two,
                three,
                four,
                five,
                something,
                something1,
                module1):
      pass

#or

  def printSome(
          self,one,
          two,three,
          four,five,
          something,something1,
           module1):
      pass

```


## 4. 내장모듈 맨위, 외장모듈 한칸띄고 모아쓰기

ex)
표준 라이브러리
관련이 있는 서드파티 라이브러리
로컬 어플리케이션/자체 라이브러리


and

모듈(Module) 명은 짧은 소문자로 구성되며 필요하다면 밑줄로 나눕니다.
C/C++ 확장 모듈은 밑줄로 시작합니다

**Not Good**

```python
import some
import os
import sys
import printsomething
```
**Good**

```python
import os
import sys

import mymodule
import mymodule1
```

```python
#good
import os
import sys

#Not Good
import sys, os
```

5. 하나의 라인당 하나의 모듈

**Not Good**

```python
import os,sys,somemodule
```

**Good**

```python
import os
import sys


 # and Good
from subprocess import Popen, PIPE
```
