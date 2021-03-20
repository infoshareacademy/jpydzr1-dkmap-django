from django.core.paginator import Paginator
from django.test import TestCase, Client
from django.urls import reverse
from player.models import CustomUser
from menu.views import LoggingReportView

from django_db_logger.models import StatusLog, LOG_LEVELS


class TestWelcomeView(TestCase):

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
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_urls_exists_at_desired_location(self) -> None:
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('menu:welcome-view'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('menu:welcome-view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'welcome_page.html')

    def test_context_has_correct_data(self) -> None:
        response = self.client.get(reverse('menu:welcome-view'))
        self.assertTrue(response.context['session'][0], "You haven't played yet.")


class TestNewGameView(TestCase):

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
        response = self.client.get('/new-game/')
        self.assertEqual(response.status_code, 302)

    def test_view_urls_exists_at_desired_location(self) -> None:
        response = self.client.get('/new-game/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('menu:new-game-view'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('menu:new-game-view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_game.html')


class TestLoggingReportView(TestCase):

    def setUp(self) -> None:
        user = CustomUser.objects.create(username='testuser')
        user.set_password('testpassword')
        user.save()
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
        self.logs = StatusLog.objects.create()
        self.logs.save()
        self.paginator = Paginator(self.logs, 5)

    def test_get_context(self) -> None:
        colors = ['#fff']
        log = {'10': '10', '20': '20', '30': '30'}
        context = LoggingReportView.get_context(colors=colors, log=log, page_obj=self.paginator, qs=self.logs)

        self.assertEqual(context['colors'], ['#fff'])
        self.assertIsInstance(context['page_obj'], Paginator)
        self.assertEqual(context['labels'], ['10', '20', '30'])
        self.assertEqual(context['labels'], ['10', '20', '30'])



