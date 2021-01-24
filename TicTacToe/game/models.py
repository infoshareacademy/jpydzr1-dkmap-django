from django.db import models
from django.conf import settings


board_choices = (('X', 'X'),
                 ('O', 'O'),
                 ('-', '-'),
                 )


class Game(models.Model):
    player_x = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 related_name="player_x_games",
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True
                                 )
    player_o = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 related_name="player_o_games",
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True
                                 )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name='created_games',
                                   on_delete=models.CASCADE,
                                   null=True,
                                   blank=True
                                   )
    in_progress = models.BooleanField(default=True)
    win = models.BooleanField(default=False)
    start_time = models.DateTimeField(auto_now_add=True, blank=True)
    finish_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.start_time} - {self.player_x}"


# class GameSession(models.Model):
#     games = models.ForeignKey(Game, on_delete=models.PROTECT)


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
