import common_


class Sell:
    common_class = common_.Common()
    product_sell_count = 1
    sell_dict = {'product_name':'', 'product_price':'', 'product_sell_count':0}
    sell_list_product = [sell_dict]
    def into_cart(self): #카트 목록을 보여주는 함수
        for i in common_class.list_product:
            print(i)
        while(1):
            select_product = int(input("Select product index('0'key is exit) : "))
            if(select_product == 0):
                break

            Sell.sell_dict = {'product_name':common_class.list_product[select_product-1]['product_name'],
                              'product_price':common_class.list_product[select_product-1]['product_price'],
                              'product_sell_count':Sell.product_sell_count}

            count = 0
            check = True
            for j in Sell.sell_list_product:
                count = count + 1
                if(j['product_name'] == Sell.sell_dict['product_name']):
                    Sell.sell_list_product[count-1]['product_sell_count']+=1
                    check = True
                    break
                else:
                    check = False
            if(check == False):
                print("test")
                Sell.sell_list_product.append(Sell.sell_dict)

    def total_cart(self):
        for i in Sell.sell_list_product:
            print(i)
        del i


# if __name__ == '__main__':
