# blog/admin.py
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Post, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [ 'id', 'title', 'user', 'status', 'created_at', 'updated_at']
    actions = ['make_published', 'make_draft', 'make_withdraw']

    def make_published(self, request, queryset):
        updated_count = queryset.update(status = 'Published')
        self.message_user(request, '총 {}건의 포스트가 공개상태로 변경'.format(updated_count))
    make_published.short_description = '공개 상태로 변경 합니다.'

    def make_draft(self, request, queryset):
        update_count = queryset.update(status = 'Draft')
        self.message_user(request, '총 {}.건의 포스트가 미공개 상태로 변경'.format(update_count))
    make_draft.short_description = '미공개 상태로 변경 합니다.'

    def make_withdraw(self, request, queryset):
        update_count = queryset.update(status = 'Withdraw')
        self.message_user(request, '총 {}.건의 포스트가 폐지 예정 상태로 변경'.format(update_count))
    make_withdraw.short_description = '폐지 예정 상태로 변경 합니다.'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
