from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField


board_choices = (('X', 'X'),
                 ('O', 'O'),
                 ('-', '-'),
                 )


class Game(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    multiplayer_game = models.BooleanField(default=False)
    win = models.BooleanField(default=False)
    start_time = models.DateTimeField(auto_now_add=True, blank=True)
    finish_time = models.DateTimeField(blank=True, null=True)
    game_duration = models.DurationField(blank=True, null=True)

    def __str__(self):
        return f"{self.start_time} - {self.user.username}"


# class GameSession(models.Model):
#     games = models.ForeignKey(Game, on_delete=models.CASCADE)


class Board(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE, blank=True, null=True)
    first_field = models.CharField(max_length=1, choices=board_choices, default='-')
    second_field = models.CharField(max_length=1, choices=board_choices, default='-')
    third_field = models.CharField(max_length=1, choices=board_choices, default='-')
    fourth_field = models.CharField(max_length=1, choices=board_choices, default='-')
    fifth_field = models.CharField(max_length=1, choices=board_choices, default='-')
    sixth_field = models.CharField(max_length=1, choices=board_choices, default='-')
    seventh_field = models.CharField(max_length=1, choices=board_choices, default='-')
    eighth_field = models.CharField(max_length=1, choices=board_choices, default='-')
    ninth_field = models.CharField(max_length=1, choices=board_choices, default='-')

    def __str__(self):
        return f"Board_{str(self.id)}"
