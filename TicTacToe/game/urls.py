from django.urls import path, include
from .views import ProfileView, \
    JoinGameBoardView, ApiView, login, \
    CreateBoard, UpdateBoard, JoinBoard, \
    RefreshBoard, ListBoardView
from menu.views import WelcomeView
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'boards', ApiView, 'board')

urlpatterns = [
    path('', WelcomeView.as_view(), name='welcome-view'),
    path('profile/', ProfileView.as_view(), name='profile-view'),
    path('boards/', ListBoardView.as_view(), name='list-board'),
    path('boards/<int:pk>/', JoinGameBoardView.as_view(), name='game-board'),

    path('api/', include(router.urls)),
    path('api/login', login),
    path('api/create', CreateBoard.as_view(), name='create_board'),
    path('api/update', UpdateBoard.as_view(), name='update_board'),
    path('api/join', JoinBoard.as_view(), name='join_board'),
    path('api/refresh', RefreshBoard.as_view(), name='refresh_board')
]
