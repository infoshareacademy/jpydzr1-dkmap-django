from django.contrib.auth.models import AbstractUser, Group
from django.db import IntegrityError
from menu.models import PlayerStatistic
import logging

db_logger = logging.getLogger('db')


class CustomUser(AbstractUser):
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        group = Group.objects.get(name='Users')

        try:
            PlayerStatistic.objects.get_or_create(user=self)
        except IntegrityError as e:
            db_logger.error("duplicate key value violates unique constraint", exc_info=True)

        self.groups.add(group)
