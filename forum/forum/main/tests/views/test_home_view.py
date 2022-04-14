import os
import tempfile
from datetime import date
from io import BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files import File
from django.test import TestCase
from django.urls import reverse

from forum import settings
from forum.accounts.models import Profile
from forum.main.models import Category, Tag, Post

UserModel = get_user_model()

class HomeViewTests(TestCase):

    VALID_USER_DATA = {
        'username': 'manoel',
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
        post = Post.objects.create(**self.VALID_POST_DATA,category_id=category.id, user=user)
        post.tag.add(tag)
        return (user, profile, category, tag, post)

    def test_get__should_render_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'main/index.html')

    def test_get__when_zero_users_created__expect_user_count_0(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(0, response.context['users_count'])

    def test_get__when_one_user_created__expect_user_count_1(self):
        user = UserModel.objects.create_user(**self.VALID_USER_DATA)
        response = self.client.get(reverse('index'))
        self.assertEqual(1, response.context['users_count'])

    def test_get__when_one_post_created__expect_post_count_1(self):
        user, profile, category, tag, post = self.__create_valid_user_category_tag_post()
        response = self.client.get(reverse('index'))
        self.assertEqual(1, response.context['posts_count'])

    def test_get__when_zero_posts_created__expect_post_count_0(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(0, response.context['posts_count'])

    def test_get_latest_user__when_no_users__exprect_user_none(self):
        response = self.client.get(reverse('index'))
        self.assertEqual('None', response.context['latest_user'])

    def test_get_latest_user__when_we_have_users__exprect_user_success(self):
        user = UserModel.objects.create_user(**self.VALID_USER_DATA)
        response = self.client.get(reverse('index'))
        self.assertEqual(user, response.context['latest_user'])