import os
class Print_class:
    
    def menu_print(self): #main Menu 구성을 보여주기 위한 함수
        print("=="*5, "POS", "=="*5)
        print("1.Add to infomation")
        print("2.Sell product")
        print("3.Balance accounts")
        print("4.Exit")
        print("=="*17)
    def add_menu_print(self):#Add product 메뉴
        os.system('cls')
        print("=="*5, "Add to information", "=="*5)
        print("1) Register Product")
        print("2) Print Product")
        print("3) Delete Product")
        print("4) Update Product")
        print("5) Back to menu")
    def sell_menu_print(self): #Sell 메뉴
        os.system('cls')
        print("=="*5, "Sell Product", "=="*5)
        print("1.Put product in cart")
        print("2.Payment")
        print("3.Back to menu")
