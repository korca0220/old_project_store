#blog/forms.py
from django import forms
from Junesite.widgets.naver_map_point_widget import NaverMapPointWidget
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'lnglat': NaverMapPointWidget(attrs={'width': 500, 'height': 300}),
        }
