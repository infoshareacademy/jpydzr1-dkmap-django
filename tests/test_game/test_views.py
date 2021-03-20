from django.test import TestCase, Client
from django.urls import reverse
from player.models import CustomUser
from stats.models import PlayerStatistic
from game.models import Board, Game


class TestProfileView(TestCase):

    def setUp(self) -> None:
        user = CustomUser.objects.create(username='testuser')
        user.set_password('testpassword')
        user.save()
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_check_if_user_logged_in(self) -> None:
        logged_in = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(logged_in)

    def test_when_user_not_log_in(self) -> None:
        self.client.logout()
        response = self.client.get('/game/profile/')
        self.assertEqual(response.status_code, 302)

    def test_view_urls_exists_at_desired_location(self) -> None:
        response = self.client.get('/game/profile/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('game:profile-view'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('game:profile-view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile_view.html')

    def test_context_has_correct_data(self) -> None:
        response = self.client.get(reverse('game:profile-view'))
        self.assertIsInstance(response.context['username'][0], PlayerStatistic)


class TestListBoardView(TestCase):

    def setUp(self) -> None:
        user = CustomUser.objects.create(username='testuser')
        user.set_password('testpassword')
        user.save()
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
        game = Game.objects.create()
        test_board = Board.objects.create(game=game)
        test_board.save()

    def test_check_if_user_logged_in(self) -> None:
        logged_in = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(logged_in)

    def test_when_user_not_log_in(self) -> None:
        self.client.logout()
        response = self.client.get('/game/boards/')
        self.assertEqual(response.status_code, 302)

    def test_view_urls_exists_at_desired_location(self) -> None:
        response = self.client.get('/game/boards/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('game:list-board'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('game:list-board'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_board_view.html')

    def test_context_has_correct_data(self) -> None:
        response = self.client.get(reverse('game:list-board'))
        self.assertIsInstance(response.context['all_current_boards'][0], Board)


class TestJoinGameBoardView(TestCase):

    def setUp(self) -> None:
        user = CustomUser.objects.create(username='testuser')
        user.set_password('testpassword')
        user.save()
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
        self.board_id = 1
        game = Game.objects.create(player_o=user, created_by=user)
        self.test_board = Board.objects.create(game=game, id=self.board_id)
        self.test_board.save()

    def test_check_if_user_logged_in(self) -> None:
        logged_in = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(logged_in)

    def test_when_user_not_log_in(self) -> None:
        self.client.logout()
        response = self.client.get('/game/boards/1/')
        self.assertEqual(response.status_code, 302)

    def test_view_urls_exists_at_desired_location(self) -> None:
        response = self.client.get('/game/boards/1/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('game:game-board', args=[self.board_id]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('game:game-board', args=[self.board_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game_board.html')

    def test_context_has_correct_data_when_creator_join(self) -> None:
        response = self.client.get(reverse('game:game-board', args=[self.board_id]))
        self.assertEqual(response.context['right_player'], 'Waiting for Player')
        self.assertEqual(response.context['right_player_sign'], 'X')
        self.assertEqual(response.context['left_player_sign'], 'O')
