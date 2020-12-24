from django.db import models


class Statistics(models.Model):

    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # statystyki ogolne:
        # - nick gracza,

        # - czas gry, ????
        # - rekordowy czas gry, ????

        # - ilosc wygranych, + 1
        # - ilosc przegranych, - 1

    pass


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
