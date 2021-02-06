from django.contrib import admin
from .models import Game, Board


@admin.register(Game)
class HouseAdmin(admin.ModelAdmin):
    pass


@admin.register(Board)
class HouseAdmin(admin.ModelAdmin):
    pass




