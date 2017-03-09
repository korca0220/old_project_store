import os

class Address_Book:

    list_count =0
    list_dict = {}
    list_address = list() #lLIst형으로 저장하기 위한 클래스 변수
    def menu_print(self): # Menu 구성을 보여주기 위한 함수
        print("=="*5, "Address_book", "=="*5)
        print("1.Add to infomation")
        print("2.Print to infomation")
        print("3.Delete to infomation")
        print("4.Modify to Address_book")
        print("5.Exit")
        print("=="*17)

    def add_info(self, name, phone, job): #주소록 목록을 추가하는 함수
        self.name = name
        self.phone = phone
        self.job = job
        Address_Book.list_count += 1
        Address_Book.list_dict = {'index':Address_Book.list_count, 'name': name, 'phone':phone, 'job':job} #한 명(하나의 정보)의 정보를 저장하는 자료형
        Address_Book.list_address.append(Address_Book.list_dict) #자료형을 list형으로 나열

    def print_info(self): #현재까지 저장된 주소록 출력
        for i in Address_Book.list_address:
            print(i)
    def delete_info(self, index_number): #리스트 삭제
        del Address_Book.list_address[index_number-1]
    #def modify_info(self, index_number, select_attribute):

    # def update_info(self):
    # def search_info(self):
