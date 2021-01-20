from django.urls import path, include
from .views import ProfileView, BoardView, ApiView, login, CreateBoard, UpdateBoard
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'boards', ApiView, 'board')

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile-view'),
    path('board/', BoardView.as_view(), name='board'),
    path('api/', include(router.urls)),
    path('api/login', login),
    path('api/create', CreateBoard.as_view(), name='create_board'),
    path('api/update', UpdateBoard.as_view(), name='update_board'),

]
