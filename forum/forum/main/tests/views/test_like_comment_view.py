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

    def test_get__when_user_is_not_logged__expect_redirect(self):
        user, profile, category, tag, post = self.__create_valid_user_category_tag_post()
        VALID_COMMENT_DATA = {
            'content': 'some text',
            'created_on': datetime.time,
            'edited_on': datetime.time,
            'user_id': user.pk,
            'post_id': post.pk,
        }

        comment = Comment.objects.create(**VALID_COMMENT_DATA)
        response = self.client.get(reverse('like comment', args=[comment.pk]))
        self.assertRedirects(response, reverse('index'))

    def test_get__when_user_is_owner_of_the_post__expect_redirect(self):
        user, profile, category, tag, post = self.__create_valid_user_category_tag_post()
        VALID_COMMENT_DATA = {
            'content': 'some text',
            'created_on': datetime.time,
            'edited_on': datetime.time,
            'user_id': user.pk,
            'post_id': post.pk,
        }
        self.client.force_login(user)
        comment = Comment.objects.create(**VALID_COMMENT_DATA)
        response = self.client.get(reverse('like comment', args=[comment.pk]))
        self.assertRedirects(response, reverse('index'))

    def test_get__when_valid_user_likes_the_post__expect_success(self):
        user, profile, category, tag, post = self.__create_valid_user_category_tag_post()
        VALID_COMMENT_DATA = {
            'content': 'some text',
            'created_on': datetime.time,
            'edited_on': datetime.time,
            'user_id': user.pk,
            'post_id': post.pk,
        }
        comment = Comment.objects.create(**VALID_COMMENT_DATA)
        user1 = UserModel.objects.create_user(**self.VALID_USER_DATA1)
        self.client.force_login(user1)
        response = self.client.get(reverse('like comment', args=[comment.pk]))
        self.assertEqual(comment.commentlikebutton_set.count(), 1)

    def test_get__when_valid_user_unlikes_the_post__expect_success(self):
        user, profile, category, tag, post = self.__create_valid_user_category_tag_post()
        VALID_COMMENT_DATA = {
            'content': 'some text',
            'created_on': datetime.time,
            'edited_on': datetime.time,
            'user_id': user.pk,
            'post_id': post.pk,
        }
        comment = Comment.objects.create(**VALID_COMMENT_DATA)
        user1 = UserModel.objects.create_user(**self.VALID_USER_DATA1)
        self.client.force_login(user1)
        self.client.get(reverse('like comment', args=[comment.pk]))
        response = self.client.get(reverse('like comment', args=[comment.pk]))
        self.assertEqual(comment.commentlikebutton_set.count(), 0)
