from django.contrib import admin

from forum.accounts.models import Profile, ForumUser


@admin.register(Profile)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(ForumUser)
class PostAdmin(admin.ModelAdmin):
    list_display = ('username',)