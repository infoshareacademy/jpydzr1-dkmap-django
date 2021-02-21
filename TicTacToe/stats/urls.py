from django.urls import path, include
from rest_framework import routers
from .views import StatsApi
from django_pdfkit import PDFView

app_name = 'stats'
router = routers.DefaultRouter()
router.register(r'stats', StatsApi, 'stats')


urlpatterns = [
    path('api/', include(router.urls)),
    path(r'report-pdf/', PDFView.as_view(template_name='pdf-report.html'), name='report-pdf'),

]