from django.urls import path, include
from rest_framework import routers
from .views import ApiView

app_name = 'stats'
router = routers.DefaultRouter()
router.register(r'stats', ApiView, 'stats')


urlpatterns = [
    path('api/', include(router.urls)),

]