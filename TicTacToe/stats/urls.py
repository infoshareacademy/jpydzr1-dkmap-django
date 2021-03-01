from django.urls import path, include
from rest_framework import routers
from .views import StatsApi

app_name = 'stats'
router = routers.DefaultRouter()
router.register(r'stats', StatsApi, 'stats')


urlpatterns = [
    path('api/', include(router.urls)),

]