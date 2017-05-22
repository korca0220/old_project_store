#ifndef MONEY_H
#define MONEY_H

class gamemoney
{
public:  //클래스내의 static 변수는 반드시 class 내에서 초기화를 해야함.
	static unsigned int money(unsigned int x, int y) // 소지금 함수 (x값은 금액 증감값, y값은 플레이어 배열번호. 0번부터시작)
	{
		static int count = 0;
		static unsigned int mon[100];
		if (count == 0)
		{
			for (int i = 0; i < 100; i++)
				mon[i] = 10000;
			count = 1;
		}

		mon[y] = mon[y] + x;
		return mon[y];
	}
};
#endif


