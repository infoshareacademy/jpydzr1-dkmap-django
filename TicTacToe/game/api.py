import time
from random import randint
import logging

from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import authenticate
from django.shortcuts import redirect

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, status

from stats.views import StatsApi
from .serializers import BoardSerializer
from .models import Board, Game

db_logger = logging.getLogger('db')


def check_if_board_is_full(board):
    tie, start_time = board.check_if_board_is_full()
    if tie:
        return True, start_time
    return False, start_time


def stats_update(request, statistic, board_id=None):
    player_stats = StatsApi()

    if statistic == 'win_counter':
        player_stats.add_win(request)
    elif statistic == 'game_counter':
        player_stats.add_game(request)
    elif statistic == 'best_time':
        player_stats.add_best_time(request, board_id)
    elif statistic == 'total_time':
        player_stats.add_total_time(request, board_id)


def victory_check(request, board, board_id):
    win = board.win_board()
    if win:
        board.game.win = True
        board.game.in_progress = False
        board.game.finish_time = time.perf_counter()
        board.game.save()
        stats_update(request, 'win_counter')
        stats_update(request, 'total_time', board_id=board_id)
        stats_update(request, 'best_time', board_id=board_id)


def tie_check(request, board, board_id):
    tie, start_time = check_if_board_is_full(board)
    if start_time != 0:
        board.game.start_time = start_time
    if tie:
        board.game.in_progress = False
        board.game.finish_time = time.perf_counter()
        board.game.save()
        stats_update(request, 'total_time', board_id=board_id)


