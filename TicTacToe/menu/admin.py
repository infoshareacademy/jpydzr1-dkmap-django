from django.contrib import admin
from .models import PlayerStatistic

admin.site.site_header = 'TicTacToe'


@admin.register(PlayerStatistic)
class HouseAdmin(admin.ModelAdmin):
    pass

