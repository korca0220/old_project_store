#include <iostream>
#include "firstmenu.h"
using namespace std;
int main()
{
	firstmenu *in = new firstmenu(); 
	int gameselect = 0;
	int selectplayer = 0;
	while (1)
	{
		gameselect = in->mainmenu();	//--------------------- 실행순서 1 : 멤버참조. mainmenu()함수가 제일먼저 실행되고 고른 메뉴값(게임)을 가지고 반환한다.  종료는 0 값. [프로그램을 종료할때까지 반복.]
		if (gameselect == 0) return 0;
		do 
		{
			selectplayer = in->personselect(); //-------------- 실행순서 2 : 사람(객체)를 생성, 선택한 사람의 배열번호반환
			if (selectplayer == 0) break;
			in->gamestartmenu(gameselect, selectplayer); //---- 실행순서 3 : 선택한 게임 번호와 사람의 배열번호를 가지고 게임을 실행시킨다. [해당 게임을 종료하고자 할때까지 반복.]
			system("cls");
		} while (!selectplayer == 0);
	}
	delete in;
	return 0;
}

