from django.db import models
from django.conf import settings
from datetime import timedelta


class PlayerStatistic(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_spend_in_game = models.DurationField(default=timedelta(seconds=0))
    best_game_time = models.DurationField(default=timedelta(seconds=0))
    game_counter = models.IntegerField(default=0)
    win_counter = models.IntegerField(default=0)
    lose_counter = models.IntegerField(default=0)

    def __str__(self):
        return f"Statistics: {self.user.username}"

    def add_win(self) -> int:
        self.win_counter += 1
        self.save()
        return self.win_counter

    def add_game(self) -> int:
        self.game_counter += 1
        self.save()
        return self.game_counter
