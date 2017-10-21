# accounts/views.py
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as auth_login
from django.shortcuts import redirect, render
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers
from .forms import SignupForm, LoginForm

@login_required # 로그인 상황을 보장 받음
def profile(request): # 사용자 프로필 view
    return render(request, 'accounts/profile.html')


# 회원가입 view
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST) # SignupFrom 커스텀 폼
        if form.is_valid(): #유효성 검사
            user = form.save()
            return redirect(settings.LOGIN_URL) # LOGIN_URL = /accounts/login
                                                # SUCCESS URL
    else:  # POST 방식이 아니면
        form = SignupForm()
    return render(request, 'accounts/signup_form.html', {
        'form':form,
    }) # 회원가입 폼으로 이동


# login
# 다른 사이트에서 OAuth 인증 방식을 통해 로그인
def login(request):
    providers = []
    for provider in get_providers(): # login providers(naver, google, facebook...)을 가지고온다
        # social_app 속성은 커스텀 속성
        try:
            # 각 provider 별로 client ID와 SecretKey가 등록이 되어 있는지
            provider.social_app = SocialApp.objects.get(provider = provider.id, sites = settings.SITE_ID)
        except SocialApp.DoesNotExist:
            provider.social_app = None
        providers.append(provider)

    return auth_login(request,
        authentication_form = LoginForm,
        template_name = ('accounts/login_form.html'),
        extra_context = {'providers' : providers}) # 인자 전달
