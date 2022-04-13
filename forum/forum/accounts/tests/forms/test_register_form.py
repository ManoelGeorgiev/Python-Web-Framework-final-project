from datetime import date
from io import BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files import File
from django.test import TestCase

from forum.accounts.forms import RegisterForm
from forum.accounts.models import Profile

UserModel = get_user_model()


class ProfileTests(TestCase):

    @staticmethod
    def get_image_file(name='test.png', ext='png', size=(50, 50), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGB", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    VALID_REGISTER_DATA = {
        'username': 'manoel',
        'password1': '8!576Hh_kd',
        'password2': '8!576Hh_kd',
        'first_name': 'Manoel',
        'last_name': 'Georgiev',
        'date_of_birth': date(1993, 9, 29),
        'bio': 'this is a bio',
        'email': 'test@email.com',
    }

    INVALID_FIRST_NAME_REGISTER_DATA = {
        'username': 'manoel',
        'password1': '8!576Hh_kd',
        'password2': '8!576Hh_kd',
        'first_name': 'Ma1noel',
        'last_name': 'Georgiev',
        'date_of_birth': date(1993, 9, 29),
        'bio': 'this is a bio',
        'email': 'test@email.com',
    }

    INVALID_LAST_NAME_REGISTER_DATA = {
        'username': 'manoel',
        'password1': '8!576Hh_kd',
        'password2': '8!576Hh_kd',
        'first_name': 'Manoel',
        'last_name': 'Ge orgiev',
        'date_of_birth': date(1993, 9, 29),
        'bio': 'this is a bio',
        'email': 'test@email.com',
    }

    def test_register_form__with_valid_input__expect_success(self):
        form = RegisterForm(data=self.VALID_REGISTER_DATA, files={'picture': self.get_image_file()})
        form.save()
        self.assertIsNotNone(Profile.pk)
        self.assertIsNotNone(UserModel.pk)

    def test_register_form__with_invalid_first_name__expect_fail(self):
        form = RegisterForm(data=self.INVALID_FIRST_NAME_REGISTER_DATA, files={'picture': self.get_image_file()})

        self.assertFalse(form.is_valid())

    def test_register_form__with_invalid_last_name__expect_fail(self):
        form = RegisterForm(data=self.INVALID_LAST_NAME_REGISTER_DATA, files={'picture': self.get_image_file()})

        self.assertFalse(form.is_valid())

