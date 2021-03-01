from django.urls import path, include
from .views import ProfileView, JoinGameBoardView, ListBoardView
from .api import login, BoardApi, JoinBoard
from menu.views import WelcomeView
from rest_framework import routers

app_name = 'game'
router = routers.DefaultRouter()
router.register(r'boards', BoardApi, basename='board')

urlpatterns = [
    path('', WelcomeView.as_view(), name='welcome-view'),
    path('profile/', ProfileView.as_view(), name='profile-view'),
    path('boards/', ListBoardView.as_view(), name='list-board'),
    path('boards/<int:pk>/', JoinGameBoardView.as_view(), name='game-board'),
    path('api/login', login),

    path('api/', include(router.urls)),
    path('api/create', BoardApi.as_view({'post': 'create'}), name='create_board'),
    path('api/update', BoardApi.as_view({'put': 'update'}), name='update_board'),
    path('api/refresh', BoardApi.as_view({'get': 'retrieve'}), name='refresh_board'),

    path('api/join', BoardApi.as_view({'put': 'join_board'}), name='join_board')

]
