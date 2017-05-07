#include "gawi.h"
#include "money.h"
#include <iostream>
#include <time.h>
#include <stdlib.h>
#include <conio.h>
using namespace std;
gamemoney GM;

void gawi::gawiPrint(int pp) //가위바위보 메뉴 출력
{
	cout << "[[ 소지금액 : " << GM.money(0, pp - 1) << " ]]" << endl;
	cout << "     당신은 ★ " << count << " ★ 연승중!" << endl;
	cout << " 500원이 차감 됩니다! 연승시 제곱수!!" << endl;
	cout << "┌───────────────────┐" << endl;
	cout << "│(1) 가위                              │" << endl;
	cout << "│(2) 바위                              │" << endl;
	cout << "│(3) 보                                │" << endl;
	cout << "│(4) 돈으로 환산하기                   │" << endl;
	cout << "│(5) 메인메뉴 복귀                    │" << endl;
	cout << "│가위, 바위, 보 중 숫자를 입력하세요!! │" << endl;
	cout << "└───────────────────┘" << endl;
}
int gawi::money(int a, int b) //가위바위보 게임에서 돈의 흐름
{
	int i, c;
	c = a;
	for (i = 0; i<b - 1; i++)
		c = c*a;

	return c;
}
int gawi::run(int p) //실제 게임 진행
{
	count = 0;
	if (GM.money(0, p - 1) < 1000)
	{
		return 0;
	}
	while (1)
	{
	GAWI: //goto 분기점
		gawiPrint(p);
		srand((unsigned)time(NULL)); //랜덤변수 이용

		cin >> user;
		if (GM.money(0, p - 1) < 1000) //소지금 체크
		{
			system("cls");
			cout << "소지금이 부족하므로 게임에 참가하실수 없습니다. 메인메뉴로 돌아갑니다." << endl;
			cout << "Press any key to continue";
			_getch();
			system("cls");
			return 0;
		}
		switch (user) //가위바위보 게임에 대한 경우의 수를 이용
		{
		case 1:
			GM.money(-500, p - 1);
			cout << "가위";
			break;
		case 2:
			GM.money(-500, p - 1);
			cout << "바위";
			break;
		case 3:
			GM.money(-500, p - 1);
			cout << "보";
			break;
		case 4: //게임 승수에 대한 환전 
			if (count == 1)
			{
				GM.money(500, p - 1);
				realMoney = +500;
			}
			else
			{
				realMoney = money(50, count);
				GM.money(realMoney, p - 1);
			}
			count = 0;
			cout << realMoney << "원이 환산되었습니다!!" << endl;
			_getch();
			system("cls");
			goto GAWI;
			break;
		case 5:
			system("cls");
			return GM.money(0, p - 1);
		}
		cout << "\n컴퓨터:";

		com = (rand() % 3) + 1;
		switch (com) //컴퓨터는 가위,바위,보 셋중에 랜덤으로 하나를 내게 됨
		{
		case 1:
			cout << "가위";
			break;
		case 2:
			cout << "바위";
			break;
		case 3:
			cout << "보";
			break;
		}
		cout << endl;

		if (com == user) // 컴퓨터와 유저를 비교, 승패 체크
		{
			cout << "Draw game" << endl;
		}
		else if (com == 1 && user == 2)
		{
			cout << "Win!" << endl;
			count++;
		}
		else if (com == 1 && user == 3)
		{
			cout << "Lose.." << endl;
			count = 0;
		}
		else if (com == 2 && user == 1)
		{
			cout << "Lose.." << endl;
			count = 0;
		}
		else if (com == 2 && user == 3)
		{
			cout << "Win!" << endl;
			count++;
		}
		else if (com == 3 && user == 1)
		{
			cout << "Win!" << endl;
			count++;
		}
		else if (com == 3 && user == 2)
		{
			cout << "Lose.." << endl;
			count = 0;
		}
		cout << endl;
		cout << "Press enter key to continue";
		enter = _getch();
		if (enter == 13)
		{
			system("cls");
			goto GAWI;
		}
		system("cls");
	}
}