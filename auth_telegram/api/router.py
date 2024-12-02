from rest_framework.routers import SimpleRouter
from .views import TelegramUserViewSet

r = SimpleRouter()
r.register('create', TelegramUserViewSet)