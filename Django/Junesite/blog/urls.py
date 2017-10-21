# blog/urls.py
from django.conf.urls import url
from . import views # FBV
from . import views_cbv # CBV
urlpatterns = [

    # /blog/
    url(r'^$', views.post_list, name = 'post_list'),

    # /blog/10/
    url(r'^(?P<id>\d+)/$', views.post_detail, name = 'post_detail'),

    # /blog/10/edit/
    url(r'^(?P<id>\d+)/edit/$', views_cbv.post_edit, name = 'post_edit'), #cbv

    # /blog/10/delete/
    url(r'^(?P<id>\d+)/delete/$', views_cbv.post_delete, name = 'post_delete'), #cbv

    # /blog/new/
    url(r'^new/$', views.post_new, name = 'post_new'), # cbv

]
