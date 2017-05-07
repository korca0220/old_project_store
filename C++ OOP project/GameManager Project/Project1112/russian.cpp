#include <iostream>
#include <time.h>
#include <math.h>
#include "money.h"
#include "russian.h"
using namespace std;

void rus::end()
{
	cout << "다시 도전 하시려면 2번" << endl;
	cout << "이전 메뉴로 돌아가시려면 아무숫자나 입력해주세요" << endl;
}

int rus::russian(int player)
{
	gamemoney G;
	system("cls");
	int i = 0;
	char enter;
	srand((unsigned)time(0));
	if (G.money(0, player - 1) < 1000)
	{
		return 0;
	}
	cout << "러시안 룰렛 게임을 시작합니다.\n동전을 던져 선을 정합니다.\n엔터를 누르면 방아쇠를 당깁니다.\n\n";
	cout << "높은 연승을 달성할수록 많은 돈을 얻습니다." << endl;
	cout << "죽을 경우 베팅한 돈을 잃게 됩니다." << endl << endl;
Re1:
	if (G.money(0, player - 1) == 0)
	{
		while ((enter = getchar()) != '\n');
		cout << "소지금이 0원이면 게임을 할 수 없습니다. 메인메뉴로 돌아갑니다.";
		while ((enter = getchar()) != '\n');
		system("cls");
		return 0;
	}
	Score = 0;
	cout << "소지금 : " << G.money(0, player - 1) << endl;
	cout << "베팅할 금액 : ";
	do {
		cin >> bet;
		if (bet > G.money(0, player - 1))
			cout << "소지금이 부족합니다" << endl;
	} while (bet > G.money(0, player - 1));
	G.money(0 - bet, player - 1);
	cout << endl;
Re2:
	Coin = rand() % 2 + 1;
	Bullet = rand() % 6;
	cout << "동전의 어느 면을 선택하시겠습니까?(앞=1, 뒤=2)\n";
	cin >> Select;

	if (Select == 1)
	{
		if (Coin == 1)
		{
			while ((enter = getchar()) != '\n');
			cout << "앞면이 나왔습니다.\n\n";
			while ((enter = getchar()) != '\n');
			system("cls");
			for (i = 0; i <= 5; i++)
			{
				cout << i + 1 << "번째 차례\n";
				if ((i % 2) == 0)
					cout << "당신의 차례입니다. 방아쇠를 당기십시오.\n";
				else
					cout << "제 차례입니다. 방아쇠를 당기겠습니다.\n";
				while ((enter = getchar()) != '\n');

				if (i == Bullet)
				{
					cout << "총성이 울려퍼집니다.\n\n";
					if ((i % 2) == 0)
					{
						cout << "당신은 죽었습니다.\n\n";
						//cout << Score << "연승하셨습니다.\n\n";
						end();
						cin >> Select;
						if (Select == 2)
						{
							cout << "다음 게임을 시작합니다.\n";
							system("cls");
							goto Re1;
						}
						system("cls");
						return 0;
					}
					else
					{
						cout << "당신은 승리했습니다.\n\n";
						Score++;
						cout << Score << "연승 중\n";
						cout << bet * pow(2, Score) << "원을 받을 수 있습니다." << endl;
						end();
						cin >> Select;
						if (Select == 2)
						{
							cout << "다음 게임을 시작합니다.\n";
							system("cls");
							goto Re2;
						}
						G.money(bet * pow(2, Score), player - 1);
						system("cls");
						return 0;
					}

				}
				else
				{
					cout << "아무일도 일어나지 않았습니다.\n\n";
					while ((enter = getchar()) != '\n');
					system("cls");
				}
			}
		}
		else
		{
			while ((enter = getchar()) != '\n');
			cout << "뒷면이 나왔습니다.\n\n";
			while ((enter = getchar()) != '\n');
			system("cls");
			for (i = 0; i <= 5; i++)
			{
				cout << i + 1 << "번째 결과\n";
				if ((i % 2) == 0)
					cout << "제 차례입니다. 방아쇠를 당기겠습니다.\n";
				else
					cout << "당신의 차례입니다. 방아쇠를 당기십시오.\n";
				while ((enter = getchar()) != '\n');

				if (i == Bullet)
				{
					cout << "총성이 울려퍼집니다.\n\n";
					if ((i % 2) == 0)
					{
						cout << "당신은 승리했습니다.\n\n";
						Score++;
						cout << Score << "연승 중\n";
						cout << bet * pow(2, Score) << "원을 받을 수 있습니다." << endl;
						end();
						cin >> Select;
						if (Select == 2)
						{
							cout << "다음 게임을 시작합니다.\n";
							system("cls");
							goto Re2;

						}
						G.money(bet * pow(2, Score), player - 1);
						system("cls");
						return 0;
					}
					else
					{
						cout << "당신은 죽었습니다.\n\n";
						//cout << Score << "연승하셨습니다.\n";
						end();
						cin >> Select;
						if (Select == 2)
						{
							cout << "다음 게임을 시작합니다.\n";
							system("cls");
							goto Re1;
						}
						system("cls");
						return 0;
					}
				}
				else
				{
					cout << "아무일도 일어나지 않았습니다.\n\n";
					while ((enter = getchar()) != '\n');
					system("cls");
				}
			}
		}

	}
	else if (Select == 2)
	{
		if (Coin == 1)
		{
			while ((enter = getchar()) != '\n');
			cout << "앞면이 나왔습니다.\n\n";
			while ((enter = getchar()) != '\n');
			system("cls");
			for (i = 0; i <= 5; i++)
			{
				cout << i + 1 << "번째 결과\n";
				if ((i % 2) == 0)
					cout << "제 차례입니다. 방아쇠를 당기겠습니다.\n";
				else
					cout << "당신의 차례입니다. 방아쇠를 당기십시오.\n";
				while ((enter = getchar()) != '\n');

				if (i == Bullet)
				{
					cout << "총성이 울려퍼집니다.\n\n";
					if ((i % 2) == 0)
					{
						cout << "당신은 승리했습니다.\n\n";
						Score++;
						cout << Score << "연승 중\n";
						cout << bet * pow(2, Score) << "원을 받을 수 있습니다." << endl;
						end();
						cin >> Select;
						if (Select == 2)
						{
							cout << "다음 게임을 시작합니다.\n";
							system("cls");
							goto Re2;
						}
						G.money(bet * pow(2, Score), player - 1);
						system("cls");
						return 0;
					}
					else
					{
						cout << "당신은 죽었습니다.\n\n";
						//cout << Score << "연승하셨습니다.\n";
						end();
						cin >> Select;
						if (Select == 2)
						{
							cout << "다음 게임을 시작합니다.\n";
							system("cls");
							goto Re1;

						}
						system("cls");
						return 0;
					}
				}
				else
				{
					cout << "아무일도 일어나지 않았습니다.\n\n";
					while ((enter = getchar()) != '\n');
					system("cls");
				}
			}
		}
		else
		{
			while ((enter = getchar()) != '\n');
			cout << "뒷면이 나왔습니다.\n\n";
			while ((enter = getchar()) != '\n');
			system("cls");
			for (i = 0; i <= 5; i++)
			{
				cout << i + 1 << "번째 결과\n";
				if ((i % 2) == 0)
					cout << "당신의 차례입니다. 방아쇠를 당기십시오.\n";
				else
					cout << "제 차례입니다. 방아쇠를 당기겠습니다.\n";
				while ((enter = getchar()) != '\n');

				if (i == Bullet)
				{
					cout << "총성이 울려퍼집니다.\n\n";
					if ((i % 2) == 0)
					{
						cout << "당신은 죽었습니다.\n\n";
						//	cout << Score << "연승하셨습니다.\n\n";
						end();
						cin >> Select;
						if (Select == 2)
						{
							cout << "다음 게임을 시작합니다.\n";
							system("cls");
							goto Re1;
						}
						system("cls");
						return 0;
					}
					else
					{
						cout << "당신은 승리했습니다.\n\n";
						Score++;
						cout << Score << "연승 중\n";
						cout << bet * pow(2, Score) << "원을 받을 수 있습니다." << endl;
						end();
						cin >> Select;
						if (Select == 2)
						{
							cout << "다음 게임을 시작합니다.\n";
							system("cls");
							goto Re2;
						}
						G.money(bet * pow(2, Score), player - 1);
						system("cls");
						return 0;
					}
				}
				else
				{
					cout << "아무일도 일어나지 않았습니다.\n\n";
					while ((enter = getchar()) != '\n');
					system("cls");
				}
			}
		}
	}
	else
	{
		printf("다시 입력하십시오.\n");
		goto Re2;
	}
	return 0;
}