import os
from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from forum import settings
from forum.accounts.models import Profile
from forum.main.models import Category, Tag, Post

UserModel = get_user_model()


class CreatePostTests(TestCase):
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

    def test_authenticated_user_can_see_page__expect_OK_200(self):
        user = UserModel.objects.create_user(**self.VALID_USER_DATA)
        self.client.force_login(user=user)
        response = self.client.get(reverse('create post'))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_try_to_see_page__expect_302(self):
        response = self.client.get(reverse('create post'))
        self.assertEqual(response.status_code, 302)

    def test_create_post__with_valid_data__expect_success(self):
        user = UserModel.objects.create_user(**self.VALID_USER_DATA)
        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user)
        category = Category.objects.create(**self.VALID_CATEGORY_DATA)
        tag = Tag.objects.create(**self.VALID_TAG_DATA)

        VALID_POST_DATA = {
            'title': 'title',
            'content': 'new content',
            'category': category.pk,
            'tag': [tag.pk],
            'user': user,
        }
        self.client.force_login(user)

        response = self.client.post(reverse('create post'), VALID_POST_DATA)
        post = Post.objects.first()
        self.assertEqual(post.title, VALID_POST_DATA['title'])
        self.assertEqual(post.content, VALID_POST_DATA['content'])
        self.assertEqual(post.category.pk, VALID_POST_DATA['category'])
        self.assertEqual(post.tag.count(), 1)
        self.assertEqual(post.user, VALID_POST_DATA['user'])