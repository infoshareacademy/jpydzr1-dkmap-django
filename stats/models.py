from django.db import models
from django.conf import settings
from datetime import timedelta


class PlayerStatistic(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    time_spend_in_game = models.DurationField(default=timedelta(seconds=0))
    best_game_time = models.DurationField(default=timedelta(seconds=0))
    game_counter = models.PositiveIntegerField(default=0)
    win_counter = models.PositiveIntegerField(default=0)

    def __str__(self):
        if self.user:
            return f"Statistics: {self.user.username}"
        return 'Account does not exist.'

