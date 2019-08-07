from django.utils import timezone

from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.

class Period(models.Model):
    """
    This is a contiguous amount of time # from what time, to what time am i available?
    anybody can add slots when they have time independently from each other
    """

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
        now = timezone.now()

        return f"{str((self.end_time-now)).split('.')[0]} Hours" if self.end_time > now else 0

    class Meta:
        unique_together = ['start_time', 'end_time', 'user']


class Reservation(models.Model):
    # caution!! this can be done better. `start_time` has to be in the periods list.
    # We need to enforce this at the db layer as well.

    start_time = models.DateTimeField()

    # this is the group of people in this reservation
    users = models.ManyToManyField(get_user_model(), blank=True, related_name='team')

    # Name the reservation! E.g Interview with Emmanuel
    name = models.CharField(null=False, blank=False, max_length=200)

    #
    # class Meta:
    #     unique_together = ['start_time', 'users']

    # todo: it would be interesting to have unique_together team and start_time :-D
    # e.g https://www.postgresql.org/docs/9.5/rangetypes.html#RANGETYPES-CONSTRAINT
    def team(self):
        return ", ".join([user.username for user in self.users.all()])
