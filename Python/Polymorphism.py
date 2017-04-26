# 다형성 구현을 위한 소스
"""
   Polymorphism ->
   부모클래스와 동일한 이림의 메소드를 그대로 자식 클래스에서 구현하여 재정의 하는 것을 의미
"""

class Developer: #부모 클래스
    def __init__(self, name): #생성자
        self.name = name
    def coding(self) : #coding 메소드
        print(self.name + ' is developer!!')

class PythonDeveloper(Developer): #PythonDeveloper 자식 클래스
    def coding(self): #coding 메소드를 재정의(overriding)
        print(self.name + ' is Python developer!!')

class JavaDeveloper(Developer): # JavaDeveloper 자식 클래스
    def coding(self):
        print(self.name + ' is Java developer!!')

class CPPDeveloper(Developer): # CPPDeveloper 자식 클래스
    def coding(self):
        #super().coding() #부모 인스턴스의 coding()함수 호출
        print(self.name + ' is C++ developer!!')

pd = PythonDeveloper('June')
jd = JavaDeveloper('Jan')
cd = CPPDeveloper('Jon')
pd.coding()
jd.coding()
cd.coding()
