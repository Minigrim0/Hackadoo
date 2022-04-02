from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.
class User(AbstractUser):
    user_types = (
        ('admin', 'Admin'),
        ('prof', 'Professor'),
        ('student', 'Student'),
    )

    accountType = models.CharField(choices=user_types, default="student", blank=False, max_length=10)