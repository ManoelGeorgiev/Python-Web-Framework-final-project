import os

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from forum.accounts.models import ForumUser, Profile
from forum.common.helpers import BootstrapMixin
from forum.common.validators import validate_image_max_size_when_registering


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
        model = get_user_model()
        field = ['username', 'password']


class RegisterForm(BootstrapMixin, UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'date_of_birth', 'picture',
                  'description']

    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LENGTH,
    )

    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGTH
    )

    picture = forms.ImageField(
        validators=(
            validate_image_max_size_when_registering,
        )
    )

    date_of_birth = forms.DateField()

    description = forms.CharField(
        widget=forms.Textarea
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None
        self._init_bootstrap_for_fields()

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            picture=self.cleaned_data['picture'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            description=self.cleaned_data['description'],
            user=user,
        )

        if commit:
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


