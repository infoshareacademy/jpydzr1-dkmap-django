import csv
import os
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django_db_logger.models import StatusLog, LOG_LEVELS


class WelcomeView(TemplateView):

    def get(self, request):

        try:
            session_element = self.request.session['last_visited_board']
        except KeyError:
            session_element = "You haven't played yet."

        context = {
            'session': session_element,
        }

        return render(request, 'welcome_page.html', context)


class GameDetailView(View):
    def get(self, request):
        return render(self.request, 'game_detail.html')


class NewGameView(View):
    def get(self, request):
        return render(self.request, 'new_game.html')


class LoggingReportView(View):
    def get(self, request):

        qs = StatusLog.objects.all()

        date_min = request.GET.get('date_min')
        date_max = request.GET.get('date_max')
        log_level = request.GET.get('log_level')

        if self.is_valid_queryparam(date_min):
            qs = qs.filter(create_datetime__gte=date_min)
        if self.is_valid_queryparam(date_max):
            qs = qs.filter(create_datetime__lt=date_max)

        if self.is_valid_queryparam(log_level) and log_level != 'Choose..':
            log_level = log_level[1:3]
            qs = qs.filter(level=log_level)

        # params_list = [
        #     'date_min',
        #     'date_max',
        #     'log_level'
        # ]
        # filter_dict = {}
        #
        # for param in params_list:
        #     x = request.GET.get(param)
        #     if x == '' or x is None:
        #         continue
        #     else:
        #         filter_dict[param] = request.GET.get(param)
        #
        # qs = StatusLog.objects.filter(**filter_dict)

        paginator = Paginator(qs, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'queryset': qs,
            'log_levels': LOG_LEVELS[1:],
            'page_obj': page_obj
        }

        return render(self.request, 'logging_report.html', context)

    @staticmethod
    def is_valid_queryparam(param):
        return param != '' and param is not None

@login_required
def export_log_to_csv(request):
    from datetime import date
    response = HttpResponse(content_type='text/csv')
    today = date.today()
    date = today.strftime("%d/%m/%Y")
    file_name = f'Logs - {date}'
    response['Content-Disposition'] = f'attachment; filename="{file_name}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Message', 'Level', 'Date'])
    qs = StatusLog.objects.all()
    for log in qs.values_list('msg', 'level', 'create_datetime'):
        writer.writerow(log)

    return response
