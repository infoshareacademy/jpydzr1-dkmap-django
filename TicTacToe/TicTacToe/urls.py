from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('menu.urls')),
    path('game/', include('game.urls')),
    path('player/', include('player.urls')),

]