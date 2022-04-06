from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from forum.accounts.managers import ForumUserManager
from forum.common.validators import validate_only_letters, validate_image_max_size


class ForumUser(AbstractBaseUser, PermissionsMixin):
    MAX_USERNAME_LENGTH = 25

    username = models.CharField(
        max_length=MAX_USERNAME_LENGTH,
        unique=True,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'username'

    objects = ForumUserManager()


class Profile(models.Model):
    FIRST_NAME_MAX_LENGTH = 25
    LAST_NAME_MAX_LENGTH = 25

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(validate_only_letters,)
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(validate_only_letters,)
    )

    picture = models.ImageField(
        upload_to='profiles',
        default='static_root/logo/forum-logo.png',
        validators=(
            validate_image_max_size,
        )
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    description = models.TextField(

    )

    user = models.OneToOneField(
        ForumUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return f'{self.user}'