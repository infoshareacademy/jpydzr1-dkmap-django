from django.db import models
from django.conf import settings


class Game(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    multiplayer_game = models.BooleanField(default=False)
    win = models.BooleanField(default=False)
    start_time = models.DateTimeField(auto_now_add=True, blank=True)
    finish_time = models.DateTimeField()
    game_duration = models.DurationField(default=0)

    def __str__(self):
        return f"{self.start_time} - {self.user.username}"