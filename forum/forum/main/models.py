from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from hitcount.models import HitCountMixin, HitCount
from tinymce import models as tinymce_models


from forum import settings


class Category(models.Model):
    TITLE_MAX_LENGTH = 30

    class Meta:
        verbose_name_plural = 'Categories'

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
    )

    def __str__(self):
        return f'{self.title}'


class Post(models.Model, HitCountMixin):
    TITLE_MAX_LENGTH = 300

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
    )

    content = tinymce_models.HTMLField()

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    created_on = models.DateTimeField(
        auto_now_add=True,
    )

    edited_on = models.DateTimeField(
        auto_now=True,
    )

    closed = models.BooleanField(
        default=False,
    )

    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    def __str__(self):
        return f'{self.title}'


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )


class Comment(models.Model):
    class Meta:
        ordering = ['created_on']

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )

    content = tinymce_models.HTMLField()

    created_on = models.DateTimeField(
        auto_now_add=True,
    )

    edited_on = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f'{self.content[:50]}'
