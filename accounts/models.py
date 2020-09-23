from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

from accounts.utils import generate_token


class User(AbstractUser):
    email = models.EmailField(max_length=254, null=True)
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    passcode = models.CharField(max_length=4, null=True, blank=True)
    passcode_timer = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username']

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.email


class ResetKey(models.Model):
    reset_key = models.CharField(max_length=40, default=generate_token)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reset_key', db_index=False)
