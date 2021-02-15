from django.shortcuts import render
from django.views.generic import TemplateView, View


class WelcomeView(TemplateView):

    def get(self, request):

        try:
            session_element = self.request.session['last_visited_board']
        except KeyError:
            session_element = "You haven't played yet."

        context = {
            'session': session_element,
        }

        return render(request, 'welcome_page.html', context)


class GameDetailView(View):
    def get(self, request):
        return render(self.request, 'game_detail.html')


class NewGameView(View):
    def get(self, request):
        return render(self.request, 'new_game.html')
