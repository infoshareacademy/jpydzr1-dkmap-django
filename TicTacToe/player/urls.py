from django.urls import path
from .views import CustomLoginView, CustomSignUpView, CustomLogoutView

app_name = 'player'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login-view'),
    path('signup/', CustomSignUpView.as_view(), name='signup-view'),
    path('logout/', CustomLogoutView.as_view(), name='logout-view'),

]