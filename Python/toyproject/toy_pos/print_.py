import os
import sys
import common_

common_class = common_.Common()
class PrintMenu:

    @staticmethod
    def print_menu():
        print("==" * 5, "POS", "==" * 5)
        print("1.Add to infomation")
        print("2.Sell product")
        print("3.Balance accounts")
        print("4.Exit")
        print("==" * 17)

    @staticmethod
    def print_add_menu():
        common_class.platformFunction()
        print("==" * 5, "Add to information", "==" * 5)
        print("1) Register Product")
        print("2) Print Product")
        print("3) Delete Product")
        print("4) Update Product")
        print("5) Back to menu")

    @staticmethod
    def print_sell_menu():
        common_class.platformFunction()
        print("==" * 5, "Sell Product", "==" * 5)
        print("1.Put product in cart")
        print("2.Payment")
        print("3.Back to menu")


if __name__ == "__main__":
    samplePrint = PrintMenu()