class BoardApi(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def create(self, request, *args, **kwargs):
        board = self.get_data_for_new_board(request)

        serializer = self.get_serializer(data=board.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @staticmethod
    def get_data_for_new_board(request):
        user = request.user
        game = Game.objects.create()
        draw_number = randint(1, 100)
        if draw_number % 2:
            game.player_x = user
        else:
            game.player_o = user
        game.created_by = user
        game.save()
        board = Board(game=game)
        db_logger.info(f'Game created by {user} - board {board.game_id}.')
        stats_update(request, 'game_counter')

        return board

    def update(self, request, *args, **kwargs):
        board = self.get_data_for_updating_board(request)

        partial = kwargs.pop('partial', False)
        instance = Board()
        serializer = self.get_serializer(board, data=board.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def get_data_for_updating_board(self, request):
        board_id = self.request.data['board_id'].split('boards/')[1].split('/')[0]

        board = Board.objects.get(id=board_id)
        field = self.request.data['button_id']
        # Check if field is empty:
        if board.check_if_field_is_empty(field) and board.game.in_progress:
            self.field_input(board, field)
        else:
            pass
        # Check victory
        victory_check(request, board, board_id)
        # Check tie
        tie_check(request, board, board_id)
        board.game.save()
        return board

    def field_input(self, board, field) -> Board:

        # board_fields = [board.first_field,
        #                 board.second_field,
        #                 board.third_field,
        #                 board.fourth_field,
        #                 board.fifth_field,
        #                 board.sixth_field,
        #                 board.seventh_field,
        #                 board.eighth_field,
        #                 board.ninth_field
        #                 ]
        #
        # board_number = {'first_field': 0,
        #                 'second_field': 1,
        #                 'third_field': 2,
        #                 'fourth_field': 3,
        #                 'fifth_field': 4,
        #                 'sixth_field': 5,
        #                 'seventh_field': 6,
        #                 'eighth_field': 7,
        #                 'ninth_field': 8
        #                 }
        #
        # for element in board_number.items():
        #     if field == element[0]:
        #         if self.two_players_on_board_validation(board):
        #             pass
        #         elif str(self.request.user) == board.game.player_x.username:
        #             if self.last_move_validation(board, 'X'):
        #                 board_fields[element[1]] = 'X'
        #                 board.last_move = 'X'
        #
        #         elif str(self.request.user) == board.game.player_o.username:
        #             if self.last_move_validation(board, 'O'):
        #                 board_fields[element[1]] = 'O'
        #                 board.last_move = 'O'
        # return board

        # x = board_number[field]
        # y = board_fields[x]
        # print(x)
        # print(y)

        if field == 'first_field':
            if self.two_players_on_board_validation(board):
                pass
            elif str(self.request.user) == board.game.player_x.username:
                if self.last_move_validation(board, 'X'):
                    board.first_field = 'X'
                    board.last_move = 'X'
            elif str(self.request.user) == board.game.player_o.username:
                if self.last_move_validation(board, 'O'):
                    board.first_field = 'O'
                    board.last_move = 'O'

        elif field == 'second_field':
            if self.two_players_on_board_validation(board):
                pass
            elif str(self.request.user) == board.game.player_x.username:
                if self.last_move_validation(board, 'X'):
                    board.second_field = 'X'
                    board.last_move = 'X'
            elif str(self.request.user) == board.game.player_o.username:
                if self.last_move_validation(board, 'O'):
                    board.second_field = 'O'
                    board.last_move = 'O'

        elif field == 'third_field':
            if self.two_players_on_board_validation(board):
                pass
            elif str(self.request.user) == board.game.player_x.username:
                if self.last_move_validation(board, 'X'):
                    board.third_field = 'X'
                    board.last_move = 'X'
            elif str(self.request.user) == board.game.player_o.username:
                if self.last_move_validation(board, 'O'):
                    board.third_field = 'O'
                    board.last_move = 'O'

        elif field == 'fourth_field':
            if self.two_players_on_board_validation(board):
                pass
            elif str(self.request.user) == board.game.player_x.username:
                if self.last_move_validation(board, 'X'):
                    board.fourth_field = 'X'
                    board.last_move = 'X'
            elif str(self.request.user) == board.game.player_o.username:
                if self.last_move_validation(board, 'O'):
                    board.fourth_field = 'O'
                    board.last_move = 'O'

        elif field == 'fifth_field':
            if self.two_players_on_board_validation(board):
                pass
            elif str(self.request.user) == board.game.player_x.username:
                if self.last_move_validation(board, 'X'):
                    board.fifth_field = 'X'
                    board.last_move = 'X'
            elif str(self.request.user) == board.game.player_o.username:
                if self.last_move_validation(board, 'O'):
                    board.fifth_field = 'O'
                    board.last_move = 'O'

        elif field == 'sixth_field':
            if self.two_players_on_board_validation(board):
                pass
            elif str(self.request.user) == board.game.player_x.username:
                if self.last_move_validation(board, 'X'):
                    board.sixth_field = 'X'
                    board.last_move = 'X'
            elif str(self.request.user) == board.game.player_o.username:
                if self.last_move_validation(board, 'O'):
                    board.sixth_field = 'O'
                    board.last_move = 'O'

        elif field == 'seventh_field':
            if self.two_players_on_board_validation(board):
                pass
            elif str(self.request.user) == board.game.player_x.username:
                if self.last_move_validation(board, 'X'):
                    board.seventh_field = 'X'
                    board.last_move = 'X'
            elif str(self.request.user) == board.game.player_o.username:
                if self.last_move_validation(board, 'O'):
                    board.seventh_field = 'O'
                    board.last_move = 'O'

        elif field == 'eighth_field':
            if self.two_players_on_board_validation(board):
                pass
            elif str(self.request.user) == board.game.player_x.username:
                if self.last_move_validation(board, 'X'):
                    board.eighth_field = 'X'
                    board.last_move = 'X'
            elif str(self.request.user) == board.game.player_o.username:
                if self.last_move_validation(board, 'O'):
                    board.eighth_field = 'O'
                    board.last_move = 'O'

        elif field == 'ninth_field':
            if self.two_players_on_board_validation(board):
                pass
            elif str(self.request.user) == board.game.player_x.username:
                if self.last_move_validation(board, 'X'):
                    board.ninth_field = 'X'
                    board.last_move = 'X'
            elif str(self.request.user) == board.game.player_o.username:
                if self.last_move_validation(board, 'O'):
                    board.ninth_field = 'O'
                    board.last_move = 'O'
        return board

    def retrieve(self, request, *args, **kwargs):
        board = self.get_data_for_board_refresh(request)
        if board is None:
            return Response(data=board)

        instance = board
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @staticmethod
    def get_data_for_board_refresh(request):
        board_id = str(request._request).split('boards%2F')[1].split('%2F')[0]
        board = Board.objects.get(id=board_id)
        return board

    @staticmethod
    def last_move_validation(board, sign):
        if board.last_move != sign:
            return True
        return False

    @staticmethod
    def two_players_on_board_validation(board):
        if board.game.player_x is None or board.game.player_o is None:
            return True
        return False

    def message_for_user(self, state):
        messages.warning(self.request, state)
        return redirect('game-board', 528)

    def join_board(self, request, *args, **kwargs):

        board = self.get_data_for_join_board(request)
        board.game.save()

        partial = kwargs.pop('partial', False)
        instance = Board()
        serializer = self.get_serializer(board, data=board.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @staticmethod
    def get_data_for_join_board(request):
        user = request.user
        board_number = request.data['joined_board']
        board = Board.objects.get(id=board_number)

        if board.game.player_x is None:
            if str(board.game.player_o) == str(user.username):
                pass
            else:
                board.game.player_x = user
                db_logger.info(f'{user} joined board {board_number}.')
                stats_update(request, 'game_counter')

        elif board.game.player_o is None:
            if str(board.game.player_x) == str(user.username):
                pass
            else:
                board.game.player_o = user
                db_logger.info(f'{user} joined board {board_number}.')
                stats_update(request, 'game_counter')
        return board


class JoinBoard(APIView):
    pass
    # def put(self, request):
    #     try:
    #         user = self.request.user
    #         board_number = self.request.data['joined_board']
    #         board = Board.objects.get(id=board_number)
    #
    #         if board.game.player_x is None:
    #             if str(board.game.player_o) == str(user.username):
    #                 pass
    #             else:
    #                 board.game.player_x = user
    #                 db_logger.info(f'{user} joined board {board_number}.')
    #                 stats_update(request, 'game_counter')
    #
    #         elif board.game.player_o is None:
    #             if str(board.game.player_x) == str(user.username):
    #                 pass
    #             else:
    #                 board.game.player_o = user
    #                 db_logger.info(f'{user} joined board {board_number}.')
    #                 stats_update(request, 'game_counter')
    #
    #         board.game.save()
    #
    #     except:
    #         raise ValueError('Wrong input data. Try again.')
    #
    #     if request.method == 'PUT':
    #         serializer = BoardSerializer(board, data=self.request.data)
    #         data = {}
    #         if serializer.is_valid():
    #             serializer.save()
    #             data['success'] = 'update successful'
    #             return Response(data=serializer.data)
    #         else:
    #             print(serializer.errors)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)