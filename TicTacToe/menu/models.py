from django.db import models
from django.conf import settings


class PlayerStatistic(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_spend_in_game = models.DurationField(default=0)
    best_game_time = models.DurationField(default=0)
    game_counter = models.IntegerField()
    win_counter = models.IntegerField()
    lose_counter = models.IntegerField()

    def __str__(self):
        return self.user.username


class Game(models.Model):

    # id,
    # multi,
    # single,
    # user, (jeden lub dwoch),
    # wygrana,
    # przegrana,
    # czas rozpoczenia,
    # czas zakonczenia,
    # czas partii, 'DurationField'
    pass

