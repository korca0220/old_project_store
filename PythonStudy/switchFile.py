import os

class Address_Book:

    list_count =0
    list_dict = {}
    list_address = list() #lLIst형으로 저장하기 위한 클래스 변수
    def menu_print(self): # Menu 구성을 보여주기 위한 함수
        print("=="*5, "Address_book", "=="*5)
        print("1.Add to infomation")
        print("2.Delete to infomation")
        print("3.Modify to infomation")
        print("4.Pirnt Address_book")
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
    def delete_info(self, index_nuber, delete_attribute):
        del(Address_Book.list_address[index_nuber-1][delete_attribute])

if __name__=='__main__':

    book_class = Address_Book()
    while(1):
        book_class.menu_print()
        select_menu = input("select menu number : ")
        if(select_menu == "1"):
            os.system('cls')
            input_name = input("What your name : ")
            input_phone = input("What your phone_number : ")
            input_job = input("What your job : ")
            book_class.add_info(input_name, input_phone, input_job)
            print("Success!")
        elif(select_menu == "2"):
            os.system('cls')
            book_class.print_info()
        elif(select_menu == "3"):
            os.system('cls')
            input_index = int(input("select index number : "))
            input_attribute = input("select attribute : ")
            book_class(input_index, input_attribute)
