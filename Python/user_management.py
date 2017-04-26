import test_pakage.user_password as upr  #user_password 모듈 탑재ㅐ

#사용자 클래스 정의
class User:
    #초기화 함수 재정의
    def __init__(self, pwd):
        self.pwd = pwd
        self.check_validation() #입력한 비밀 번호 검증

    #정합성 검증 함수 호출을 통한 비밀번호 적합성 검증

    def check_validation(self):
        upr.password_validation_check(self.pwd)

    def name_test(self):
        print(__name__)
if __name__=='__main__':
    user1= User('3jkMf8Exe')
    print('='*10)
    user2= User('eee')
    print('='*10)
    user3= User('3#kMEx90e')
    user3.name_test()
