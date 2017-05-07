#ifndef RUS_H
#define RUS_H

class rus // 러시안 룰렛게임 클래스 선언
{
public:
	int russian(int player); // 러시안 룰렛 함수
	int Bullet; // 총알 난수 생성 변수 
	int Coin; // 동전앞면 뒷면 난수 생성 변수
	int Select; // 선잡는 동전 앞뒷면 변수
	int Score; // 연승 카운트 변수
	unsigned int bet; // 베팅 금액 변수
	void end(); // 게임이 끝날 때 마다 출력되는 문장 함수
};
#endif