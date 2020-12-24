from django.urls import path
from menu.views import WelcomeView, GameDetailView


urlpatterns = [
    path('', WelcomeView.as_view(), name='welcome-view'),
    path('game-detail/', GameDetailView.as_view(), name='game-detail'),

]
