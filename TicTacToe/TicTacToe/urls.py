from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('TicTacToe.menu.urls', namespace='menu')),
    path('game/', include('TicTacToe.game.urls', namespace='game')),
    path('stats/', include('TicTacToe.stats.urls', namespace='stats')),
    path('player/', include('TicTacToe.player.urls', namespace='player')),

]