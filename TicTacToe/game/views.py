from django.contrib.auth import authenticate
from django.contrib.auth.models import User
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
        context = {
            'board': Board.objects.last()
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


class JoinBoard(APIView):
    def put(self, request):
        try:
            user = self.request.user
            board = Board.objects.last()

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


class UpdateBoard(APIView):
    def put(self, request):
        try:
            user = self.request.user
            board = Board.objects.last()
            field = self.request.data['button_id']
            self.field_input(board, field)

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
            board.first_field = 'X'
        elif field == 'second_field':
            board.second_field = 'X'
        elif field == 'third_field':
            board.third_field = 'X'
        elif field == 'fourth_field':
            board.fourth_field = 'X'
        elif field == 'fifth_field':
            board.fifth_field = 'X'
        elif field == 'sixth_field':
            board.sixth_field = 'X'
        elif field == 'seventh_field':
            board.seventh_field = 'O'
        elif field == 'eighth_field':
            board.eighth_field = 'O'
        elif field == 'ninth_field':
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
