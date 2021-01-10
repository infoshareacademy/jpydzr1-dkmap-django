from django.urls import path
from game.views import ProfileView, BoardView


urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile-view'),
    path('board/', BoardView.as_view(), name='board'),

]
