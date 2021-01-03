from django.urls import path
from menu.views import WelcomeView, GameDetailView, NewGameView


urlpatterns = [
    path('', WelcomeView.as_view(), name='welcome-view'),
    path('game-detail/', GameDetailView.as_view(), name='game-detail'),
    path('new-game/', NewGameView.as_view(), name='new-game-view'),

]
