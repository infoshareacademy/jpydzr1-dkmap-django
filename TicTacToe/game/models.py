import time
from datetime import timedelta

from django.db import models
from django.conf import settings


board_choices = (
    ('X', 'X'),
    ('O', 'O'),
    (' ', ' '),
    )

X_or_O = (
    ('X', 'X'),
    ('O', 'O')
    )


class Game(models.Model):
    player_x = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="player_x_games",
        on_delete=models.CASCADE,
        blank=True,
        null=True
        )
    player_o = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="player_o_games",
        on_delete=models.CASCADE,
        blank=True,
        null=True
        )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='created_games',
        on_delete=models.CASCADE,
        null=True,
        blank=True
        )
    in_progress = models.BooleanField(default=True)
    win = models.BooleanField(default=False)
    start_time = models.FloatField(null=True, blank=True)
    finish_time = models.FloatField(null=True, blank=True)

    def __str__(self):
        state = 'not finished' if self.in_progress else 'finished'
        return f"Game {self.id} - {state}"


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
    last_move = models.CharField(max_length=1, choices=X_or_O, blank=True)
    end_game = models.BooleanField(default=False)

    @property
    def data(self):
        return {
            'game': self.game.id,
            'first_field': self.first_field,
            'second_field': self.second_field,
            'third_field': self.third_field,
            'fourth_field': self.fourth_field,
            'fifth_field': self.fifth_field,
            'sixth_field': self.sixth_field,
            'seventh_field': self.seventh_field,
            'eighth_field': self.eighth_field,
            'ninth_field': self.ninth_field,
            'last_move': self.last_move,
            'end_game': self.end_game
        }

    def __str__(self):
        return f"Board {self.id}"

    def get_game_time(self) -> timedelta:
        game_duration = self.game.finish_time - self.game.start_time
        return timedelta(seconds=game_duration)

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

    def check_if_board_is_full(self):
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
            if field != ' ':
                index += 1

        start_time = time.perf_counter() if index == 1 else 0

        if index == 9:
            return True, start_time
        return False, start_time

    def check_if_field_is_empty(self, field) -> bool:
        """Method which check if field is empty."""
        board_fields = [
            self.first_field,
            self.second_field,
            self.third_field,
            self.fourth_field,
            self.fifth_field,
            self.sixth_field,
            self.seventh_field,
            self.eighth_field,
            self.ninth_field
            ]

        board_number = {
            'first_field': 0,
            'second_field': 1,
            'third_field': 2,
            'fourth_field': 3,
            'fifth_field': 4,
            'sixth_field': 5,
            'seventh_field': 6,
            'eighth_field': 7,
            'ninth_field': 8
            }

        for element in board_number.items():
            if field == element[0]:
                current_field = board_fields[element[1]]
                if current_field == ' ':
                    return True
                return False


