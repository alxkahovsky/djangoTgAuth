from django.db import models
from django.contrib.auth.models import User


class TelegramUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_id = models.CharField(max_length=255, unique=True)
    # token = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.user.username} - {self.telegram_id}"
