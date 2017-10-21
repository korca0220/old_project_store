from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Post


post_new = CreateView.as_view(model=Post)

post_edit = UpdateView.as_view(model=Post, fields='__all__', pk_url_kwarg='id')

post_delete = DeleteView.as_view(model= Post, success_url='/blog/', pk_url_kwarg='id')
