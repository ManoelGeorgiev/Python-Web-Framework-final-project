import os
import tempfile
from datetime import date
from io import BytesIO

from PIL import Image
from django.contrib.staticfiles import finders
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from forum import settings
from forum.accounts.models import Profile, ForumUser


class ProfileTests(TestCase):

    @staticmethod
    def get_image_file(name='test.png', ext='png', size=(50, 50), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGB", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

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
    }

    def test_profile_create__when_first_name_contains_only_letters__expect_success(self):
        user = ForumUser.objects.create_user(**self.VALID_USER_DATA)

        profile = Profile(
            **self.VALID_PROFILE_DATA,
            user=user,
            picture=self.get_image_file()
        )
        profile.save()
        self.assertIsNotNone(profile.pk)

    def test_profile_create__when_first_name_contains_a_digit__expect_fail(self):
        user = ForumUser.objects.create_user(**self.VALID_USER_DATA)
        first_name = '1Manoel1'
        profile = Profile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],
            date_of_birth=self.VALID_PROFILE_DATA['date_of_birth'],
            bio=self.VALID_PROFILE_DATA['bio'],
            email=self.VALID_PROFILE_DATA['email'],
            user=user,
            picture=self.get_image_file()
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_a_dollar_sign__expect_fail(self):
        user = ForumUser.objects.create_user(**self.VALID_USER_DATA)
        first_name = 'Mano&el'
        profile = Profile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],
            date_of_birth=self.VALID_PROFILE_DATA['date_of_birth'],
            bio=self.VALID_PROFILE_DATA['bio'],
            email=self.VALID_PROFILE_DATA['email'],
            user=user,
            picture=self.get_image_file()
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_a_space__expect_fail(self):
        user = ForumUser.objects.create_user(**self.VALID_USER_DATA)
        first_name = 'Mano el'
        profile = Profile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],
            date_of_birth=self.VALID_PROFILE_DATA['date_of_birth'],
            bio=self.VALID_PROFILE_DATA['bio'],
            email=self.VALID_PROFILE_DATA['email'],
            user=user,
            picture=self.get_image_file()
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_full_name__when_valid__expect_correct_full_name(self):
        profile = Profile(**self.VALID_PROFILE_DATA)
        expected_fullname = f'{self.VALID_PROFILE_DATA["first_name"]} {self.VALID_PROFILE_DATA["last_name"]}'
        self.assertEqual(expected_fullname, profile.full_name)

    def test_profile_create__when_picture_is_under_5_mb__expect_success(self):
        user = ForumUser.objects.create_user(**self.VALID_USER_DATA)
        first_name = 'Manoel'
        profile = Profile(
            **self.VALID_PROFILE_DATA,
            user=user
        )

        profile.save()

        self.assertIsNotNone(profile.pk)

    def test_profile_create__when_picture_is_more_than_5_mb__expect_fail(self):
        def get_image_file(name='test.png', ext='png', size=(20000, 15000), color=(256, 0, 0)):
            file_obj = BytesIO()
            image = Image.new("RGB", size=size, color=color)
            image.save(file_obj, ext)
            file_obj.seek(0)
            return File(file_obj, name=name)

        user = ForumUser.objects.create_user(**self.VALID_USER_DATA)
        profile = Profile(
            first_name=self.VALID_PROFILE_DATA['first_name'],
            last_name=self.VALID_PROFILE_DATA['last_name'],
            date_of_birth=self.VALID_PROFILE_DATA['date_of_birth'],
            bio=self.VALID_PROFILE_DATA['bio'],
            email=self.VALID_PROFILE_DATA['email'],
            user=user,
            picture=os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, '10mb.png')
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)
