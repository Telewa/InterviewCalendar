from django.utils import timezone

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

class Period(models.Model):
    """
    This is a contiguous amount of time
    """
    # from what time are you available?
    start_time = models.DateTimeField()

    # up to what time are you available?
    end_time = models.DateTimeField()

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    def duration(self):
        return self.end_time - self.start_time

    def time_left(self):
        end = self.end_time
        start = timezone.now()

        return f"{str((end-start)).split('.')[0]} Hours" if end > start else 0