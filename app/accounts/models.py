from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    USER_ROLE = (
        ('student', 'Student'),
        ('teacher', 'Teacher')
    )

    role = models.CharField(choices=USER_ROLE, max_length=7, default=None)
