# blog/models.py
import re
from django.db import models
from django.conf import settings
from django.forms import ValidationError
from django.shortcuts import reverse

def lnglat_validator(value):
    if not re.match(r'^([+-]?\d+\.?\d*),([+-]?\d+\.?\d*)$', value):
        raise ValidationError('Invalid LngLat Type')

class Post(models.Model):
    STATUS_CHOICES = (
        ('Draft', '미완성'),
        ('Published', '공개'),
        ('Withdraw', '폐지 예정'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length = 100, verbose_name = '제목',
        help_text = '포스트의 제목(최대 100자)')
    content = models.TextField(verbose_name = '내용')
    created_at = models.DateTimeField(auto_now_add=True) #최초 작성 시간 저장
    updated_at = models.DateTimeField(auto_now=True) # 저장(갱실)될 때마다 자동 저장
    lnglat = models.CharField(max_length=50, blank=True,
        validators=[lnglat_validator])
    tag_set = models.ManyToManyField('Tag', blank = True)
    status = models.CharField(max_length = 10, choices = STATUS_CHOICES)

    class Meta:
        ordering = ['-id'] # id 역순으로 정렬

    def __str__(self):
        return self.title

    def get_absolute_url(self): # cbv 에서 success_url 값을 대신한다
        return reverse('blog:post_detail', args = [self.id])

class Tag(models.Model): # tag_set , Post모델과 N:M의 관계
    name = models.CharField(max_length=50, unique = True)

    def __str__(self):
        return self.name
