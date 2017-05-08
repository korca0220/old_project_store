# -*- coding: utf-8 -*-
import os

import manager
import common_
import print_

if __name__=='__main__':

    common_class = common_.Common()
    print_class = print_.PrintMenu()
    manager_class = manager.Manager()

    while(1):
        common_class.platformFunction()
        print_class.print_menu()
        select_menu = input("select POS menu : ")

        if(select_menu == "1"): #product 메뉴
            while(select_menu !="5"):
                print_class.print_add_menu()
                select_detail = input("select Register-detail : ")
                if(select_detail=="1"):
                    common_class.platformFunction()
                    product_name = input("Product name : ")
                    product_price = input("Set product price :")
                    product_count = int(input("Set product count :"))
                    manager_class.append_product(product_name, product_price, product_count)
                elif(select_detail== "2"):
                    common_class.platformFunction()
                    manager_class.print_all_product()
                    os.system('pause')
                elif(select_detail == "3"):
                    pass
                elif(select_detail == "4"):
                    pass
                elif(select_detail == "5"):
                    break
        elif(select_menu == "2"): #sell 메뉴
            pass
        elif(select_menu == "3"):
            pass
        else:
            break
