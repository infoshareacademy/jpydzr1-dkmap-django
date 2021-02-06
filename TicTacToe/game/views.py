from django.contrib import messages
from django.contrib.auth import authenticate
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, ListView, DetailView
from menu.models import PlayerStatistic
from rest_framework import viewsets, status
from .serializers import BoardSerializer
from .models import Board, Game
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from random import randint


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

        return context


class ApiView(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class CreateBoard(APIView):
    def post(self, request):
        try:
            user = self.request.user
            game = Game.objects.create()

            draw_number = randint(1, 100)
            if draw_number % 2:
                game.player_x = user
            else:
                game.player_o = user

            game.created_by = user
            game.save()

            board = Board(game=game)

        except:
            raise ValueError('Wrong input data. Try again.')

        if self.request.method == 'POST':
            serializer = BoardSerializer(board, data=self.request.data)
            data = {}
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshBoard(APIView):
    def get(self, request):
        try:
            user = self.request.user
            board_id = str(self.request._request).split('boards%2F')[1].split('%2F')[0]

            board = Board.objects.get(id=board_id)
            if board is None:
                return Response(data=board)

        except:
            raise ValueError('Wrong input data. Try again.')
        if request.method == 'GET':
            serializer = BoardSerializer(board, data=self.request.data)
            data = {}
            if serializer.is_valid():
                serializer.save()
                data['success'] = 'update successful'
                return Response(data=serializer.data)
            else:
                print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JoinBoard(APIView):
    def put(self, request):
        try:
            user = self.request.user
            board_number = self.request.data['joined_board']
            board = Board.objects.get(id=board_number)

            if board.game.player_x is None:
                if str(board.game.player_o) == str(user.username):
                    pass
                else:
                    board.game.player_x = user

            elif board.game.player_o is None:
                if str(board.game.player_x) == str(user.username):
                    pass
                else:
                    board.game.player_o = user

            else:
                pass

            board.game.save()

        except:
            raise ValueError('Wrong input data. Try again.')

        if request.method == 'PUT':
            serializer = BoardSerializer(board, data=self.request.data)
            data = {}
            if serializer.is_valid():
                serializer.save()
                data['success'] = 'update successful'
                return Response(data=serializer.data)
            else:
                print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def check_win_board(board) -> bool:
    if board.win_board():
        return True
    return False


def check_if_board_is_full(board) -> bool:
    if board.check_if_board_is_full():
        return True
    return False


class UpdateBoard(APIView):
    def put(self, request):
        try:
            user = self.request.user
            board_id = self.request.data['board_id'].split('boards/')[1].split('/')[0]

            board = Board.objects.get(id=board_id)
            field = self.request.data['button_id']

            # Empty field check:
            if board.check_if_field_is_empty(field) and board.game.in_progress:
                self.field_input(board, field)
            else:
                pass

            # Win/tie check:
            win = check_win_board(board)
            if win:
                board.game.win = True
                board.game.in_progress = False
            else:
                tie = check_if_board_is_full(board)
                if tie:
                    board.game.in_progress = False

            board.game.save()
        except:
            raise ValueError('Wrong input data. Try again.')

        if request.method == 'PUT':
            serializer = BoardSerializer(board, data=self.request.data)
            data = {}
            if serializer.is_valid():
                serializer.save()
                data['success'] = 'update successful'
                return Response(data=serializer.data)
            else:
                print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def message_for_user(self, state):
        messages.warning(self.request, state)
        return redirect('game-board', 528)

    def field_input(self, board, field):

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


# TODO: odswiezenie nickow, ??

# TODO: zliczanie wygranych, czasu itd.

# TODO: testy,

# TODO: heroku,

# TODO: logowanie,
