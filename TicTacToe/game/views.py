import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View, ListView, DetailView

from stats.models import PlayerStatistic
from player.models import CustomUser
from .models import Board


db_logger = logging.getLogger('db')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = self.request.user
        context = {
            'username': PlayerStatistic.objects.filter(user=user),
        }

        return render(self.request, 'profile_view.html', context)


class ListBoardView(LoginRequiredMixin, ListView):
    model = Board
    context_object_name = 'all_current_boards'
    template_name = 'list_board_view.html'
    queryset = Board.objects.filter(game__in_progress=True).filter(
        Q(game__player_o=None) | Q(game__player_x=None)).order_by('game')


class JoinGameBoardView(LoginRequiredMixin, DetailView):
    model = Board
    template_name = 'game_board.html'

    def get_context_data(self, **kwargs):

        logged_user = self.request.user
        pk = str(self.request).split('boards/')[1].split('/')[0]

        player_1 = CustomUser.objects.get(id=logged_user.id)

        board_qs = Board.objects.select_related(
            'game__created_by',
            'game__player_x',
            'game__player_o').filter(id=pk)
        board = board_qs[0]

        if player_1 != board.game.created_by:
            if board.game.player_x is None:
                right_player = board.game.player_o
            else:
                right_player = board.game.player_x
        else:
            right_player = 'Waiting for Player'

        if player_1 == board.game.player_o:
            left_player_sign = 'O'
            right_player_sign = 'X'
        else:
            left_player_sign = 'X'
            right_player_sign = 'O'

        context = {
            'right_player': right_player,
            'right_player_sign': right_player_sign,
            'left_player_sign': left_player_sign,
        }

        self.request.session['last_visited_board'] = pk

        return context
