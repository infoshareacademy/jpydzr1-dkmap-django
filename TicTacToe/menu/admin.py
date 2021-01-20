from django.contrib import admin
from menu.models import PlayerStatistic

admin.site.site_header = 'TicTacToe'

admin.site.register(PlayerStatistic)


