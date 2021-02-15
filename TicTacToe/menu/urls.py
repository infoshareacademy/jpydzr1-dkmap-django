from django.urls import path
from .views import WelcomeView, GameDetailView, NewGameView, LoggingReportView, export_log_to_csv

app_name = 'menu'


urlpatterns = [
    path('', WelcomeView.as_view(), name='welcome-view'),
    path('game-detail/', GameDetailView.as_view(), name='game-detail'),
    path('new-game/', NewGameView.as_view(), name='new-game-view'),
    path('log-report/', LoggingReportView.as_view(), name='log-report-view'),
    path('export-to-csv', export_log_to_csv, name='export-to-csv')

]
