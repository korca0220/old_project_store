from datetime import datetime
from product import Product
from calculate import Calculate


"""
개인적으로 calculate는 sell 즉 판매 쪽과 연관이 있으므로
sell클래스 내부의 프로퍼티로 관리하는 방향으로 바꿔봄
"""

class Sell:

    _calculate = None

    def __init__(self):
        self._calculate = Calculate()

    #product 에는 _products의 key값 즉, name갑이 들어간다
    def sell_product(self, product: Product, how_many: int):

        check_how = str(how_many).isdigit()
        if check_how == True:
            count = product.count #각 key값이 갖고잇는 value(count)의 값을 대입
            if count >= how_many: #갖고 있는 값이 요구하는 값보다 크면
                time = datetime.today().strftime("%Y.%m.%d %H:%M:%S") #strftime(format) => string data로 만듬.
                self._calculate.save_data(product.name, how_many, time)
                return True
            else:
                return False
        else:
            print("Invalid input how_many")
            pass



    def print_all_calculate(self):
        self._calculate.all_calculates()
