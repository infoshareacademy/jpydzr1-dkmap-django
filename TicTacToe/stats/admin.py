from django.contrib import admin
from .models import PlayerStatistic


@admin.register(PlayerStatistic)
class PlayerStatsAdmin(admin.ModelAdmin):
    pass
