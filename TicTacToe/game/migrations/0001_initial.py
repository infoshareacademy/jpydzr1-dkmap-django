# Generated by Django 3.1.4 on 2021-01-20 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_field', models.CharField(choices=[('X', 'X'), ('O', 'O'), ('-', '-')], default='-', max_length=1)),
                ('second_field', models.CharField(choices=[('X', 'X'), ('O', 'O'), ('-', '-')], default='-', max_length=1)),
                ('third_field', models.CharField(choices=[('X', 'X'), ('O', 'O'), ('-', '-')], default='-', max_length=1)),
                ('fourth_field', models.CharField(choices=[('X', 'X'), ('O', 'O'), ('-', '-')], default='-', max_length=1)),
                ('fifth_field', models.CharField(choices=[('X', 'X'), ('O', 'O'), ('-', '-')], default='-', max_length=1)),
                ('sixth_field', models.CharField(choices=[('X', 'X'), ('O', 'O'), ('-', '-')], default='-', max_length=1)),
                ('seventh_field', models.CharField(choices=[('X', 'X'), ('O', 'O'), ('-', '-')], default='-', max_length=1)),
                ('eighth_field', models.CharField(choices=[('X', 'X'), ('O', 'O'), ('-', '-')], default='-', max_length=1)),
                ('ninth_field', models.CharField(choices=[('X', 'X'), ('O', 'O'), ('-', '-')], default='-', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('multiplayer_game', models.BooleanField(default=False)),
                ('win', models.BooleanField(default=False)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('finish_time', models.DateTimeField(blank=True, null=True)),
                ('game_duration', models.DurationField(blank=True, null=True)),
            ],
        ),
    ]
