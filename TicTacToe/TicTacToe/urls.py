import debug_toolbar
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('menu.urls', namespace='menu')),
    path('game/', include('game.urls', namespace='game')),
    path('stats/', include('stats.urls', namespace='stats')),
    path('player/', include('player.urls', namespace='player')),

]