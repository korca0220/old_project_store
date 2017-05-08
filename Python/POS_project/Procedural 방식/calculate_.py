from datetime import datetime

class Calculate:

    def __init__(self, name, price, count):
        self.name = name
        self.price = price
        self.count = count
        self.year = str(datetime.today().year)
        self.month = str(datetime.today().month)
        self.day = str(datetime.today().day)
        self.today_ = self.year +"."+ self.month + "." + self.day
        self.total = 0

if __name__ == '__main__':

    banana = Calculate("Banana", "3000", 20)

    print(banana.name, banana.price, banana.count, banana.today_)
