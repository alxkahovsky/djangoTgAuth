from django.contrib import admin
from .models import TelegramUser, TelegramAuthSession


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    model = TelegramUser


@admin.register(TelegramAuthSession)
class TelegramAuthSessionAdmin(admin.ModelAdmin):
    model = TelegramAuthSession
