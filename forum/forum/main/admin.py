from django.contrib import admin

from forum.main.models import Post, Category, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Comment)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('content',)