#ifndef LOTTO_H
#define LOTTO_H
class lotto  // lotto 클래스 선언
{
private:
	int menu; // 입력받는 메뉴값 멤버변수
	int count; // 당첨갯수 확인하는 멤버변수
	int bonusnum; // 본게임에서 사용하는 보너스번호 멤버변수
public:
	int simul3(int player); // 3개 숫자 맞추기 함수
	int simul6(int player); // 일반 로또시뮬돌리는 함수
	int chart(); // 당첨금액차트 보여주는 함수
	void endprint(); // 맨끝에 보여주는 문구 함수
	int remenu; // 메뉴로 돌아가는 멤버변수
	int mainmenu(int player); //메인메뉴에서 값 입력받는 함수

};
#endif