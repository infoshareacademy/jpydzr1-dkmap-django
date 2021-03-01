import pdfkit
from django.contrib import admin
from django.db.models import Sum
from django.http import HttpResponse
from django.template.loader import get_template
from django_db_logger.models import StatusLog

from .models import PlayerStatistic


def get_a_report(modeladmin, request, queryset):

    game_amount = queryset.aggregate(game_amount=Sum('game_counter'))
    wins_amount = queryset.aggregate(wins_amount=Sum('win_counter'))
    game_time = queryset.aggregate(game_time=Sum('time_spend_in_game'))

    names = []
    for query in queryset:
        user = query.user.username
        names.append(user)

    users = StatusLog.objects.filter()

    template = get_template('pdf-report.html')
    html = template.render({
        'queryset': queryset,
        'game_amount': game_amount['game_amount'],
        'wins_amount': wins_amount['wins_amount'],
        'game_time': game_time['game_time']
    })

    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }
    pdf = pdfkit.from_string(html, False, options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment'

    return response


get_a_report.short_description = 'Select statistic and download a report.'


@admin.register(PlayerStatistic)
class PlayerStatsAdmin(admin.ModelAdmin):
    ordering = ['-game_counter']
    actions = [get_a_report]
