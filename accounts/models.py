from django.contrib.auth.models import AbstractUser
from django.db import models
from encrypted_model_fields.fields import EncryptedCharField


class User(AbstractUser):
    platform_login = EncryptedCharField(max_length=200, blank=True, null=True)
    platform_password = EncryptedCharField(max_length=200, blank=True, null=True)
    platform_id = models.IntegerField(unique=True, blank=True, null=True)
