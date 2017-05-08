import os

class Product:


        list_count =0 #인덱스 카운터
        list_dict ={} #상품목록 dict
        list_product = list()#상품목록 dict를 담을 list
        def add_info(self, name, price): #주소록 목록을 추가하는 함수
            self.product_name = name
            self.product_price = price
            Product.list_count += 1 #인덱스 1씩 증가
            Product.list_dict = {'index':Product.list_count, 'product_name': name, 'product_price':price} #한 명(하나의 정보)의 정보를 저장하는 자료형
            Product.list_product.append(Product.list_dict) #자료형을 list형으로 나열

        def print_info(self): #현재까지 저장된 주소록 출력
            for i in Product.list_product:
                 print(i)

        def delete_info(self, index_number): #리스트 삭제
            del Product.list_product[index_number-1]

        def update_info(self):#인덱스 재 정렬
            Product.list_count =0
            temp_list = Product.list_product #임시 리스트
            Product.list_product= list() #리스트 초기화
            for i in temp_list: #초기화 이후 인덱스를 이용해 재정렬
                self.product_name = i['product_name']
                self.product_price = i['product_price']
                Product.list_count += 1
                Product.list_dict = {'index':Product.list_count, 'product_name': self.product_name, 'product_price': self.product_price}
                Product.list_product.append(Product.list_dict)
