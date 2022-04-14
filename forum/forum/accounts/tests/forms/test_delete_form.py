import os.path
from datetime import date
from io import BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files import File
from django.test import TestCase

from forum.accounts.forms import RegisterForm, DeleteProfileForm

UserModel = get_user_model()


class DeleteFormTests(TestCase):

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

    def test_delete_form_is_also_deleting_photo_from_disc__expect_success(self):
        form = RegisterForm(data=self.VALID_REGISTER_DATA, files={'picture': self.get_image_file()})
        form.save()
        user = UserModel.objects.get(pk=1)
        profile_picture_path = user.profile.picture.path
        form = DeleteProfileForm(instance=user)
        form.save()
        self.assertFalse(os.path.exists(profile_picture_path))
