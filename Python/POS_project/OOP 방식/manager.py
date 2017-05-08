from product import Product
from calculate import Calculate
from sell_product import Sell


class Manager:
    _product = None
    _calculate = None
    _products = dict()
    _sell = None


    def __init__(self):
        self._sell = Sell()

    # 기능 : 단순히 product를 추가하는 기능
    def append_product(self, name: str, price: int, count: int):

        #_prdocuts = {'name':{value, value2,...}}
        if name in self._products:
            print('fail: ' + name)
        else:
            print('success: ' + name)
            #_products = {'name':{value={'name':name, 'price':price, 'count':count},...value2}}
            self._products[name] = Product(name=name,
                                           price=price,
                                           count=count)

    # 기능 : 모든 products 딕셔너리 요소를 하나하나를 출력
    def print_all_product(self):

        #key = _products = {'name':{value}}
        #value = _products = {'name':{value:{'name':...'price':,,}}}
        for key, value in self._products.items():
            print(key, ':', 'Price :', value.price, 'Count :', value.count)

    # 기능 : 해당 product의 count를 증가 (제품 발주)
    def increase_product_count(self, name: str, many: int):

        if name in self._products: #name값이 _products의 key값으로 있어야함
            self._products[name].count += many # value인 count에 many로 들어온 만큼 추가
            print('success: %s - 현재 잔량 %d' % (name, self._products[name].count))
        else:
            return 'fail'

    def sell_product(self, name: str, how_many: int):

        result = self._sell.sell_product(product=self._products[name], how_many=how_many) #True or False
        current_count = self._products[name].count

        #x if a > b else y    파이썬에서의 3항연산 데이터베이스의 트렌젝션 기능
        # result값이 True면 앞에 값(current_count - how_many), False 면 뒤에 값(current_count)
        self._products[name].count =\
                            current_count - how_many if result else current_count


    def print_all_detail_calculates(self):
        self._sell.print_all_calculate()



if __name__ == '__main__':
    manager = Manager()

    # append
    manager.append_product('banana', 1000, 30)
    manager.append_product('banana', 1000, 30)
    manager.append_product('apple', 1000, 40)
    manager.append_product('py', 2000, 100)

    # increase
    manager.increase_product_count(name='apple', many=10)
    manager.increase_product_count(name='banana', many=20)
    manager.increase_product_count(name='py', many=10)

    # sell
    # how_many = 0으로 놓는 순간 정상동작 .. 추후 해결
    manager.sell_product(name='banana', how_many=10)
    manager.sell_product(name='py', how_many=0)
    manager.sell_product(name='py', how_many=10)

    manager.print_all_detail_calculates()
