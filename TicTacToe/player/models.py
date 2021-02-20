from django.contrib.auth.models import AbstractUser, Group
from django.db import IntegrityError
from stats.models import PlayerStatistic
import logging

db_logger = logging.getLogger('db')


class CustomUser(AbstractUser):

    class Meta:
        default_permissions = ()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            PlayerStatistic.objects.get_or_create(user=self)
        except IntegrityError as e:
            db_logger.error("Duplicate key value violates unique constraint", exc_info=True)
