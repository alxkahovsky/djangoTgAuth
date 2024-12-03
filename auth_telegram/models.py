import uuid

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class TelegramAuthSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(default=None)

    def __str__(self):
        return f"{self.id}"


class TelegramUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='telegram_user')
    session = models.OneToOneField(TelegramAuthSession, on_delete=models.CASCADE,
                                         related_name='telegram_session', blank=True, null=True)
    telegram_id = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(blank=True, null=True, default=timezone.now)
    updated = models.DateTimeField(blank=True, null=True, default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.telegram_id}"


