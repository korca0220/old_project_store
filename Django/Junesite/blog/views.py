from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from .forms import PostForm


def post_list(request):
    post = Post.objects.prefetch_related('tag_set').all()
    q = request.GET.get('q', '') #GET메소드로 받음. 'q'가 없으면 공백을 반환
    if q:
        post = post.filter(title__icontains = q) # q를 필터로 쿼리셋을 반환한다

    return render(request, 'blog/post_list.html', {
        'post_list' : post,
        'q' : q,
    })

def post_detail(request, id):
    post = get_object_or_404(Post, id = id) # 페이지가 없는 경우 404에러
    return render(request, 'blog/post_detail.html', {
        'post': post,
    })

@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            #messages의 경우 'context_processros'를 이용해 context list에 접근 가능
            messages.success(request, '새 포스트를 저장했습니다.')
            return redirect(post) #post.get_absolute_url
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {
        'form':form,
    })
