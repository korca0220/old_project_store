import common_

common_class = common_.Common()
class Sell:

    def into_cart(self): #카트 목록을 보여주는 함수
        for i in common_class.list_product:
            print(i)
    #def sell_product():
