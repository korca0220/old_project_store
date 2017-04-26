
from datetime import datetime

class Calculate:

    product = None
    year = None
    month = None
    day = None

    def __init__(self,Product):
        self.product = Product
        self.year = datetime.today().year
        self.month = datetime.today().month
        self.day = datetime.today().day






if __name__ == "__main__":
    calculate = Calculate(Product= None)


    print("%d년 %d월 %d일" % (calculate.year,calculate.month,calculate.day))