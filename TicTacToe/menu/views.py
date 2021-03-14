import csv
from collections import Counter
from random import randint

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


class NewGameView(View):
    def get(self, request):
        return render(self.request, 'new_game.html')


class LoggingReportView(View):
    def get(self, request):
        date_min = request.GET.get('date_min')
        date_max = request.GET.get('date_max')
        log_level = request.GET.get('log_level')

        filter_dict = {}

        if self.is_valid_queryparam(date_min):
            filter_dict['create_datetime__gte'] = date_min

        if self.is_valid_queryparam(date_max):
            filter_dict['create_datetime__lt'] = date_max

        if self.is_valid_queryparam(log_level) and log_level != '':
            log_level = log_level[1:3]
            filter_dict['level'] = log_level

        qs = StatusLog.objects.filter(**filter_dict)

        paginator = Paginator(qs, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        all_logs = list(StatusLog.objects.filter(**filter_dict).values_list('level', flat=True))
        log = Counter(all_logs)

        colors = []
        for color in range(5):
            color = '#%06x' % randint(0, 0xFFFFFF)
            colors.append(color)

        context = {
            'queryset': qs,
            'log_levels': LOG_LEVELS[1:],
            'page_obj': page_obj,
            'labels': list(log.keys()),
            'data': list(log.values()),
            'colors': colors,
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
