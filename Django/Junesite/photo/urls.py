# photo/urls.py
from django.conf.urls import url
from . import views #fbv
from . import views_cbv # cbv

urlpatterns = [

    #/photo/
    url(r'^$', views_cbv.photo_list, name = 'photo_list'), #cbv

    #/photo/new/
    url(r'^new/$', views.photo_new, name = 'photo_new'),

    #/photo/10/
    url(r'^(?P<id>\d+)/$', views_cbv.photo_detail, name = 'photo_detail'), #cbv

    #/photo/10/edit/
    url(r'^(?P<id>\d+)/edit/$', views.photo_edit, name = 'photo_edit'),

    #/photo/10/delete
    url(r'^(?P<id>\d+)/delete/$', views_cbv.photo_delete, name = 'photo_delete'), #cbv
]
