from django.core.exceptions import ValidationError
import os

def allow_only_images_validator(value):
    extension = os.path.splitext(value.name)[1]
    print(extension)
    valid_extensions = ['.jpg', '.jpeg', '.png']
    if not extension.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Allowed extensions are .jpg, .jpeg, .png')
