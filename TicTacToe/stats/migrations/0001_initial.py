# Generated by Django 3.1.6 on 2021-02-16 15:55

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_spend_in_game', models.DurationField(default=datetime.timedelta(0))),
                ('best_game_time', models.DurationField(default=datetime.timedelta(0))),
                ('game_counter', models.PositiveIntegerField(default=0)),
                ('win_counter', models.PositiveIntegerField(default=0)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]