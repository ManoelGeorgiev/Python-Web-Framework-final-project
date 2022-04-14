from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

UserModel = get_user_model()


class CreatePostTests(TestCase):
    VALID_USER_DATA = {
        'username': 'manoel',
        'password': '8!576Hh_kd',
    }

    def test_authenticated_user_can_see_page__expect_OK_200(self):
        user = UserModel.objects.create_user(**self.VALID_USER_DATA)
        self.client.force_login(user=user)
        response = self.client.get(reverse('create post'))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_try_to_see_page__expect_302(self):
        response = self.client.get(reverse('create post'))
        self.assertEqual(response.status_code, 302)
