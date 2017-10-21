#photo/views_cbv.py
from django.views.generic import ListView, DetailView, DeleteView
from .models import Photo


photo_detail = DetailView.as_view(model = Photo, pk_url_kwarg = 'id')

photo_list = ListView.as_view(model = Photo, paginate_by = 4)

photo_delete = DeleteView.as_view(model = Photo, pk_url_kwarg = 'id', success_url='/photo/')
