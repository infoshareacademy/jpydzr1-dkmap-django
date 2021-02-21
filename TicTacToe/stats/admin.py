import pdfkit
from django.contrib import admin
from django.http import HttpResponse
from django.template.loader import get_template

from .models import PlayerStatistic


def get_a_report(modeladmin, request, queryset):

    template = get_template('pdf-report.html')
    html = template.render({
        'queryset': queryset,
        'labels': ['gdansk', 'moskwa'],
        'data': [1231312, 3213123]
    })

    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }
    pdf = pdfkit.from_string(html, False, options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment'
    filename = "person_list_pdf.pdf"
    return response


get_a_report.short_description = 'Select statistic and download a report.'


@admin.register(PlayerStatistic)
class PlayerStatsAdmin(admin.ModelAdmin):
    ordering = ['-game_counter']
    actions = [get_a_report]
