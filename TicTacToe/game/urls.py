from django.urls import path
from game.views import ProfileView


urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile-view')

]
