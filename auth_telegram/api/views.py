from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet
from ..models import TelegramUser, TelegramAuthSession
from .serializer import TelegramUserSerializer, TelegramAuthSessionSerializer


class TelegramUserViewSet(RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, GenericViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    lookup_field = 'telegram_id'


class TelegramAuthSessionViewSet(GenericViewSet):
    queryset = TelegramAuthSession.objects.all()
    serializer_class = TelegramAuthSessionSerializer

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    @action(detail=False, methods=['post'])
    def start(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
