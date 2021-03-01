import logging

from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View, ListView, DetailView

from stats.models import PlayerStatistic
from .models import Board


db_logger = logging.getLogger('db')


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


class ListBoardView(ListView):
    model = Board
    context_object_name = 'all_current_boards'
    template_name = 'list_board_view.html'
    queryset = Board.objects.filter(game__in_progress=True).filter(
        Q(game__player_o=None) | Q(game__player_x=None)).order_by('game')


class JoinGameBoardView(DetailView):
    model = Board
    template_name = 'game_board.html'

    def get_context_data(self, **kwargs):

        logged_user = self.request.user
        pk = str(self.request).split('boards/')[1].split('/')[0]

        player_1 = str(logged_user)
        player_2 = str(Board.objects.get(id=pk).game.player_o)

        if player_1 == player_2:
            if Board.objects.get(id=pk).game.player_x is None:
                right_player = 'Waiting for player'
            else:
                right_player = str(Board.objects.get(id=pk).game.player_x)

            right_player_sign = 'X'
            left_player_sign = 'O'
        else:
            if Board.objects.get(id=pk).game.player_o is None:
                right_player = 'Waiting for player'
            else:
                right_player = player_2
            right_player_sign = 'O'
            left_player_sign = 'X'

        context = {
            'right_player': right_player,
            'right_player_sign': right_player_sign,
            'left_player_sign': left_player_sign,
        }

        self.request.session['last_visited_board'] = pk

        return context

