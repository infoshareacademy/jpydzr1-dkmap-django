from django.urls import path
from game.views import ProfileView


urlpatterns = [
    path('', ProfileView.as_view(), name='profile-view')

]
