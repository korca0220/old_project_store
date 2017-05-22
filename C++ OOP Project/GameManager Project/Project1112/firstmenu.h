#ifndef FIRSTMENU_H
#define FIRSTMENU_H
class firstmenu
{
private:
	int player; // Player 
	int selectplayer; //Player를 선택하는 변수
	int realMoney; //실제 게임에서 활용되는 돈
	int gamecount; //게임 생성개수 체크를위한 변수(다형성 사용 test)

public:
	int mainmenu(); //1번. 메인메뉴를 띄워주고 선택한 메뉴값 반환하는 함수
	int personselect(); //2번. 원하는만큼 플레이어 생성 및 선택한 플레이어의 배열번호 반환
	int checkfirstgame; //처음 실행인지 체크
	void gamestartmenu(int game, int y); //3번. 메뉴값, 플레이어 배열번호를 넘겨받아 게임실행.
	int lastmenu(std::string gamename);
	int lastmenu2(std::string gamename);
	void Givemoney(int mon); // 각 게임에서 반환된 돈을 플레이어에 넘겨서저장
	firstmenu *person[100]; 
	virtual void startgame(int y);
};

class lottogame : public firstmenu
{
public:
	void startgame(int y);
};

class gawigame : public firstmenu
{
public:
	void startgame(int y);
};

class russiangame : public firstmenu
{
public:
	void startgame(int y);
};

#endif