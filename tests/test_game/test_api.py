from django.test import TestCase
from game.api import check_if_board_is_full
from game.models import Game, Board
from player.models import CustomUser
from stats.models import PlayerStatistic


class TestCheckIfBoardIsFull(TestCase):

    def setUp(self) -> None:
        self.game = Game.objects.create()
        self.test_board = Board.objects.create(game=self.game)
        self.test_board.save()

    def test_check_if_board_is_full_before_first_move(self) -> None:
        self.function_test = check_if_board_is_full(self.test_board)
        self.assertEqual(self.function_test[1], 0)
        self.assertFalse(self.function_test[0])

    def test_check_if_board_is_full_after_first_move(self) -> None:
        self.test_board.first_field = 'X'
        self.test_board.save()
        self.function_test = check_if_board_is_full(self.test_board)

        self.assertNotEqual(self.function_test[1], 0)
        self.assertFalse(self.function_test[0])

    def test_check_if_board_is_full_after_last_move(self) -> None:
        self.test_board.first_field = 'X'
        self.test_board.second_field = 'O'
        self.test_board.third_field = 'O'
        self.test_board.fourth_field = 'O'
        self.test_board.fifth_field = 'X'
        self.test_board.sixth_field = 'X'
        self.test_board.seventh_field = 'O'
        self.test_board.eighth_field = 'X'
        self.test_board.ninth_field = 'X'
        self.test_board.save()
        self.function_test = check_if_board_is_full(self.test_board)

        self.assertEqual(self.function_test[1], 0)
        self.assertTrue(self.function_test[0])
