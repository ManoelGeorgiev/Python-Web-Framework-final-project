from django.contrib import admin

from forum.main.models import Post, Category, Comment, Tag


class CommentInline(admin.TabularInline):
    model = Comment
    list_display = ('content',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [
        CommentInline,
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content',)
