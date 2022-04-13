import os
import tempfile
from datetime import date
from io import BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files import File
from django.test import TestCase

from forum import settings
from forum.accounts.models import Profile

UserModel = get_user_model()

class ProfileTests(TestCase):

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

    def test_profile_create__when_first_name_contains_only_letters__expect_success(self):
        user = UserModel.objects.create_user(**self.VALID_USER_DATA)

        profile = Profile(
            **self.VALID_PROFILE_DATA,
            user=user,
        )
        profile.save()
        self.assertIsNotNone(profile.pk)

    def test_profile_create__when_first_name_contains_a_digit__expect_fail(self):
        user = UserModel.objects.create_user(**self.VALID_USER_DATA)
        first_name = '1Manoel1'
        profile = Profile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],
            date_of_birth=self.VALID_PROFILE_DATA['date_of_birth'],
            bio=self.VALID_PROFILE_DATA['bio'],
            email=self.VALID_PROFILE_DATA['email'],
            user=user,
            picture=os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, 'test.png')
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_a_dollar_sign__expect_fail(self):
        user = UserModel.objects.create_user(**self.VALID_USER_DATA)
        first_name = 'Mano&el'
        profile = Profile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],
            date_of_birth=self.VALID_PROFILE_DATA['date_of_birth'],
            bio=self.VALID_PROFILE_DATA['bio'],
            email=self.VALID_PROFILE_DATA['email'],
            user=user,
            picture=os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, 'test.png')
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_a_space__expect_fail(self):
        user = UserModel.objects.create_user(**self.VALID_USER_DATA)
        first_name = 'Mano el'
        profile = Profile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],
            date_of_birth=self.VALID_PROFILE_DATA['date_of_birth'],
            bio=self.VALID_PROFILE_DATA['bio'],
            email=self.VALID_PROFILE_DATA['email'],
            user=user,
            picture=os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, 'test.png')
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
        user = UserModel.objects.create_user(**self.VALID_USER_DATA)
        first_name = 'Manoel'
        profile = Profile(
            **self.VALID_PROFILE_DATA,
            user=user
        )

        profile.save()

        self.assertIsNotNone(profile.pk)

    def test_profile_create__when_picture_is_more_than_5_mb__expect_fail(self):
        user = UserModel.objects.create_user(**self.VALID_USER_DATA)
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
