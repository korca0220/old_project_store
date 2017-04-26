class test_:
    def __init__(self, number1, number2):
        self.number1 = number1
        self.number2 = number2
        self.test_function(number1, number2)

    def test_function(self, one, two):
        print(one+two)
        test_function2(one, two)

def test_function2(one, two):
    print(one*two)

if __name__=='__main__':
    test = test_(3,4)
