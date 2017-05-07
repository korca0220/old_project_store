#include <iostream>
#include <time.h>
#include "lotto.h"
#include "money.h"
using namespace std;
gamemoney G2;

int lotto::mainmenu(int player)
{

	do
	{
		cout << "========== 로또 게임 선택 메뉴==========" << endl;
		cout << "1. 숫자 3개 맞추기 \t" << "소지금액 : " << G2.money(0, player - 1) << endl;
		cout << "2. 로또 시뮬레이터" << endl;
		cout << "3. 당첨금 보기" << endl;
		cout << "4. 이전메뉴로 나가기" << endl;
		cout << "\n 해당 숫자를 입력하세요." << endl;
		cout << "===================================" << endl;
		if (G2.money(0, player - 1) < 10)
		{
			system("cls");
			return 0;
		}
		if (G2.money(0, player - 1) < 1000)
		{
			system("cls");
			cout << "소지금이 부족하므로 로또게임에 참가하실수 없습니다. 메인메뉴로 돌아갑니다." << endl;
			return 0;
		}
		do
		{
			cin >> menu;
			if (menu < 1 || 4 < menu)
			{
				cout << "잘못된 값을 입력하셨습니다. 다시 입력해주세요" << endl;
			}
		} while (menu < 1 || 4 < menu); // 1보다 작거나 4보다 큰값 입력하면 계속 반복
		switch (menu)
		{
		case 1:
			do { simul3(player); } while (remenu == 2);
			break;
		case 2:
			do { simul6(player); } while (remenu == 2);
			break;
		case 3:
			chart();
			break;
		case 4:
			system("cls");
			remenu = 4;
			return remenu;
			break;
		default: // 추가메뉴 미구현
			break;
		}
	} while (remenu == 1);
	return 0;
}
void lotto::endprint()
{
	cout << endl;
	cout << "로또 게임 선택 메뉴로 돌아가시려면 1번" << endl;
	cout << "다시 도전 하시려면 2번" << endl;
	cout << "이전 메뉴로 돌아가시려면 아무숫자나 입력해주세요." << endl;
}
int lotto::simul3(int player)
{
	int usernum3[3];
	int lonum3[3];
	G2.money(-500, player - 1);
	system("cls");
	cout << "도전 비용 500 원이 차감됩니다.  잔여 소지금: " << G2.money(0, player - 1) << endl;
	cout << "1~10 까지의 숫자 3개를 차례로 입력해주세요." << endl;
	for (int i = 0; i < 3; i++)
	{
		cin >> usernum3[i]; // 배열에 숫자 3개 입력받기
	}
	system("cls");
	cout << "-------------------이번회차 당첨 번호는-------------------" << endl;  // 추후에 1회차 2회차.. 이렇게 보이게 수정.
	for (int i = 0; i < 3; i++)
	{
		lonum3[i] = rand() % 10 + 1;
		for (int j = 0; j < i; j++)
		{
			if (lonum3[j] == lonum3[i])
			{
				i--;
				break;
			}
		}
	}
	for (int i = 0; i < 3; i++) //로또 당첨 번호 출력하기
	{
		cout << lonum3[i] << "\t";
	}

	cout << "입니다." << endl;
	cout << endl;
	for (int i = 0; i < 3; i++) //내가 입력한값 일렬로 정렬해서 보여주기
	{
		cout << usernum3[i] << "\t";
	}
	count = 0; // 멤버변수 카운트 초기화
	cout << "<- 내가 선택한 번호" << endl;

	for (int i = 0; i < 3; i++)  //몇개나 일치하는지 체크
	{
		for (int j = 0; j < 3; j++)
		{
			if (usernum3[i] == lonum3[j]) //입력값과 당첨번호값 같은지 확인하고
			{
				count++;  // 같다면 카운트변수 +1 추가 (당첨번호갯수)
				break;
	cout << endl;
			}
		}
	}

	cout << "번호가 총 " << count << "개 일치. ";
	switch (count) //당첨갯수로 당첨금액 보여주는 문구 출력하기.
	{
	case 1:
		cout << "3등 입니다.  당첨금: 1,000 원" << endl;
		cout << "----------------------------------------------------------" << endl;
		G2.money(1000, player - 1);
		cout << "소지금: " << G2.money(0, player - 1) << " 원" << endl;
		cout << "----------------------------------------------------------" << endl;
		break;
	case 2:
		cout << "2등 입니다.  당첨금: 5,000 원" << endl;
		cout << "----------------------------------------------------------" << endl;
		G2.money(5000, player - 1);
		cout << "소지금: " << G2.money(0, player - 1) << " 원" << endl;
		cout << "----------------------------------------------------------" << endl;
		break;
	case 3:
		cout << "1등 입니다.  당첨금: 10,000 원" << endl;
		cout << "----------------------------------------------------------" << endl;
		G2.money(10000, player - 1);
		cout << "소지금: " << G2.money(0, player - 1) << " 원" << endl;
		cout << "----------------------------------------------------------" << endl;
		break;
	default:
		cout << "꽝. 낙첨입니다." << endl;
		cout << "----------------------------------------------------------" << endl;
		cout << "소지금: " << G2.money(0, player - 1) << " 원" << endl;
		cout << "----------------------------------------------------------" << endl;
		break;
	}

	cout << endl;
	endprint();
	cin >> remenu;
	system("cls");  // 시스템 출력화면 지우기	
	return remenu;
}
int lotto::simul6(int player)
{
	int usernum6[6];
	int lonum6[7]; // 본게임에는 보너스번호때문에 하나추가
	G2.money(-1000, player - 1);
	system("cls");
	cout << "도전 비용 1000 원이 차감됩니다.  잔여 소지금: " << G2.money(0, player - 1) << endl;
	cout << "1~45 까지의 숫자 6개를 차례로 입력해주세요." << endl;
	for (int i = 0; i < 6; i++) // 1-1. 입력은 6개를 받고,
	{
		cin >> usernum6[i]; // 배열에 숫자 3개 입력받기
	}
	system("cls");
	cout << "-------------------이번회차 당첨 번호는-------------------" << endl;  // 추후에 1회차 2회차.. 이렇게 보이게 수정.
	for (int i = 0; i < 7; i++) // 1-2. 생성은 보너스 번호까지 7개를 해둔다.
	{
		lonum6[i] = rand() % 45 + 1;
		for (int j = 0; j < i; j++)
		{
			if (lonum6[j] == lonum6[i])
			{
				i--;
				break;
			}
		}
	}
	for (int i = 0; i < 6; i++) //로또 당첨 번호 출력하기
	{
		cout << lonum6[i] << "\t";
	}

	cout << "입니다." << endl;
	cout << "2등 보너스 번호는 " << lonum6[6] << " 입니다." << endl; //보너스번호 따로출력
	cout << endl;
	for (int i = 0; i < 6; i++) //내가 입력한값 일렬로 정렬해서 보여주기
	{
		cout << usernum6[i] << "\t";
	}
	count = 0; // 멤버변수 카운트 초기화
	cout << "<- 내가 선택한 번호" << endl;
	for (int i = 0; i < 6; i++)  //몇개나 일치하는지 체크
	{
		for (int j = 0; j < 6; j++)
		{
			if (usernum6[i] == lonum6[j]) //입력값과 당첨번호값 같은지 확인하고
			{
				count++;  // 같다면 카운트변수 +1 추가 (당첨번호갯수)
				break;
			}
		}
	}
	cout << endl;
	cout << "번호가 총 " << count << "개 일치. ";
	bonusnum = 0;//보너스번호일치여부 초기화
	if (count == 5) //보너스번호 일치하면 1로 바꿔주기
	{
		for (int i = 0; i < 6; i++)
		{
			if (usernum6[i] == lonum6[7])
				bonusnum = 1;
			else
				bonusnum = 0;
		}
	}

	switch (count) //당첨갯수로 당첨금액 보여주는 문구 출력하기.
	{
	case 3:
		cout << "5등 입니다.  당첨금: 5,000 원" << endl;
		cout << "----------------------------------------------------------" << endl;
		G2.money(5000, player - 1);
		cout << "소지금: " << G2.money(0, player - 1) << " 원" << endl;
		cout << "----------------------------------------------------------" << endl;
		break;
	case 4:
		cout << "4등 입니다.  당첨금: 50,000 원" << endl;
		cout << "----------------------------------------------------------" << endl;
		G2.money(50000, player - 1);
		cout << "소지금: " << G2.money(0, player - 1) << " 원" << endl;
		cout << "----------------------------------------------------------" << endl;
		break;
	case 5:
		if (bonusnum == 1)
		{
			cout << "2등 입니다.  당첨금: 40,000,000 원" << endl;
			cout << "----------------------------------------------------------" << endl;
			G2.money(40000000, player - 1);
			cout << "소지금: " << G2.money(0, player - 1) << " 원" << endl;
			cout << "----------------------------------------------------------" << endl;
			break;
		}
		else
		{
			cout << "3등 입니다.  당첨금: 1,000,000 원" << endl;
			cout << "----------------------------------------------------------" << endl;
			G2.money(1000000, player - 1);
			cout << "소지금: " << G2.money(0, player - 1) << " 원" << endl;
			cout << "----------------------------------------------------------" << endl;
			break;
		}
	case 6:
		cout << "1등 입니다.  당첨금: 2,000,000,000 원" << endl;
		cout << "----------------------------------------------------------" << endl;
		G2.money(2000000000, player - 1);
		cout << "소지금: " << G2.money(0, player - 1) << " 원" << endl;
		cout << "----------------------------------------------------------" << endl;
		break;
	default:
		cout << "꽝. 낙첨입니다." << endl;
		cout << "----------------------------------------------------------" << endl;
		cout << "소지금: " << G2.money(0, player - 1) << " 원" << endl;
		cout << "----------------------------------------------------------" << endl;
		break;
	}
	cout << endl;
	endprint();
	cin >> remenu;
	system("cls");  // 시스템 출력화면 지우기
	return remenu;
}
int lotto::chart()
{
	system("cls");
	cout << "-----당첨 금액-----" << endl;
	cout << "3개 숫자 맞추기" << endl;
	cout << "1등 10,000 원" << endl;
	cout << "2등 5,000 원" << endl;
	cout << "3등 1,000 원" << endl;
	cout << "-------------------" << endl;
	cout << "로또 시뮬" << endl;
	cout << "1등 2,000,000,000 원" << endl;
	cout << "2등 40,000,000 원" << endl;
	cout << "3등 1,000,000 원" << endl;
	cout << "4등 50,000 원" << endl;
	cout << "5등 5,000 원" << endl;
	cout << endl;
	cout << "-------------------" << endl;
	cout << "메뉴로 돌아가시려면 아무숫자나 입력해주세요." << endl;
	cin >> remenu;
	system("cls");  // 시스템 출력화면 지우기
	return 0;
}
