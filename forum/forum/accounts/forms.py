import os

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from forum.accounts.models import Profile
from forum.common.helpers import BootstrapMixin
from forum.common.validators import validate_image_max_size_when_registering

UserModel = get_user_model()


class LoginForm(BootstrapMixin, AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self._init_bootstrap_for_fields()

    username = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
            }
        )
    )

    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
            }
        )
    )

    class Meta:
        model = UserModel
        field = ['username', 'password']


class RegisterForm(BootstrapMixin, UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'date_of_birth', 'picture',
                  'bio']

    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LENGTH,
    )

    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGTH
    )

    email = forms.EmailField()

    picture = forms.ImageField(
        validators=(
            validate_image_max_size_when_registering,
        )
    )

    date_of_birth = forms.DateField()

    bio = forms.CharField(
        widget=forms.Textarea
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None
        self._init_bootstrap_for_fields()

    def save(self, commit=True):
        user = super().save(commit=False)
        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            picture=self.cleaned_data['picture'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            bio=self.cleaned_data['bio'],
            user=user,
        )

        if commit:
            user.save()
            profile.save()
        return user


class DeleteProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ()

    def save(self, commit=True):
        photo_path = self.instance.profile.picture.path
        os.remove(photo_path)
        self.instance.delete()
        return self.instance


class EditProfileForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email', 'first_name', 'last_name', 'date_of_birth', 'picture', 'bio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_for_fields()

    # checks if there is new picture and deletes the old one
    def save(self, commit=True):
        past_photo_name = self.initial['picture'].name
        new_photo_name = self.cleaned_data['picture'].name
        if not past_photo_name == new_photo_name:
            os.remove(self.initial['picture'].path)
        self.instance.save()
        return self.instance
