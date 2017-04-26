import test_class

class Test2:

    def __init__(self):
        pass
    def print_test(self, Test1):
        Test1.print_product("EEE")

if __name__ == '__main__':

    test1_class = test_class.Test1()
    test2_class = Test2()

    test2_class.print_test(test1_class)
