#피보나치 수열을 위한 모듈

def fib(n): #n까지의 피보나치 수열을 출력
    a, b = 0, 1
    while b < n:
        print(b, end=' ')
        a, b = b,a+b
    print()

def fib2(n): #n까지의 피보나치 수열을 반환
        result = []
        a, b = 0, 1
        while b < n:
            result.append(b) #리스트 값 채우기
            a, b = b, a+b
        return result
