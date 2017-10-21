#Junesite/views.py
from django.views.generic.base import TemplateView

home_view = TemplateView.as_view(template_name='home.html')
