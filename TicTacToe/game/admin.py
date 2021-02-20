from django.contrib import admin
from .models import Game, Board


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    pass
