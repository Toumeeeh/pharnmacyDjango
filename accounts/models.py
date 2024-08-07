from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('pharmacist', 'Pharmacist'),
        ('supplier', 'Supplier'),
    )
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES)
