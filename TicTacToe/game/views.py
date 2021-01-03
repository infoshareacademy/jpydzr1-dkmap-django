from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

# Create your views here.


class ProfileView(View):
    def get(self, request):
        context = {
            'username': 'mateusz',
        }
        return render(self.request, 'profile_view.html')

    def post(self, request):
        context = {
            'username': 'mateusz',
        }
        return render(self.request, 'profile_view.html', context)
