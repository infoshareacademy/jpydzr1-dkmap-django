from django.shortcuts import render
from django.views.generic import TemplateView, View


class WelcomeView(TemplateView):
    template_name = 'welcome_page.html'


class GameDetailView(View):
    def get(self, request):
        return render(self.request, 'game_detail.html')


class NewGameView(View):
    def get(self, request):
        return render(self.request, 'new_game.html')

