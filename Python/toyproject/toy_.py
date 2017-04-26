import switchFile as sw #switchFile 모듈을 'sw'라고 재정의
import os #system 함수를 이용하기 위한 os 모듈 import
if __name__=='__main__':

    book_class = sw.Address_Book() #book_class 라는 객체 생성
    while(1): #5가 선택되지 않는 인상 무한 반복
        book_class.menu_print() #선택지를 보여주는 함수
        select_menu = input("select menu number : ")
        if(select_menu == "1"):
            os.system('cls') #현재 창을 clear
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
            book_class.delete_info(input_index)
        elif(select_menu == "5"):
            break
