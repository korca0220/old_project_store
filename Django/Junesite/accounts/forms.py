#accounts/forms.py
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm # 유저 로그인 확인, 회운가입
from django import forms
from . models import Profile

class SignupForm(UserCreationForm):
    # UserCreationForm에서 기본제공 되는 field가 아님. 커스텀 필드
    phone_number = forms.CharField()
    address = forms.CharField()

    # Meta 클래스만을 상속받아 field만 재정의
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',) #email은 기본 제공 필드

    def save(self): # save 메서드를 통해 커스텀 필드 저장
        user = super().save()
        # model manager를 통해 오브젝트 생성
        profile = Profile.objects.create(
            user = user,
            phone_number = self.cleaned_data['phone_number'],
            address = self.cleaned_data['address'])
        return user


class LoginForm(AuthenticationForm):
    answar = forms.IntegerField(label= '4*3=?') # 로그인 시 사용자 확인 (봇 인지 아닌지)

    def clean_answar(self): # clean_ 메서드를 통한 1회성 유효성 검사
        answar = self.cleaned_data.get('answar', None) #폼 인스턴스 내에서 clean함수를 통해 변환되었을 수도 있을 데이터
        if answar != 12:                                # answar가 있으면 이를 가저오고 아니면 None
            raise forms.ValidationError('답이 아닙니다!') # 유효성 검사 에러 발생
        return answar
