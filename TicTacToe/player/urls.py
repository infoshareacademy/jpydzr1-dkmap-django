from django.urls import path
from .views import OurLoginView, OurSignUpView


urlpatterns = [
    path('login/', OurLoginView.as_view(), name='login-view'),
    path('signup/', OurSignUpView.as_view(), name='signup-view'),

]