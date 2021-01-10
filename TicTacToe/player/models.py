from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class CustomUser(AbstractUser):

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        group = Group.objects.get(id=2)
        self.groups.add(group)

