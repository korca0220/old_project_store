# accounts/urls.py
from django.conf.urls import url
from django.contrib.auth import views as auth_view # 장고 기본 제공 auth
from django.conf import settings
from . import views

urlpatterns = [

    # /accounts/profile
    url(r'^profile/$', views.profile, name = 'profile'),

    # /accounts/signup
    url(r'^signup/$', views.signup, name = 'signup'),

    # /accounts/login
    url(r'^login/$', views.login, name = 'login'),

    # /accounts/logout
    url(r'^logout/$', auth_view.logout, name = 'logout',
        kwargs={'next_page':settings.LOGIN_URL}),
]
