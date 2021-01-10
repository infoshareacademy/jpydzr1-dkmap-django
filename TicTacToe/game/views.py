from django.shortcuts import render
from django.views.generic import View
from menu.models import PlayerStatistic


class ProfileView(View):
    def get(self, request):
        user = self.request.user

        context = {
            'username': PlayerStatistic.objects.filter(user=user),
        }

        return render(self.request, 'profile_view.html', context)

    def post(self, request):
        context = {
            'username': 'mateusz',
        }
        return render(self.request, 'profile_view.html', context)


class BoardView(View):
    def get(self, request):
        return render(self.request, 'board_view.html')

    def post(self, request):
        data = self.request.POST