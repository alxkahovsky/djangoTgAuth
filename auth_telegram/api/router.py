from rest_framework.routers import SimpleRouter
from .views import TelegramUserViewSet, TelegramAuthSessionViewSet

r = SimpleRouter()
r.register('telegram', TelegramUserViewSet)
r.register('telegram/auth', TelegramAuthSessionViewSet)

