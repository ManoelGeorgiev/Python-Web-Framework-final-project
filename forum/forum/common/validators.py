import os

from django.core.exceptions import ValidationError


def validate_only_letters(value):
    if not value.isalpha():
        return ValidationError('The name should contain only letters.')


def validate_image_max_size(value):
    filesize = value.file.size
    max_filesize = 5
    if filesize > max_filesize * 1024 * 1024:
        raise ValidationError(f'Max file size {max_filesize}MB.')


def validate_image_max_size_when_registering(value):
    filesize = value.size
    max_filesize = 5
    if filesize > max_filesize * 1024 * 1024:
        raise ValidationError(f'Max file size {max_filesize}MB.')
