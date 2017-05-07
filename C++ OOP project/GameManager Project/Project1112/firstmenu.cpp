#include <iostream>
#include <string>
#include "firstmenu.h"
#include "money.h"
#include "lotto.h"
#include "russian.h"
#include "gawi.h"
using namespace std;
gamemoney G;
lotto L;
rus R;
gawi W;

// 실행순서 1-1.
int firstmenu::mainmenu()  // 1-1. 메뉴를 띄워준다.
{
	checkfirstgame = 0;
	while(1)
	{
		int gameselect = 0;
		cout << "┌── 게임 1 ──┐┌── 게임 2 ──┐┌── 게임 3 ──┐" << endl;
		cout << "│                ││                ││                │" << endl;
		cout << "│    로또게임    ││   러시안룰렛   ││   가위바위보   │" << endl;
		cout << "│                ││                ││                │" << endl;
		cout << "└────────┘└────────┘└────────┘" << endl;
		cout << "=============================================================" << endl;
		cout << "   게임을 선택 해주세요. [ 종료하시려면 4 번을 입력하세요. ] " << endl;
		cout << "=============================================================" << endl;
		cin >> gameselect;

		if(gameselect >=1 && gameselect <=3)
			return gameselect;
		else if (gameselect == 4 )
			return 0;
		else 
			system("cls");
			cout << "잘못 입력하셨습니다." <<endl;
	}
}

// 실행순서 2-1.
int firstmenu::personselect()
{
	system("cls");
	Re:
	firstmenu *in = new firstmenu();
	if (checkfirstgame == 0) // checkfirstgame -> 처음 실행하는 것인지 검사한다. 0 일결우 처음 실행 메뉴.
	{
		cout << " 원하는 만큼 플레이어의 수를 입력하십시오." << endl;
		cin >> player;
		while (player <= 0)
		{
			system("cls");
			cout << "양의 정수만 입력하실수 있습니다. 다시 입력해주세요." << endl;
			cin >> player;
		}
		system("cls");
		cout << " 메인 메뉴로 가시려면 0 번을 입력하세요.  " << endl;
		cout << " 입장하실 플레이어 번호를 입력해주세요. " << endl;
		for (int i = 0; i < player; i++)
		{
			person[i] = in;
			cout << "┌─────────────────────────────┐" << endl;
			printf("│ %2d 번 플레이어 // 자금 : %-29d 원│\n", i + 1,  person[i]->realMoney = G.money(0, i));
			cout << "└─────────────────────────────┘" << endl;
		}
		checkfirstgame = 1; // 처음 실행 체크변수 1로 변경
	}
	else
	{
		cout << " 메인 메뉴로 가시려면 0 번을 입력하세요.  " << endl;
		cout << " 입장하실 플레이어 번호를 입력해주세요. " << endl;
		for (int i = 0; i < player; i++)
		{
			cout << "┌─────────────────────────────┐" << endl;
			printf("│ %2d 번 플레이어 // 자금 : %-29d 원│\n", i + 1, person[i]->realMoney = G.money(0, i));
			cout << "└─────────────────────────────┘" << endl;
		}
	}
	cin >> selectplayer;
	if (selectplayer == 0)
	{
		for (int i = 0; i < player; i++)
		{
			int resetmoney = 0;
			resetmoney = G.money(0, i);
			G.money(-resetmoney, i);
			G.money(10000, i);
		}
	}
	else if (selectplayer > player || selectplayer < 0)
	{
		system("cls");
		cout << "잘못 입력 하셨습니다. 목록에 있는 플레이어중 선택해주세요." << endl;
		goto Re;
	}
	system("cls");
	delete in;
	return selectplayer;
}

// 실행순서 3-1.
void firstmenu::gamestartmenu(int game, int y) //3.1  입력받은 메뉴값으로 다음 실행을한다.
{                      
	firstmenu *fir = new firstmenu;
	switch (game)
	{
		case 1: {
			string gamename = "로또";
			fir = new lottogame[lastmenu(gamename)];
			(fir+lastmenu2(gamename)-1)->startgame(y); 
			Givemoney(y-1);
			delete[] fir;
			break; }
		case 2: {
			string gamename = "러시안 룰렛";
			fir = new russiangame[lastmenu(gamename)];
			(fir+lastmenu2(gamename)-1)->startgame(y); 
			Givemoney(y-1);
			delete[] fir;
			break; }
		case 3: {
			string gamename = "가위바위보";
			fir = new gawigame[lastmenu(gamename)];
			(fir+lastmenu2(gamename)-1)->startgame(y); 
			Givemoney(y-1);
			delete[] fir;
			break; }
		default: {
			system("cls");
			cout << "잘못된 값을 입력하셨습니다." << endl;
			delete fir;
			break; }
	}
}

int firstmenu::lastmenu(string gamename)
{
	system("cls");
	cout << "몇개의 "<< gamename <<" 게임을 생성 하시겠습니까?" <<endl;
	cin >> gamecount;
	while (gamecount <= 0)
	{
		system("cls");
		cout << "양의 정수만 입력하실수 있습니다. 다시 입력해주세요."<<endl;
		cin >> gamecount;
	}
	return gamecount;
}

int firstmenu::lastmenu2(string gamename)
{
	int selectgame;
	cout << "몇번째의 " << gamename << " 게임으로 시작하시겠습니까?" <<endl;
	cin >> selectgame;

	while (selectgame > gamecount || selectgame <= 0)
	{
		cout<<"생성한 게임 갯수의 범위를 벗어났습니다."<<endl;
		cout<< "현재 " <<gamecount << " 개의 " << gamename << " 게임이 생성 되어있습니다. " <<endl;
		cout<<"다시 선택해주세요."<<endl;
		cin >> selectgame;
	}
	system("cls");
	cout<<gamecount<<" 개의 " << gamename << " 게임중에 "<<selectgame<<" 번째 " << gamename << " 게임으로 시작합니다. " <<endl;
	return selectgame;
}

void firstmenu::Givemoney(int mey)
{
	person[mey]->realMoney = G.money(0, mey);
}

// 다형성
void firstmenu::startgame(int y)
{
	system("cls");
	cout << "게임파일(헤더,소스)을 추가해주세요." << endl;
};

void lottogame::startgame(int y)
{
	L.mainmenu(y);
};

void russiangame::startgame(int y)
{
	R.russian(y);
};

void gawigame::startgame(int y)
{
	W.run(y);
};