from django.test import TestCase
from game.models import Game, Board
from tests.common.constants import BOARD_FIELDS_EXPECTED, FIELD_EMPTY_VAL


class MyTestCase(TestCase):
    def test_board_default_state(self):
        board = Board()

        field_emptiness_statuses = {
            field_name: board.check_if_field_is_empty(field=field_name) for field_name in BOARD_FIELDS_EXPECTED
        }
        self.assertNotIn(
            False, field_emptiness_statuses.values(),
            f"in default state not all Board fields values were reported as empty:"
            f"reported: {field_emptiness_statuses}"
        )

        for _field_name in BOARD_FIELDS_EXPECTED:
            _field_val = getattr(board, _field_name)
            self.assertEqual(
                _field_val, FIELD_EMPTY_VAL,
                f"Board in default state reported a non-empty `{_field_name}` value:"
                f"reported: {_field_val}, expected: {FIELD_EMPTY_VAL}"
            )
        
        self.assertEqual(
            board.check_if_board_is_full(), (False, 0),
            "Board in default state reported to be full"
        )

        self.assertFalse(board.win_board(), "Board in default state reported win condition as met")

        self.assertFalse(
            board.end_game,
            f"Board in default state reported game end condition to be True - `end_game`={board.end_game}"
        )

        self.assertFalse(
            board.last_move,
            f"Board in default state reported last move dump as populated - `last_move`={board.last_move}"
        )

        self.assertIsNone(
            board.game,
            f"Board in default state reported game as populated - `game`={board.game}"
        )

        # game_time = board.get_game_time()
        # self.assertEquals(
        #     game_time, 0,
        #     f"Board in default state reported non-0 game time: {game_time}"
        # )

    def test_game_default_state(self):
        pass