import product_, print_, sell_
import os
if __name__=='__main__':

    product_class = product_.Product()
    print_class = print_.Print_class()
    sell_class = sell_.Sell()
    while(1):
        os.system('cls')
        print_class.menu_print()
        select_menu = input("select POS menu : ")
        if(select_menu == "1"):
            while(select_menu !="5"):
                print_class.add_menu_print()
                select_detail = input("select Register-detail : ")
                if(select_detail=="1"):
                    os.system('cls')
                    product_name = input("Product name : ")
                    product_price = int(input("Set to product price :"))
                    product_class.add_info(product_name, product_price)
                elif(select_detail== "2"):
                    os.system('cls')
                    product_class.print_info()
                    os.system('pause')
                elif(select_detail == "3"):
                    select_index = int(input("select delete index : "))
                    product_class.delete_info(select_index)
                elif(select_detail == "4"):
                    os.system('cls')
                    product_class.update_info()
                    print("Updated Proudct list!! ")
                    os.system('pause')
                elif(select_detail == "5"):
                    break
        elif(select_menu == "2"):
            os.system('cls')
            while(1):
                print_class.sell_menu_print()
                select_sell = input("Select Sell menu :")
                if(select_sell == "1"):
                    sell_class.into_cart()
        elif(select_menu == "3"):
            pass
        elif(select_menu == "4"):
            break
