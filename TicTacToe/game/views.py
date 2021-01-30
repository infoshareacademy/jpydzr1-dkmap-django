from django.contrib.auth import authenticate
from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
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


class BoardView(View):
    def get(self, request):

        logged_user = request.user

        player_1 = str(logged_user)

        player_2 = str(Board.objects.last().game.player_o)

        if player_1 == player_2:
            right_player = str(Board.objects.last().game.player_x)
            right_player_sign = 'X'
            left_player_sign = 'O'
        else:
            right_player = str(Board.objects.last().game.player_o)
            right_player_sign = 'O'
            left_player_sign = 'X'

        context = {
            'board': Board.objects.last(),
            'right_player': right_player,
            'right_player_sign': right_player_sign,
            'left_player_sign': left_player_sign,
            'open_games': Board.objects.filter(game__in_progress=True).filter(
                Q(game__player_o=None) | Q(game__player_x=None)).order_by('game')
        }

        return render(self.request, 'board_view.html', context)


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
            board = Board.objects.filter(game__in_progress=True).filter(Q(game__player_o=user) | Q(game__player_x=user)).last()
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
                board.game.player_x = user
            elif board.game.player_o is None:
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
            board = Board.objects.filter(game__in_progress=True).filter(Q(game__player_o=user) | Q(game__player_x=user)).last()
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

    def field_input(self, board, field):

        if field == 'first_field':
            if str(self.request.user) == board.game.player_x.username:
                board.first_field = 'X'
            else:
                board.first_field = 'O'
        elif field == 'second_field':
            if str(self.request.user) == board.game.player_x.username:
                board.second_field = 'X'
            else:
                board.second_field = 'O'
        elif field == 'third_field':
            if str(self.request.user) == board.game.player_x.username:
                board.third_field = 'X'
            else:
                board.third_field = 'O'
        elif field == 'fourth_field':
            if str(self.request.user) == board.game.player_x.username:
                board.fourth_field = 'X'
            else:
                board.fourth_field = 'O'
        elif field == 'fifth_field':
            if str(self.request.user) == board.game.player_x.username:
                board.fifth_field = 'X'
            else:
                board.fifth_field = 'O'
        elif field == 'sixth_field':
            if str(self.request.user) == board.game.player_x.username:
                board.sixth_field = 'X'
            else:
                board.sixth_field = 'O'
        elif field == 'seventh_field':
            if str(self.request.user) == board.game.player_x.username:
                board.seventh_field = 'X'
            else:
                board.seventh_field = 'O'
        elif field == 'eighth_field':
            if str(self.request.user) == board.game.player_x.username:
                board.eighth_field = 'X'
            else:
                board.eighth_field = 'O'
        elif field == 'ninth_field':
            if str(self.request.user) == board.game.player_x.username:
                board.ninth_field = 'X'
            else:
                board.ninth_field = 'O'

        return board

    def player_turn(self):
        pass


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


# TODO: odswiezenie nickow,

# TODO: tura graczy, kolejkowac,

# TODO: ID gry zamiast Board.objects.last()

# TODO: zliczanie wygranych, czasu itd.

# TODO: zabronic uzytkownikowi grac jesli nie ma 2 userow

# TODO: wlasny url dla kazdego boardu: primary key(pk)