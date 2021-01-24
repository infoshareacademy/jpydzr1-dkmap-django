from django.contrib.auth.models import AbstractUser, Group


class CustomUser(AbstractUser):
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        group = Group.objects.get(name='Users')
        self.groups.add(group)
