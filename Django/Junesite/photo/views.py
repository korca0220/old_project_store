#photo/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django import forms
from .models import Photo
from .forms import PhotoForm


def photo_new(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()

            messages.success(request, '새 포토를 저장했습니다.')
            return redirect(post) #post.get_absolute_url
    else:
        form = PhotoForm()
    return render(request, 'photo/photo_form.html', {
        'form':form,
    })

def photo_edit(request, id):
    post = get_object_or_404(Photo, id=id)

    if request.method == 'POST':
        form = PhotoForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, '포스트를 수정했습니다.')
            return redirect(post) #post.get_absolute_url
    else:
        form = PhotoForm(instance=post)
    return render(request, 'photo/photo_form.html', {
        'form':form,
    })
