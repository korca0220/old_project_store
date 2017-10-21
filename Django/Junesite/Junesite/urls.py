# Junesite/urls.py
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.shortcuts import redirect
from . import views

urlpatterns = [
    url(r'^$', views.home_view, name='home'), # homepage
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^photo/', include('photo.urls', namespace='photo'))
]

#media 파일을 개발서버에서 인식하기 위함
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

#debug_toolbar 사용을 위함
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
