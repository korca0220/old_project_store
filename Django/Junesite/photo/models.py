#photo/models.py
from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import Thumbnail

class Photo(models.Model):
    photo = ProcessedImageField(blank=True, upload_to='photo/post/%Y/%m/%d',
            processors=[Thumbnail(300, 300)],
            format='JPEG',
            options={'qualirt':60})
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length = 100, verbose_name='제목',
    help_text='포스트 제목을 입력해주세요(최대 100자)') #길이 제한이 있는 문자열
    created_at = models.DateTimeField(auto_now_add=True) #최초 생성 자동 저장
    updated_at = models.DateTimeField(auto_now=True) # 저장 될떄마다(갱신) 자동 저장

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('photo:photo_detail', args=[self.id])
