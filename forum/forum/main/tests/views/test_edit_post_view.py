import os
from datetime import date
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from forum import settings
from forum.accounts.models import Profile
from forum.main.models import Category, Tag, Post

UserModel = get_user_model()


class EditPostViewTests(TestCase):
    VALID_USER_DATA = {
        'username': 'manoel',
        'password': '8!576Hh_kd',
    }

    VALID_USER1_DATA = {
        'username': 'manol',
        'password': '!586Hh_kd',
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
    VALID_CATEGORY_DATA1 = {
        'title': 'Java',
    }

    VALID_TAG_DATA = {
        'name': 'function'
    }

    VALID_TAG_DATA1 = {
        'name': 'app'
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

    def test_get__when_post_owner__expect_OK_200(self):
        user, profile, category, tag, post = self.__create_valid_user_category_tag_post()
        self.client.force_login(user=user)
        response = self.client.get(reverse('edit post', args=[post.pk]))
        self.assertEqual(response.status_code, 200)

    def test_get__when_not_post_owner__expect_redirect(self):
        user, profile, category, tag, post = self.__create_valid_user_category_tag_post()
        user1 = UserModel.objects.create_user(**self.VALID_USER1_DATA)
        self.client.force_login(user=user1)
        response = self.client.get(reverse('edit post', args=[post.pk]))
        self.assertEqual(response.status_code, 302)

    def test_get__when_post_doesnt_exist__expect_404(self):
        user = UserModel.objects.create_user(**self.VALID_USER_DATA)
        self.client.force_login(user=user)
        response = self.client.get(reverse('edit post', args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_edit_post__with_valid_data__expect_success(self):
        user, profile, category, tag, post = self.__create_valid_user_category_tag_post()
        category2 = Category.objects.create(**self.VALID_CATEGORY_DATA1)
        tag2 = Tag.objects.create(**self.VALID_TAG_DATA1)
        VALID_POST_DATA_EDIT = {
            'title': 'new title',
            'content': 'new content',
            'category': category2.pk,
            'tag': [tag.pk, tag2.pk],
        }
        self.client.force_login(user)
        s = self.client.session
        s.update(
            {'previous_page': reverse('post details', args=[post.pk])},
        )
        s.save()
        response = self.client.post(reverse('edit post', args=[post.pk]), VALID_POST_DATA_EDIT)
        post1 = Post.objects.first()
        self.assertEqual(post1.title, VALID_POST_DATA_EDIT['title'])
        self.assertEqual(post1.content, VALID_POST_DATA_EDIT['content'])
        self.assertEqual(post1.category.pk, VALID_POST_DATA_EDIT['category'])
        self.assertEqual(post1.tag.count(), 2)
