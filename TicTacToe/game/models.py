from django.db import models
from django.conf import settings


board_choices = (('X', 'X'),
                 ('O', 'O'),
                 (' ', ' '),
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
    first_field = models.CharField(max_length=1, choices=board_choices, default=' ')
    second_field = models.CharField(max_length=1, choices=board_choices, default=' ')
    third_field = models.CharField(max_length=1, choices=board_choices, default=' ')
    fourth_field = models.CharField(max_length=1, choices=board_choices, default=' ')
    fifth_field = models.CharField(max_length=1, choices=board_choices, default=' ')
    sixth_field = models.CharField(max_length=1, choices=board_choices, default=' ')
    seventh_field = models.CharField(max_length=1, choices=board_choices, default=' ')
    eighth_field = models.CharField(max_length=1, choices=board_choices, default=' ')
    ninth_field = models.CharField(max_length=1, choices=board_choices, default=' ')


    def __str__(self):
        return f"Board_{str(self.id)}"

    def win_board(self) -> bool:
        """Function which check board state, check if win condition has been met.
        """
        board_fields = [self.first_field,
                        self.second_field,
                        self.third_field,
                        self.fourth_field,
                        self.fifth_field,
                        self.sixth_field,
                        self.seventh_field,
                        self.eighth_field,
                        self.ninth_field
                        ]

        wins_conditions_list = [
            board_fields[0:3],
            board_fields[3:6],
            board_fields[6:9],
            board_fields[0::3],
            board_fields[1::3],
            board_fields[2::3],
            board_fields[0::4],
            board_fields[2::2][:3],
        ]

        for element in wins_conditions_list:
            if element.count('X') == 3 or element.count('O') == 3:
                return True

        return False

    def check_if_board_is_full(self) -> bool:
        board_fields = [self.first_field,
                        self.second_field,
                        self.third_field,
                        self.fourth_field,
                        self.fifth_field,
                        self.sixth_field,
                        self.seventh_field,
                        self.eighth_field,
                        self.ninth_field
                        ]
        index = 0
        for field in board_fields:
            if field != '':
                index += 1

        if index == 9:
            return True
        return False

    def check_if_field_is_empty(self, field) -> bool:
        """Method which check if field is empty."""

        if field == 'first_field':
            if self.first_field == ' ':
                return True
            return False
        elif field == 'second_field':
            if self.second_field == ' ':
                return True
            return False
        elif field == 'third_field':
            if self.third_field == ' ':
                return True
            return False
        elif field == 'fourth_field':
            if self.fourth_field == ' ':
                return True
            return False
        elif field == 'fifth_field':
            if self.fifth_field == ' ':
                return True
            return False
        elif field == 'sixth_field':
            if self.sixth_field == ' ':
                return True
            return False
        elif field == 'seventh_field':
            if self.seventh_field == ' ':
                return True
            return False
        elif field == 'eighth_field':
            if self.eighth_field == ' ':
                return True
            return False
        elif field == 'ninth_field':
            if self.ninth_field == ' ':
                return True
            return False
