# -*- coding: utf-8 -*-
#비밀번호 정합성 체크를 위한 함수
def password_validation_check(pwd):
    f = open("D:/Storage/Study/Python/Text/password.txt", 'a') # file open
    """ checking password validation

    Args:
        pwd (str) : password string

    return :
        True or False (boolean) : the result of checking validation
    """

    #비밀번호 길이 확인(6~12)
    if len(pwd) < 6 or len(pwd) > 12:
        print(pwd, 'is length false_value.')
        p_file = "%s is length false_value. \n" % pwd #file에 들어갈 문자열 변수
        f.write(p_file) #file.write를 이용하여 p_file 변수 삽입.
        return False

    #숫자 혹은 알파벳 유무 확인
    for c in pwd:
        if not c.isnumeric() and not c.isalpha() :
            print(pwd, 'is not numeric and alphabat false_value.')
            p_file = "%s is not numberic and alphabat false_value \n" % pwd
            f.write(p_file)
            return False

    #알파벳 대소문자 확인
    upper = False #대문자 포함 유무를 위한 논리형 변수
    lower = False #소문자 포함 유무를 위한 논리형 변수

    #각 문자 확인
    for c in pwd:
        #대문자와 소문자가 모두 있으면 루프 탈출
        if upper and lower:
            break

        #해당 문자가 영문이면
        if c.isalpha():

            #아직 대문자가 발견 되지 않은 경우에만
            if not upper:
                upper = c.isupper() #대문자 포함 유무 저장

            #아직 소문자가 발견 되지 않은 경우에만
            if not lower:
                lower = c.islower() #소문자 포함 유무 저장

    #대문자 혹은 소문자가 없는 경우
    if not upper or not lower:
        print(pwd, 'is not exist upper and lower false_value.')
        p_file = "%s is not exist upper and lower false_value \n" % pwd
        f.write(p_file)
        return False


    print(pwd, 'is right password true_value')
    p_file = "%s is right password true_value \n" % pwd
    f.write(p_file)
    f.close()
    return True

# if __name__=='__main__':
#     password_validation_check('23jke') #False, 길이 오류
#     password_validation_check('432rewvb53') #False, 대문자 부재
#     password_validation_check('203jke%') #False, 기호 포함
#     password_validation_check('3k39QLe6oO') #True
