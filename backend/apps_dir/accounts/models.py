from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'admin'),
        (2, 'interviewer'),
        (3, 'candidate'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=3)

    def __str__(self):
        return "{} ({})".format(self.username, dict(self.USER_TYPE_CHOICES)[self.user_type])
