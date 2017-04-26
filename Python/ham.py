import random

print("안녕하세요")
print("(인터페이스 기술과 실험)")
print("프로그램 실행...\n")

while 1:
    age=int(input("당신의 나이는 몇살입니까?"))
    gender=int(input("성별은 무엇입니까?(남자:0, 여자:1 입력)\n"))

    if gender==0 and (age>=20 and age<=25):
        ans0=int(input("미필이면 0, 군필이면 1 입력\n"))

        if ans0==0:
            print("에휴...\n")

        else:
            print("승리자\n")

    elif gender==1 and (age>=20 and age<26):
        print("여대생\n")

    elif (gender==0 or gender==1) and age<20:
        print("공부 열심히 해라\n")

    elif (gender==0 or gender==1) and (age>25 and age<31):
        print("사회 초년생\n")

    elif (gender==0 or gender==1) and (age>30 and age<50):
        print("부자 되세요\n")

    else:
        print("...")

    ans0=int(input("지금 단계를 반복하려면 0, 다음단계로 가려면 1을 입력하세요:"))

    if ans0==0:
        continue

    else:
        break

print("구구단 프로그램\n")

for i in range(1,10):
    print("2 X",i,"=",2*i)

for i in range(1,10):
    print("3 X",i,"=",3*i)

for i in range(1,10):
    print("4 X",i,"=",4*i)

for i in range(1,10):
    print("5 X",i,"=",5*i)

for i in range(1,10):
    print("6 X",i,"=",6*i)

for i in range(1,10):
    print("7 X",i,"=",7*i)

for i in range(1,10):
    print("8 X",i,"=",8*i)

for i in range(1,10):
    print("9 X",i,"=",9*i)

print("\n")
print("2중 for문으로 다시 코딩하면\n")

for i in range(2,10):
    for j in range(1,10):
        print(i,"X",j,"=",i*j)

print("\n")

def Arr(n):
    print("리스트와 함수연습...")

    arr=list()
    for i in range(0,n):
        arr.append(random.randint(0,100))

    r=int(input("0~n까지의 리스트 중 확인하고 싶은 배열을 입력하세요:"))

    print(arr[r])



if __name__ == '__main__':

    n=int(input("0~n의 리스트 중 정수 n값을 입력하세요..."))
    Arr(n)
