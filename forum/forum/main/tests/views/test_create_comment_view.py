import datetime
import os
from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from forum import settings
from forum.accounts.models import Profile
from forum.main.models import Category, Tag, Post, Comment

UserModel = get_user_model()


class LikeCommentViewTests(TestCase):
    VALID_USER_DATA = {
        'username': 'manoel',
        'password': '8!576Hh_kd',
    }

    VALID_USER_DATA1 = {
        'username': 'ivan',
        'password': '8!576Hh_kd',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'Manoel',
        'last_name': 'Georgiev',
        'date_of_birth': date(1993, 9, 29),
        'bio': 'this is a bio',
        'email': 'test@email.com',
        'picture': os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, 'test.png')
    }

    VALID_CATEGORY_DATA = {
        'title': 'Python',
    }

    VALID_TAG_DATA = {
        'name': 'function'
    }

    VALID_POST_DATA = {
        'title': 'post1',
        'content': 'some content'
    }

    def __create_valid_user_category_tag_post(self):
        user = UserModel.objects.create_user(**self.VALID_USER_DATA)
        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user)
        category = Category.objects.create(**self.VALID_CATEGORY_DATA)
        tag = Tag.objects.create(**self.VALID_TAG_DATA)
        post = Post.objects.create(**self.VALID_POST_DATA, category_id=category.id, user=user)
        post.tag.add(tag)
        return (user, profile, category, tag, post)

    def test_get__when_post_is_closed__expect_redirect(self):
        user, profile, category, tag, post = self.__create_valid_user_category_tag_post()
        post.closed = True
        post.save()
        VALID_COMMENT_DATA = {
            'content': 'some text',
            'created_on': datetime.time,
            'edited_on': datetime.time,
            'user_id': user.pk,
            'post_id': post.pk,
        }
        self.client.force_login(user)
        response = self.client.get(reverse('create comment', args=[post.pk]))
        self.assertRedirects(response, reverse('index'))

    def test_post__when_comment_is_valid__expect_success(self):
        user, profile, category, tag, post = self.__create_valid_user_category_tag_post()
        VALID_COMMENT_DATA = {
            'content': 'some text',
            'created_on': datetime.date,
            'edited_on': datetime.date,
            'user_id': user.pk,
            'post_id': post.pk,
        }
        self.client.force_login(user)
        s = self.client.session
        s.update(
            {'previous_page': reverse('post details', args=[post.pk])},
        )
        s.save()
        response = self.client.post(reverse('create comment', args=[post.pk]), VALID_COMMENT_DATA)
        comment = Comment.objects.first()
        self.assertEqual(comment.content, VALID_COMMENT_DATA['content'])
        self.assertEqual(comment.user_id, VALID_COMMENT_DATA['user_id'])
        self.assertEqual(comment.post_id, VALID_COMMENT_DATA['post_id'])
        self.assertRedirects(response, reverse('post details', args=[post.pk]))
