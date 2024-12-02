from rest_framework.viewsets import ModelViewSet
from ..models import TelegramUser
from .serializer import TelegramUserSerializer


class TelegramUserViewSet(ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
