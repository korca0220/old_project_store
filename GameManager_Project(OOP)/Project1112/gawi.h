#ifndef GAWI_H
#define GAWI_H

class gawi
{
private:
	int user; //게임을 플레이할 user(player)선택
	int com; //유저와 게임을 하게될 computer
	int count; //승리수 누적 체크
	int enter; //입력 변수
	int realMoney; //각 user가 갖고있는 돈을 가저오는 변수
public:
	void gawiPrint(int pp);
	int run(int p);
	int money(int a, int b);
};
#endif