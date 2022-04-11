from django import forms
from tinymce.widgets import TinyMCE

from forum.common.helpers import BootstrapMixin
from forum.main.models import Post, Comment


class CreatePostForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'tag', 'content']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self._init_bootstrap_for_fields()

    def save(self, commit=True):
        post = super().save(commit=False)
        post.user = self.user
        if commit:
            post.save()
            self._save_m2m()
        return post


class EditPostForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'tag', 'content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_for_fields()


class DeletePostForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'readonly': True,
                }
            ),
            'content': forms.Textarea(
                attrs={
                    'readonly': True,
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_for_fields()


class CreateCommentForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, user, post_pk, *args, **kwargs):
        self.user = user
        self.post_pk = post_pk
        super().__init__(*args, **kwargs)
        self._init_bootstrap_for_fields()

    content = forms.CharField(
        label='',
        widget=TinyMCE()
        )

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.user = self.user
        comment.post_id = self.post_pk
        if commit:
            comment.save()
        return comment


class EditCommentForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_for_fields()

    content = forms.CharField(
        label='',
        widget=TinyMCE()
        )


class DeleteCommentForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_for_fields()

    content = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'readonly': True,
            }
        )
    )

