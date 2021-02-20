from datetime import timedelta

from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import PlayerStatistic
from .serializers import PlayerStatisticsSerializer
from game.models import Board


class ApiView(viewsets.ModelViewSet):
    queryset = PlayerStatistic.objects.all()
    serializer_class = PlayerStatisticsSerializer

    def add_win(self, request):
        user = request.user
        statistics = PlayerStatistic.objects.get(user=user)
        statistics.win_counter += 1
        statistics.save()
        serializer = PlayerStatisticsSerializer(statistics, data=request.data)
        if serializer.is_valid():
            wins = serializer.data['win_counter']
            return Response(data={'wins': wins}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def add_game(self, request):
        user = request.user
        statistics = PlayerStatistic.objects.get(user=user)
        statistics.game_counter += 1
        statistics.save()
        serializer = PlayerStatisticsSerializer(statistics, data=request.data)
        if serializer.is_valid():
            games = serializer.data['game_counter']
            return Response(data={'games': games}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def add_total_time(self, request, board_id):
        user = request.user
        board = Board.objects.get(id=board_id)
        statistics = PlayerStatistic.objects.get(user=user)
        statistics.time_spend_in_game += board.get_game_time()
        statistics.save()
        self.add_total_time_for_looser(request, board_id, user)

        serializer = PlayerStatisticsSerializer(statistics, data=request.data)
        if serializer.is_valid():
            time_spend_in_game = serializer.data['time_spend_in_game']
            return Response(data={'time_spend_in_game': time_spend_in_game}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def add_best_time(self, request, board_id):
        user = request.user
        board = Board.objects.get(id=board_id)
        statistics = PlayerStatistic.objects.get(user=user)
        best_time_so_far = statistics.best_game_time
        current_game_time = board.get_game_time()
        if best_time_so_far == timedelta(seconds=0):
            statistics.best_game_time = current_game_time

        elif current_game_time < best_time_so_far:
            statistics.best_game_time = current_game_time

        statistics.save()

        serializer = PlayerStatisticsSerializer(statistics, data=request.data)
        if serializer.is_valid():
            best_game_time = serializer.data['best_game_time']
            return Response(data={'best_game_time': best_game_time}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def add_total_time_for_looser(request, board_id, user):
        board = Board.objects.get(id=board_id)
        player_x = board.game.player_x
        player_o = board.game.player_o
        if player_x == user:
            statistics = PlayerStatistic.objects.get(user=player_o)
        else:
            statistics = PlayerStatistic.objects.get(user=player_x)

        statistics.time_spend_in_game += board.get_game_time()
        statistics.save()

        serializer = PlayerStatisticsSerializer(statistics, data=request.data)
        if serializer.is_valid():
            time_spend_in_game = serializer.data['time_spend_in_game']
            return Response(data={'time_spend_in_game': time_spend_in_game}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)