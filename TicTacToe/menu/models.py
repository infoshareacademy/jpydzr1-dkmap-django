from django.db import models
from django.conf import settings
from datetime import timedelta, datetime


class PlayerStatistic(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_spend_in_game = models.DurationField(default=timedelta(seconds=0))
    best_game_time = models.DurationField(default=timedelta(seconds=0))
    game_counter = models.IntegerField(default=0)
    win_counter = models.IntegerField(default=0)
    lose_counter = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


# class Game(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     multiplayer_game = models.BooleanField(default=False)
#     win = models.BooleanField(default=False)
#     start_time = models.TimeField(auto_now_add=True, blank=True)
#     finish_time = models.TimeField(default=datetime.now() + timedelta(seconds=432))
#     game_duration = models.DurationField(default=0)


