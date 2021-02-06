# Generated by Django 3.1.4 on 2021-01-24 11:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_spend_in_game', models.DurationField(default=datetime.timedelta(0))),
                ('best_game_time', models.DurationField(default=datetime.timedelta(0))),
                ('game_counter', models.IntegerField(default=0)),
                ('win_counter', models.IntegerField(default=0)),
                ('lose_counter', models.IntegerField(default=0)),
            ],
        ),
    ]
